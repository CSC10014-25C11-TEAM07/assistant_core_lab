import httpx
import pytest
from fastapi.testclient import TestClient

from assistant_api.db import Repository, init_db, make_engine
from assistant_api.main import create_app
from assistant_api.weather import WeatherClient

OK_JSON = {"current": {"time": "2026-10-05T09:00", "temperature_2m": 31.2, "weather_code": 3, "wind_speed_10m": 8.5}}


def weather_with(handler) -> WeatherClient:
    transport = httpx.MockTransport(handler)
    return WeatherClient("https://example.test/forecast", 10.76, 106.68, retries=1, transport=transport)


@pytest.fixture
def repo():
    engine = make_engine("sqlite://")
    init_db(engine)
    return Repository(engine, "test-salt")


@pytest.fixture
def client(settings, service, repo):
    settings = settings.model_copy(update={"api_admin_key": "secret-admin", "rate_limit_per_min": 5})
    app = create_app(settings, service, weather_with(lambda req: httpx.Response(200, json=OK_JSON)), repo)
    return TestClient(app)


def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200 and r.json()["status"] == "ok"


def test_chat_fee(client):
    r = client.post("/v1/chat", json={"message": "tuition for 18 credits and 2 retake"})
    assert r.status_code == 200
    body = r.json()
    assert body["intent"] == "fee" and "9,450,000" in body["answer"] and body["request_id"]


def test_chat_validation_error(client):
    r = client.post("/v1/chat", json={"message": ""})
    assert r.status_code == 422 and r.json()["error"]["code"] == "invalid_request"


def test_rate_limit(client):
    codes = [client.post("/v1/chat", json={"message": "hi"}).status_code for _ in range(6)]
    assert codes[-1] == 429


def test_feedback_roundtrip(client):
    rid = client.post("/v1/chat", json={"message": "hi"}).json()["request_id"]
    r = client.post("/v1/feedback", json={"request_id": rid, "rating": 1})
    assert r.status_code == 201 and r.json()["id"] == 1
    assert client.get("/v1/feedback").status_code == 401
    listed = client.get("/v1/feedback", headers={"X-API-Key": "secret-admin"})
    assert listed.status_code == 200 and len(listed.json()) == 1


def test_feedback_rating_out_of_range(client):
    assert client.post("/v1/feedback", json={"request_id": "x", "rating": 5}).status_code == 422


def test_feedback_unknown_request_returns_404(client):
    response = client.post("/v1/feedback", json={"request_id": "nope", "rating": -1})
    assert response.status_code == 404
    assert response.json()["error"]["code"] == "unknown_request_id"


def test_feedback_survives_app_and_database_engine_restart(tmp_path, settings, service):
    settings = settings.model_copy(update={"api_admin_key": "restart-test-key"})
    url = f"sqlite:///{tmp_path / 'restart.db'}"
    engine = make_engine(url)
    init_db(engine)
    app = create_app(settings, service, repo=Repository(engine, "restart-test-salt"))
    with TestClient(app) as first:
        rid = first.post("/v1/chat", json={"message": "hi", "session_id": "synthetic-session"}).json()["request_id"]
        saved = first.post("/v1/feedback", json={"request_id": rid, "rating": 1, "comment": "Synthetic test"})
        assert saved.status_code == 201
        saved_id = saved.json()["id"]
    engine.dispose()

    # Build a new engine and app against the same file, with no shared repository.
    restarted_engine = make_engine(url)
    restarted_app = create_app(settings, service, repo=Repository(restarted_engine, "restart-test-salt"))
    with TestClient(restarted_app) as restarted:
        assert restarted.get("/v1/feedback").status_code == 401
        listed = restarted.get("/v1/feedback", headers={"X-API-Key": "restart-test-key"})
        assert listed.status_code == 200
        assert [(fb["id"], fb["request_id"], fb["rating"]) for fb in listed.json()] == [(saved_id, rid, 1)]
    restarted_engine.dispose()


def test_weather_ok(client):
    r = client.get("/v1/weather")
    assert r.status_code == 200 and r.json()["description"] == "overcast"


def test_weather_down_returns_503(settings, service):
    def boom(req):
        raise httpx.ConnectTimeout("timeout", request=req)

    app = create_app(settings, service, weather_with(boom))
    r = TestClient(app).get("/v1/weather")
    assert r.status_code == 503 and r.json()["error"]["code"] == "weather_service_unavailable"


def test_weather_stale_cache_when_upstream_fails():
    calls = {"n": 0}

    def flaky(req):
        calls["n"] += 1
        if calls["n"] == 1:
            return httpx.Response(200, json=OK_JSON)
        return httpx.Response(500)

    w = weather_with(flaky)
    w.cache_ttl_s = 0  # force a refresh on the second call
    assert not w.current().stale
    assert w.current().stale

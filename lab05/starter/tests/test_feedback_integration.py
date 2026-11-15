"""Bao04: independent R1/R2 checks, including disk persistence and API auth."""

import json
import sqlite3
import subprocess
import sys
from datetime import datetime, timezone

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, select

from assistant_api.db import Feedback, Repository, init_db, make_engine
from assistant_api.main import create_app


@pytest.fixture
def feedback_repo():
    engine = make_engine("sqlite://")
    init_db(engine)
    yield Repository(engine, "integration-test-salt")
    engine.dispose()


@pytest.fixture
def feedback_client(settings, service, feedback_repo):
    config = settings.model_copy(update={"api_admin_key": "integration-admin"})
    with TestClient(create_app(config, service, repo=feedback_repo)) as client:
        yield client


@pytest.fixture
def seeded_feedback(feedback_repo):
    # Insert timestamps out of order: ordering by id would give the wrong result.
    # Seed directly so a broken R1 cannot hide failures in R2.
    for day in [3, 1, 2]:
        request_id = f"request-{day}"
        feedback_repo.record_interaction("session", request_id, "fee", None, True, False, 2.0)
        with Session(feedback_repo.engine) as db:
            db.add(
                Feedback(
                    request_id=request_id,
                    rating=-1,
                    comment=f"day {day}",
                    created_at=datetime(2026, 1, day, tzinfo=timezone.utc),
                )
            )
            db.commit()
    return feedback_repo


@pytest.mark.parametrize("rating", [-1, 0, 1])
def test_r1_api_saves_each_valid_rating(feedback_client, feedback_repo, rating):
    request_id = feedback_client.post("/v1/chat", json={"message": "hi"}).json()["request_id"]
    payload = {"request_id": request_id, "rating": rating, "comment": "Phản hồi O'Brien"}
    response = feedback_client.post("/v1/feedback", json=payload)
    assert response.status_code == 201
    saved = response.json()
    assert saved.items() >= payload.items()
    assert isinstance(saved["id"], int)
    assert datetime.fromisoformat(saved["created_at"])
    # Query independently of R2 to prove the transaction was committed.
    with Session(feedback_repo.engine) as db:
        row = db.exec(select(Feedback)).one()
        assert (row.id, row.request_id, row.rating, row.comment) == (
            saved["id"],
            request_id,
            rating,
            payload["comment"],
        )


def test_r1_unknown_request_returns_404_without_writing(feedback_client, feedback_repo):
    response = feedback_client.post("/v1/feedback", json={"request_id": "missing", "rating": 1})
    assert response.status_code == 404
    assert response.json() == {"error": {"code": "unknown_request_id", "message": "Unknown request id"}}
    with Session(feedback_repo.engine) as db:
        assert db.exec(select(Feedback)).all() == []


@pytest.mark.parametrize(
    "payload",
    [
        {"request_id": "missing", "rating": -2},
        {"request_id": "missing", "rating": 2},
        {"request_id": "", "rating": 1},
        {"request_id": "missing", "rating": 1, "comment": "x" * 501},
    ],
)
def test_r1_invalid_payload_returns_422_without_writing(feedback_client, feedback_repo, payload):
    response = feedback_client.post("/v1/feedback", json=payload)
    assert response.status_code == 422
    assert response.json()["error"]["code"] == "invalid_request"
    with Session(feedback_repo.engine) as db:
        assert db.exec(select(Feedback)).all() == []


def test_r1_commit_survives_engine_close_and_new_process(tmp_path):
    path = tmp_path / "assistant.db"
    engine = make_engine(f"sqlite:///{path}")
    init_db(engine)
    repo = Repository(engine, "integration-test-salt")
    try:
        repo.record_interaction("session", "persisted", "fee", None, True, False, 1.0)
        saved = repo.add_feedback("persisted", -1, "O'Brien")
        assert saved is not None and saved.id is not None
        expected = [saved.id, "persisted", -1, "O'Brien"]
    finally:
        engine.dispose()
    # A fresh Python process reads the SQLite file, independent of R2 and ORM state.
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            "import json, sqlite3, sys; "
            "con = sqlite3.connect(sys.argv[1]); "
            "print(json.dumps(con.execute('SELECT id, request_id, rating, comment FROM feedback').fetchall())); "
            "con.close()",
            str(path),
        ],
        check=True,
        capture_output=True,
        text=True,
        timeout=10,
    )
    assert json.loads(result.stdout) == [expected]


def test_r2_repository_empty(feedback_repo):
    assert feedback_repo.list_feedback() == []


@pytest.mark.parametrize(
    "limit, expected",
    [
        (0, []),
        (1, ["request-3"]),
        (2, ["request-3", "request-2"]),
        (100, ["request-3", "request-2", "request-1"]),
    ],
)
def test_r2_repository_orders_by_timestamp_and_limits(seeded_feedback, limit, expected):
    rows = seeded_feedback.list_feedback(limit)
    assert isinstance(rows, list)
    assert [row.request_id for row in rows] == expected
    assert all(row.comment is not None for row in rows)  # accessible after the Session closes


@pytest.mark.parametrize("headers", [{}, {"X-API-Key": "wrong-key"}])
def test_r2_api_rejects_missing_or_wrong_key(feedback_client, headers):
    response = feedback_client.get("/v1/feedback", headers=headers)
    assert response.status_code == 401
    assert response.json()["error"]["code"] == "missing_or_invalid_api_key"


def test_r2_api_accepts_valid_key_with_empty_database(feedback_client):
    response = feedback_client.get("/v1/feedback", headers={"X-API-Key": "integration-admin"})
    assert response.status_code == 200 and response.json() == []


def test_r2_api_limits_and_serializes_without_r1(feedback_client, seeded_feedback):
    response = feedback_client.get("/v1/feedback?limit=2", headers={"X-API-Key": "integration-admin"})
    assert response.status_code == 200
    rows = response.json()
    assert [row["request_id"] for row in rows] == ["request-3", "request-2"]
    assert rows[0]["rating"] == -1 and rows[0]["comment"] == "day 3"
    assert rows[0]["created_at"] > rows[1]["created_at"]


def test_r1_r2_api_persists_after_application_and_engine_restart(tmp_path, settings, service):
    path = tmp_path / "assistant.db"
    config = settings.model_copy(update={"api_admin_key": "integration-admin"})
    first_engine = make_engine(f"sqlite:///{path}")
    init_db(first_engine)
    first_repo = Repository(first_engine, "integration-test-salt")
    try:
        with TestClient(create_app(config, service, repo=first_repo)) as client:
            request_id = client.post("/v1/chat", json={"message": "hi"}).json()["request_id"]
            response = client.post("/v1/feedback", json={"request_id": request_id, "rating": 0})
            assert response.status_code == 201
            saved = response.json()
    finally:
        first_engine.dispose()
    # New app and connection pool, using only the same database file.
    second_engine = make_engine(f"sqlite:///{path}")
    init_db(second_engine)
    second_repo = Repository(second_engine, "integration-test-salt")
    try:
        with TestClient(create_app(config, service, repo=second_repo)) as client:
            response = client.get("/v1/feedback", headers={"X-API-Key": "integration-admin"})
            assert response.status_code == 200
            assert response.json() == [saved]
    finally:
        second_engine.dispose()
    with sqlite3.connect(path) as db:
        assert db.execute("SELECT COUNT(*) FROM feedback").fetchone()[0] == 1

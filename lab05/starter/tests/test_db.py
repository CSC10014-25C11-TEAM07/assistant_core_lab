from datetime import datetime, timezone

from sqlmodel import Session, select

from assistant_api.db import ChatSession, Feedback, Interaction, Repository, hash_session, init_db, make_engine


def make_repo():
    engine = make_engine("sqlite://")
    init_db(engine)
    return Repository(engine, "salt"), engine


def test_session_id_is_hashed():
    repo, engine = make_repo()
    repo.record_interaction("student-42", "r1", "fee", None, True, False, 3.0)
    with Session(engine) as db:
        s = db.exec(select(ChatSession)).one()
    assert s.id == hash_session("student-42", "salt") and "student-42" not in s.id


def test_one_session_many_interactions():
    repo, engine = make_repo()
    for i in range(3):
        repo.record_interaction("s", f"r{i}", "rule", "H26-5.3", True, False, 10.0)
    with Session(engine) as db:
        assert len(db.exec(select(ChatSession)).all()) == 1
        assert len(db.exec(select(Interaction)).all()) == 3


def test_feedback_requires_existing_interaction():
    repo, _ = make_repo()
    assert repo.add_feedback("missing", 1, None) is None
    repo.record_interaction("s", "r1", "fee", None, True, False, 1.0)
    assert repo.add_feedback("r1", -1, "wrong fee").id == 1


def test_feedback_is_newest_first_and_limited():
    repo, engine = make_repo()
    repo.record_interaction("s", "r1", "fee", None, True, False, 1.0)
    # Insert out of chronological order so sorting by insertion ID would fail.
    with Session(engine) as db:
        for day in (3, 1, 2):
            db.add(Feedback(request_id="r1", rating=1, created_at=datetime(2026, 1, day, tzinfo=timezone.utc)))
        db.commit()
    assert [fb.created_at.day for fb in repo.list_feedback(limit=2)] == [3, 2]
    assert len(repo.list_feedback()) == 3
    assert repo.list_feedback(limit=0) == []

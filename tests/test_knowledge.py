from pathlib import Path

import pytest

from assistant_core.errors import DataError
from assistant_core.knowledge import Handbook, OfficeDirectory

DATA_DIR = Path(__file__).resolve().parents[1] / "data"


@pytest.fixture
def offices() -> OfficeDirectory:
    return OfficeDirectory.from_csv(DATA_DIR / "offices.csv")


@pytest.fixture
def handbook() -> Handbook:
    return Handbook.from_json(DATA_DIR / "handbook.json")


# ---------- Office: found / not found ----------
def test_find_office_library(offices):
    office = offices.find("where is the library")
    assert office is not None
    assert (office.name, office.room, office.hours) == ("Library", "B.201", "Mon-Sat 07:00-20:00")


def test_find_office_is_case_insensitive(offices):
    assert offices.find("WHERE IS THE IT HELPDESK?").room == "E.005"


def test_find_office_not_found(offices):
    assert offices.find("where is the cafeteria") is None


def test_office_names(offices):
    assert offices.names == {"training office", "student affairs", "library", "it helpdesk"}


# ---------- Handbook: found / not found ----------
def test_search_thesis_matches_monolith(handbook):
    # characterisation: monolith returned source H26-5.3 for this question
    rule = handbook.search("can I register my thesis with 118 credits")
    assert rule is not None
    assert rule.id == "H26-5.3"
    assert rule.title == "Thesis registration"


def test_search_exam_absence(handbook):
    assert handbook.search("what if I am absent from the final exam").id == "H26-7.2"


def test_search_no_match_returns_none(handbook):
    assert handbook.search("zzzz qqqq") is None


def test_search_ignores_short_words(handbook):
    assert handbook.search("is it a to of") is None


# ---------- Data errors ----------
def test_offices_file_missing(tmp_path):
    with pytest.raises(DataError, match="not found"):
        OfficeDirectory.from_csv(tmp_path / "nope.csv")


def test_offices_missing_column(tmp_path):
    f = tmp_path / "offices.csv"
    f.write_text("name,room\nLibrary,B.201\n", encoding="utf-8")
    with pytest.raises(DataError, match="missing column"):
        OfficeDirectory.from_csv(f)


def test_offices_incomplete_row(tmp_path):
    f = tmp_path / "offices.csv"
    f.write_text("name,room,hours\nLibrary,B.201\n", encoding="utf-8")
    with pytest.raises(DataError, match="incomplete"):
        OfficeDirectory.from_csv(f)


def test_handbook_file_missing(tmp_path):
    with pytest.raises(DataError, match="not found"):
        Handbook.from_json(tmp_path / "nope.json")


def test_handbook_invalid_json(tmp_path):
    f = tmp_path / "handbook.json"
    f.write_text("{not json", encoding="utf-8")
    with pytest.raises(DataError, match="not valid JSON"):
        Handbook.from_json(f)


def test_handbook_not_a_list(tmp_path):
    f = tmp_path / "handbook.json"
    f.write_text('{"id": "x"}', encoding="utf-8")
    with pytest.raises(DataError, match="JSON list"):
        Handbook.from_json(f)


def test_handbook_rule_missing_key(tmp_path):
    f = tmp_path / "handbook.json"
    f.write_text('[{"id": "H1", "title": "T"}]', encoding="utf-8")
    with pytest.raises(DataError, match="malformed"):
        Handbook.from_json(f)

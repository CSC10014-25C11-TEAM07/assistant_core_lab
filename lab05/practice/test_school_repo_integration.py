"""Bao04: edge cases beyond the five supplied D1-D3 acceptance tests."""

import sqlite3
from pathlib import Path

import pytest
import school_repo as repo

SQL = (Path(__file__).parent / "school.sql").read_text(encoding="utf-8")


@pytest.fixture
def con():
    connection = sqlite3.connect(":memory:")
    connection.executescript(SQL)
    yield connection
    connection.close()


@pytest.mark.parametrize("name", ["O'Brien", "x', 1, 'CS'); DROP TABLE students;--"])
def test_add_student_commits_and_preserves_input(tmp_path, name):
    path = tmp_path / "school.db"
    writer = sqlite3.connect(path)
    reader = sqlite3.connect(path)
    program = "CS' OR 1=1--"
    try:
        writer.executescript(SQL)
        new_id = repo.add_student(writer, name, 2, program)
        assert isinstance(new_id, int)
        # A different connection cannot see an uncommitted INSERT.
        assert reader.execute("SELECT name, year, program FROM students WHERE id = ?", (new_id,)).fetchone() == (
            name,
            2,
            program,
        )
        assert reader.execute("SELECT COUNT(*) FROM students").fetchone()[0] == 9
    finally:
        reader.close()
        writer.close()


def test_program_lookup_treats_injection_as_data(con):
    assert repo.students_in_program(con, "CS' OR 1=1--") == []


def test_average_with_only_null_grades(con):
    con.execute("UPDATE enrollments SET grade = NULL WHERE course_code = ?", ("CSC10014",))
    assert repo.average_grade(con, "CSC10014") is None


@pytest.mark.parametrize("grades, expected", [([0.0, None, 8.0, 8.0], 5.33), ([0.0] * 4, 0.0)])
def test_average_ignores_null_but_includes_zero_and_rounds(con, grades, expected):
    for student_id, grade in zip([2, 3, 4, 7], grades, strict=True):
        con.execute(
            "UPDATE enrollments SET grade = ? WHERE student_id = ? AND course_code = ?",
            (grade, student_id, "CSC10004"),
        )
    assert repo.average_grade(con, "CSC10004") == expected


def test_average_course_code_treats_injection_as_data(con):
    assert repo.average_grade(con, "CSC10004' OR 1=1--") is None


@pytest.mark.parametrize("student_id", [999, "2 OR 1=1"])
def test_transcript_missing_or_injected_id_returns_empty(con, student_id):
    assert repo.transcript(con, student_id) == []


def test_transcript_keeps_different_courses_with_the_same_title(con):
    con.execute("INSERT INTO courses VALUES (?, ?, ?)", ("TEST001", "Calculus 1", 2))
    con.execute("INSERT INTO enrollments VALUES (?, ?, ?)", (1, "TEST001", None))
    rows = repo.transcript(con, 1)
    assert len(rows) == 3
    assert rows[-1] == ("Fundamentals of Programming", 4, 8.5)
    assert set(rows[:2]) == {("Calculus 1", 3, 6.0), ("Calculus 1", 2, None)}

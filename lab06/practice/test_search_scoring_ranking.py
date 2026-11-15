"""Acceptance tests for S2–S3 Scoring and Ranking in Mini Search.

Author: Tran Gia Bao (giabao1001 / Bao04)
Role: Assigned owner for S2–S3 (scoring & ranking).

These tests isolate and rigorously verify:
1. Score accumulation across multiple matching query tokens.
2. Descending score ordering.
3. Ascending document-ID alphabetical tie-breaking for equal scores.
4. Top-k limiting behavior (including k=0, k=1, k > matches).
5. Exclusion of zero-score documents.
6. Non-mutating and idempotent query execution.
7. Independent execution using synthetic mock indices (ensuring
   S2–S3 correctness is evaluated without coupling to S1).
"""

from __future__ import annotations

import copy

import pytest
from mini_search import DOCS, build_index, search


def test_isolated_score_accumulation():
    """Verify that every matching query token increments the document's score by 1."""
    synthetic_index = {
        "network": {"DOC_A", "DOC_B"},
        "protocol": {"DOC_A"},
        "routing": {"DOC_A", "DOC_C"},
    }
    # Query with 3 matching tokens for DOC_A, 1 for DOC_B, 1 for DOC_C
    results = search(synthetic_index, "network protocol routing", k=10)
    scores = dict(results)

    assert scores["DOC_A"] == 3
    assert scores["DOC_B"] == 1
    assert scores["DOC_C"] == 1


def test_descending_score_ordering():
    """Verify results are sorted strictly in descending order of score."""
    synthetic_index = {
        "term1": {"D_LOW", "D_MID", "D_HIGH"},
        "term2": {"D_MID", "D_HIGH"},
        "term3": {"D_HIGH"},
    }
    results = search(synthetic_index, "term1 term2 term3", k=5)

    assert [doc_id for doc_id, _ in results] == ["D_HIGH", "D_MID", "D_LOW"]
    assert [score for _, score in results] == [3, 2, 1]


def test_ascending_doc_id_tie_breaking():
    """Verify that when scores are identical, ties are broken alphabetically by doc_id."""
    synthetic_index = {
        "shared": {"DOC_Z", "DOC_A", "DOC_M", "DOC_B"},
    }
    results = search(synthetic_index, "shared", k=10)

    # All have score 1; order must be strictly alphabetical
    assert results == [
        ("DOC_A", 1),
        ("DOC_B", 1),
        ("DOC_M", 1),
        ("DOC_Z", 1),
    ]


def test_combined_score_and_tie_breaking():
    """Verify descending score primary key and ascending doc_id secondary key."""
    synthetic_index = {
        "apple": {"D3", "D1", "D2", "D4"},
        "banana": {"D3", "D2"},
        "cherry": {"D4"},
    }
    # D3: apple + banana = 2
    # D2: apple + banana = 2
    # D4: apple + cherry = 2
    # D1: apple = 1
    # For score 2: tie between D2, D3, D4 -> alphabetical: D2, D3, D4
    # For score 1: D1
    results = search(synthetic_index, "apple banana cherry", k=10)

    assert results == [
        ("D2", 2),
        ("D3", 2),
        ("D4", 2),
        ("D1", 1),
    ]


@pytest.mark.parametrize("k, expected_len", [(0, 0), (1, 1), (2, 2), (3, 3), (10, 3)])
def test_top_k_parameter_bounds(k, expected_len):
    """Verify top-k bounds when k is 0, 1, exact count, or exceeds available matches."""
    synthetic_index = {
        "sample": {"D1", "D2", "D3"},
    }
    results = search(synthetic_index, "sample", k=k)
    assert len(results) == expected_len


def test_zero_score_documents_excluded():
    """Verify documents with 0 matching tokens are never returned."""
    synthetic_index = {
        "science": {"D1"},
        "history": {"D2"},
        "art": {"D3"},
    }
    results = search(synthetic_index, "science", k=10)
    returned_ids = {doc_id for doc_id, _ in results}

    assert "D1" in returned_ids
    assert "D2" not in returned_ids
    assert "D3" not in returned_ids
    assert len(results) == 1


def test_empty_query_and_stop_words_only():
    """Verify queries with empty string or only stop words return an empty list."""
    synthetic_index = {
        "thesis": {"D1"},
        "credits": {"D1", "D2"},
    }
    assert search(synthetic_index, "") == []
    assert search(synthetic_index, "   ") == []
    assert search(synthetic_index, "the a an in at to") == []


def test_empty_index():
    """Verify searching an empty index returns an empty list without raising."""
    assert search({}, "query text") == []


def test_search_does_not_mutate_index():
    """Verify that search is read-only and does not mutate the index structure."""
    synthetic_index = {
        "words": {"D1", "D2"},
        "test": {"D2"},
    }
    backup = copy.deepcopy(synthetic_index)

    _ = search(synthetic_index, "words test", k=5)
    assert synthetic_index == backup


def test_end_to_end_with_official_docs():
    """Verify search on the official DOCS corpus produces expected ranking."""
    idx = build_index(DOCS)

    # Query with multiple keywords
    hits = search(idx, "Students may borrow library books for days", k=4)
    # D4 has: borrow, library, books, days -> 4 matches
    assert hits[0][0] == "D4"
    assert hits[0][1] >= 4

    # Query matching D1 and D2
    hits_credits = search(idx, "credits", k=4)
    # Both D1 and D2 have 'credits' -> tie at score 1, D1 should come before D2
    assert hits_credits[0] == ("D1", 1)
    assert hits_credits[1] == ("D2", 1)

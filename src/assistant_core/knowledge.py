"""Knowledge sources: office directory (CSV) and student handbook (JSON)."""

from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from pathlib import Path

from assistant_core.errors import DataError

# Monolith only counted words longer than 3 characters when searching rules.
MIN_KEYWORD_LENGTH = 3


@dataclass(frozen=True)
class Office:
    name: str
    room: str
    hours: str


@dataclass(frozen=True)
class Rule:
    id: str
    title: str
    text: str


class OfficeDirectory:
    """Office lookup loaded once from a CSV file (columns: name, room, hours)."""

    def __init__(self, offices: dict[str, Office]):
        self._offices = offices

    @classmethod
    def from_csv(cls, path: Path) -> OfficeDirectory:
        try:
            with path.open(encoding="utf-8", newline="") as f:
                rows = list(csv.DictReader(f))
        except FileNotFoundError as exc:
            raise DataError(f"office file not found: {path}") from exc
        except (OSError, UnicodeDecodeError) as exc:
            raise DataError(f"cannot read office file {path}: {exc}") from exc

        offices: dict[str, Office] = {}
        for row in rows:
            try:
                name, room, hours = row["name"], row["room"], row["hours"]
            except KeyError as exc:
                raise DataError(f"office file {path} is missing column {exc}") from exc
            if not name or not name.strip() or room is None or hours is None:
                raise DataError(f"office file {path} has an incomplete row: {row}")
            offices[name.lower()] = Office(name, room, hours)

        if not offices:
            raise DataError(f"office file has no data: {path}")
        return cls(offices)

    @property
    def names(self) -> set[str]:
        return set(self._offices)

    def find(self, text: str) -> Office | None:
        t = text.lower()
        return next((o for name, o in self._offices.items() if name in t), None)


class Handbook:
    """Handbook rules loaded once from a JSON file, with keyword search."""

    def __init__(self, rules: list[Rule]):
        self._rules = rules

    @classmethod
    def from_json(cls, path: Path) -> Handbook:
        try:
            raw = json.loads(path.read_text(encoding="utf-8"))
        except FileNotFoundError as exc:
            raise DataError(f"handbook file not found: {path}") from exc
        except json.JSONDecodeError as exc:
            raise DataError(f"handbook file {path} is not valid JSON: {exc}") from exc
        except (OSError, UnicodeDecodeError) as exc:
            raise DataError(f"cannot read handbook file {path}: {exc}") from exc

        if not isinstance(raw, list):
            raise DataError(f"handbook file {path} must contain a JSON list")
        try:
            rules = [Rule(id=item["id"], title=item["title"], text=item["text"]) for item in raw]
        except (KeyError, TypeError) as exc:
            raise DataError(f"handbook file {path} has a malformed rule: {exc!r}") from exc
        return cls(rules)

    def search(self, query: str) -> Rule | None:
        """Return the rule sharing the most keywords with the query (None if no overlap)."""
        words = [w for w in query.lower().split() if len(w) > MIN_KEYWORD_LENGTH]
        best: Rule | None = None
        best_score = 0
        for rule in self._rules:
            text = rule.text.lower()
            score = sum(1 for w in words if w in text)
            if score > best_score:  # strict ">" keeps the first rule on ties, like the monolith
                best, best_score = rule, score
        return best

"""CLI:  python -m assistant_core "tuition for 18 credits and 2 retake" """

from __future__ import annotations

import sys
from typing import Any

from pydantic import ValidationError
from fastapi import FastAPI, HTTPException

from assistant_core.config import load_settings
from assistant_core.errors import AssistantError
from assistant_core.logging_setup import setup_logging
from assistant_core.models import Message
from assistant_core.service import build_service
from assistant_core.knowledge import OfficeDirectory 


app = FastAPI(title="Assistant Core API")
service = build_service(load_settings())

def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    try:
        settings = load_settings()
        setup_logging(settings.log_level)
        service = build_service(settings)
    except AssistantError as exc:
        print(f"Startup error: {exc}", file=sys.stderr)
        return 2
    if not argv:
        print('Usage: python -m assistant_core "your question"')
        return 1
    try:
        resp = service.handle(Message(text=" ".join(argv)))
    except ValidationError:
        print("Please type a question (1–2000 characters).")
        return 1
    print(resp.answer)
    for src in resp.sources:
        print(f"  source: {src.id} — {src.title}")
    return 0

@app.get("/v1/offices")
def list_offices() -> list[dict[str, Any]]:
    """Return a list of all offices in the directory, sorted by name."""
    return [o.__dict__ for o in service.offices.all()]

if __name__ == "__main__":
    raise SystemExit(main())

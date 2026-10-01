from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .model import Issue


def validate_schema(events: list[dict[str, Any]], schema_path: Path) -> list[Issue]:
    try:
        from jsonschema import Draft202012Validator, FormatChecker
    except ImportError:
        return [Issue("DEPENDENCY_JSONSCHEMA", "WARNING", "jsonschema não instalado; camada JSON Schema não executada")]

    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    issues: list[Issue] = []
    for event in events:
        for error in sorted(validator.iter_errors(event), key=lambda e: list(e.path)):
            issues.append(Issue(
                "SCHEMA_INVALID", "ERROR", error.message,
                event_id=event.get("event_id"),
                stream_id=event.get("stream", {}).get("stream_id"),
                path="/" + "/".join(map(str, error.path)),
            ))
    return issues


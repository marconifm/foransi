from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .model import Issue

MAX_SAFE_INTEGER = 9_007_199_254_740_991


class DuplicateKeyError(ValueError):
    pass


def _pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in pairs:
        if key in out:
            raise DuplicateKeyError(f"chave JSON duplicada: {key}")
        out[key] = value
    return out


def _int(value: str) -> int:
    parsed = int(value)
    if abs(parsed) > MAX_SAFE_INTEGER:
        raise ValueError("inteiro JSON fora do intervalo seguro de I-JSON")
    return parsed


def _constant(value: str) -> None:
    raise ValueError(f"constante JSON não finita proibida: {value}")


def parse_line(text: str) -> dict[str, Any]:
    value = json.loads(
        text,
        object_pairs_hook=_pairs,
        parse_int=_int,
        parse_constant=_constant,
    )
    if not isinstance(value, dict):
        raise ValueError("cada linha JSONL deve conter um objeto")
    return value


def load_jsonl(path: Path) -> tuple[list[dict[str, Any]], list[Issue]]:
    events: list[dict[str, Any]] = []
    issues: list[Issue] = []
    with path.open("r", encoding="utf-8", errors="strict") as handle:
        for line_number, raw in enumerate(handle, 1):
            text = raw.rstrip("\n\r")
            if not text:
                issues.append(Issue("EMPTY_LINE", "ERROR", "linha vazia no JSONL", line=line_number))
                continue
            try:
                events.append(parse_line(text))
            except (json.JSONDecodeError, ValueError) as exc:
                issues.append(Issue("JSON_PARSE_ERROR", "ERROR", str(exc), line=line_number))
    return events, issues


from __future__ import annotations

import copy
import hashlib
from typing import Any

from .model import Issue


def canonical_bytes(value: Any) -> bytes:
    try:
        import rfc8785
    except ImportError as exc:
        raise RuntimeError("dependência rfc8785 não instalada") from exc
    return rfc8785.dumps(value)


def hashable_event(event: dict[str, Any]) -> dict[str, Any]:
    value = copy.deepcopy(event)
    integrity = value.get("integrity", {})
    integrity.pop("event_hash", None)
    integrity.pop("signature", None)
    return value


def calculate_event_hash(event: dict[str, Any]) -> str:
    return hashlib.sha256(canonical_bytes(hashable_event(event))).hexdigest()


def validate_hashes(events: list[dict[str, Any]]) -> list[Issue]:
    try:
        canonical_bytes({"probe": True})
    except RuntimeError as exc:
        return [Issue("DEPENDENCY_RFC8785", "WARNING", str(exc))]
    issues: list[Issue] = []
    for event in events:
        expected = event.get("integrity", {}).get("event_hash")
        actual = calculate_event_hash(event)
        if expected != actual:
            issues.append(Issue(
                "EVENT_HASH_MISMATCH", "ERROR", f"hash esperado {expected}; calculado {actual}",
                event_id=event.get("event_id"), stream_id=event.get("stream", {}).get("stream_id"),
            ))
    return issues


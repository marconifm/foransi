from __future__ import annotations

from collections import defaultdict
from typing import Any

from .model import Issue


def validate_manifests(events: list[dict[str, Any]]) -> tuple[list[Issue], bool]:
    issues: list[Issue] = []
    streams: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for event in events:
        streams[event.get("stream", {}).get("stream_id")].append(event)
    manifests = [e for e in events if e.get("event_type") == "manifest.sealed"]
    verified = False
    for manifest in manifests:
        for summary in manifest.get("payload", {}).get("streams", []):
            stream_id = summary["stream_id"]
            items = sorted(streams.get(stream_id, []), key=lambda e: e.get("stream_sequence", 0))
            if not items:
                issues.append(Issue("MANIFEST_STREAM_NOT_FOUND", "ERROR", "stream declarado não existe", event_id=manifest.get("event_id"), stream_id=stream_id))
                continue
            expected = {
                "first_sequence": items[0]["stream_sequence"],
                "last_sequence": items[-1]["stream_sequence"],
                "event_count": len(items),
                "first_hash": items[0]["integrity"]["event_hash"],
                "last_hash": items[-1]["integrity"]["event_hash"],
            }
            for field, value in expected.items():
                if summary.get(field) != value:
                    issues.append(Issue("MANIFEST_STREAM_MISMATCH", "ERROR", f"{field} diverge", event_id=manifest.get("event_id"), stream_id=stream_id))
        ledger_items = sorted(streams.get("STR-LEDGER-01", []), key=lambda e: e.get("stream_sequence", 0))
        if ledger_items and manifest["payload"].get("ledger_hash") != ledger_items[-1]["integrity"]["event_hash"]:
            issues.append(Issue("MANIFEST_LEDGER_HASH", "ERROR", "ledger_hash diverge do último hash conhecido", event_id=manifest.get("event_id")))
        verified = not any(i.severity == "ERROR" and i.event_id == manifest.get("event_id") for i in issues)
    return issues, verified


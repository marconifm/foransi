from __future__ import annotations

from typing import Any

from .model import Issue


def validate_ledger(events: list[dict[str, Any]], require_complete: bool = False) -> tuple[list[Issue], int]:
    issues: list[Issue] = []
    by_id = {event.get("event_id"): event for event in events}
    ledger = [event for event in events if event.get("event_type") == "ledger.event.accepted"]
    ledger.sort(key=lambda e: e.get("payload", {}).get("ledger_sequence", 0))
    accepted: set[str] = set()
    for expected, event in enumerate(ledger, 1):
        payload = event["payload"]
        if payload.get("ledger_sequence") != expected:
            issues.append(Issue("LEDGER_SEQUENCE_GAP", "ERROR", f"esperado {expected}", event_id=event.get("event_id")))
        target_id = payload.get("source_event_id")
        target = by_id.get(target_id)
        if not target:
            issues.append(Issue("LEDGER_TARGET_NOT_FOUND", "ERROR", "evento referenciado não existe", event_id=event.get("event_id")))
            continue
        if target_id in accepted:
            issues.append(Issue("LEDGER_DUPLICATE_ACCEPTANCE", "ERROR", "evento aceito mais de uma vez", event_id=event.get("event_id")))
        accepted.add(target_id)
        checks = {
            "source_stream_id": target.get("stream", {}).get("stream_id"),
            "source_stream_sequence": target.get("stream_sequence"),
            "source_event_hash": target.get("integrity", {}).get("event_hash"),
        }
        for field, expected_value in checks.items():
            if payload.get(field) != expected_value:
                issues.append(Issue("LEDGER_REFERENCE_MISMATCH", "ERROR", f"{field} diverge do evento de origem", event_id=event.get("event_id")))

    if require_complete:
        excluded_types = {"ledger.event.accepted", "manifest.sealed"}
        official = {e.get("event_id") for e in events if e.get("event_type") not in excluded_types}
        missing = official - accepted
        for event_id in sorted(missing):
            issues.append(Issue("LEDGER_EVENT_MISSING", "ERROR", "evento oficial ausente do ledger", event_id=event_id))
    return issues, len(ledger)


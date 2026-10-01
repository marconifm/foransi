from __future__ import annotations

from typing import Any

from .model import Issue


def validate_semantics(events: list[dict[str, Any]]) -> list[Issue]:
    issues: list[Issue] = []
    by_id = {event.get("event_id"): event for event in events}
    starts: dict[str, dict[str, Any]] = {}
    for event in events:
        event_id = event.get("event_id")
        stream_id = event.get("stream", {}).get("stream_id")
        cause = event.get("causation_id")
        if cause and cause not in by_id:
            issues.append(Issue("CAUSATION_NOT_FOUND", "ERROR", "causation_id não resolve", event_id=event_id, stream_id=stream_id))

        payload = event.get("payload", {})
        kind = event.get("event_type")
        if kind == "execution.step.started":
            starts[payload.get("evento_id")] = event
        elif kind == "execution.step.finished":
            start = starts.get(payload.get("evento_id"))
            if not start:
                issues.append(Issue("STEP_START_NOT_FOUND", "ERROR", "etapa finalizada sem início", event_id=event_id, stream_id=stream_id))
            else:
                begin = int(start["payload"]["inicio_monotonico_ns"])
                end = int(payload["fim_monotonico_ns"])
                expected = (end - begin) // 1_000_000
                if payload.get("duracao_ms") != expected:
                    issues.append(Issue("DURATION_MISMATCH", "ERROR", f"duracao_ms deveria ser {expected}", event_id=event_id, stream_id=stream_id))

        if kind == "record.corrected":
            target = payload.get("target_event_id")
            original = by_id.get(target)
            if not original:
                issues.append(Issue("CORRECTION_TARGET_NOT_FOUND", "ERROR", "evento corrigido não existe", event_id=event_id, stream_id=stream_id))
            elif original.get("integrity", {}).get("event_hash") != payload.get("target_event_hash"):
                issues.append(Issue("CORRECTION_HASH_MISMATCH", "ERROR", "hash do alvo da correção diverge", event_id=event_id, stream_id=stream_id))
    return issues


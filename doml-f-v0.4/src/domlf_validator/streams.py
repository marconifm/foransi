from __future__ import annotations

from collections import defaultdict
from typing import Any

from .model import Issue


def validate_streams(events: list[dict[str, Any]]) -> tuple[list[Issue], int]:
    issues: list[Issue] = []
    streams: dict[str, list[dict[str, Any]]] = defaultdict(list)
    event_ids: dict[str, str] = {}
    for event in events:
        event_id = event.get("event_id")
        stream = event.get("stream", {})
        stream_id = stream.get("stream_id")
        if not stream_id:
            continue
        streams[stream_id].append(event)
        if event_id in event_ids:
            issues.append(Issue("DUPLICATE_EVENT_ID", "ERROR", "event_id repetido", event_id=event_id, stream_id=stream_id))
        else:
            event_ids[event_id] = stream_id

    for stream_id, items in streams.items():
        items.sort(key=lambda e: e.get("stream_sequence", 0))
        identity = None
        previous_hash = None
        for expected_sequence, event in enumerate(items, 1):
            stream = event["stream"]
            current_identity = (stream.get("emitter_type"), stream.get("emitter_instance_id"), stream.get("host"), stream.get("boot_id"))
            identity = identity or current_identity
            if current_identity != identity:
                issues.append(Issue("STREAM_IDENTITY_CHANGED", "ERROR", "identidade do stream mudou", event_id=event.get("event_id"), stream_id=stream_id))
            if event.get("stream_sequence") != expected_sequence:
                issues.append(Issue("STREAM_SEQUENCE_GAP", "ERROR", f"esperado {expected_sequence}", event_id=event.get("event_id"), stream_id=stream_id))
            declared_previous = event.get("integrity", {}).get("previous_event_hash")
            if declared_previous != previous_hash:
                issues.append(Issue("STREAM_HASH_CHAIN", "ERROR", "previous_event_hash não corresponde ao evento anterior", event_id=event.get("event_id"), stream_id=stream_id))
            previous_hash = event.get("integrity", {}).get("event_hash")
    return issues, len(streams)


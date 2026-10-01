from __future__ import annotations

from pathlib import Path

from .canonical import validate_hashes
from .ledger import validate_ledger
from .manifest import validate_manifests
from .model import Report
from .parser import load_jsonl
from .schema import validate_schema
from .semantic import validate_semantics
from .streams import validate_streams


def audit(path: Path, schema_path: Path | None = None, verify_crypto: bool = True, require_complete_ledger: bool = False) -> Report:
    report = Report()
    events, issues = load_jsonl(path)
    report.issues.extend(issues)
    report.events_checked = len(events)
    if schema_path:
        report.issues.extend(validate_schema(events, schema_path))
    if verify_crypto:
        report.issues.extend(validate_hashes(events))
    stream_issues, report.streams_checked = validate_streams(events)
    report.issues.extend(stream_issues)
    report.issues.extend(validate_semantics(events))
    ledger_issues, report.ledger_entries = validate_ledger(events, require_complete_ledger)
    report.issues.extend(ledger_issues)
    manifest_issues, report.manifest_verified = validate_manifests(events)
    report.issues.extend(manifest_issues)
    report.evidence_checked = sum(e.get("event_type") == "evidence.registered" for e in events)
    return report


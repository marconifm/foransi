from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(slots=True)
class Issue:
    code: str
    severity: str
    message: str
    line: int | None = None
    event_id: str | None = None
    stream_id: str | None = None
    path: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {k: v for k, v in asdict(self).items() if v is not None}


@dataclass(slots=True)
class Report:
    issues: list[Issue] = field(default_factory=list)
    events_checked: int = 0
    streams_checked: int = 0
    ledger_entries: int = 0
    evidence_checked: int = 0
    manifest_verified: bool = False

    def add(self, issue: Issue) -> None:
        self.issues.append(issue)

    @property
    def errors(self) -> int:
        return sum(i.severity == "ERROR" for i in self.issues)

    @property
    def warnings(self) -> int:
        return sum(i.severity == "WARNING" for i in self.issues)

    @property
    def valid(self) -> bool:
        return self.errors == 0

    def to_dict(self) -> dict[str, Any]:
        return {
            "valid": self.valid,
            "errors": self.errors,
            "warnings": self.warnings,
            "events_checked": self.events_checked,
            "streams_checked": self.streams_checked,
            "ledger_entries": self.ledger_entries,
            "evidence_checked": self.evidence_checked,
            "manifest_verified": self.manifest_verified,
            "issues": [i.to_dict() for i in self.issues],
        }


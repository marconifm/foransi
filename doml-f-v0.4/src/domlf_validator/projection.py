from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


class ProjectionError(ValueError):
    pass


_MISSING = object()


def pointer(document: Any, path: str, current: Any = None) -> Any:
    if path.startswith("./"):
        value = current
        parts = path[2:].split("/")
    elif path.startswith("/"):
        value = document
        parts = path[1:].split("/")
    else:
        raise ProjectionError(f"JSON Pointer inválido: {path}")
    for raw in parts:
        key = raw.replace("~1", "/").replace("~0", "~")
        if isinstance(value, dict) and key in value:
            value = value[key]
        elif isinstance(value, list) and key.isdigit() and int(key) < len(value):
            value = value[int(key)]
        else:
            return _MISSING
    return value


def resolve(document: dict[str, Any], spec: Any, current: Any = None) -> Any:
    if isinstance(spec, str):
        return pointer(document, spec, current)
    if isinstance(spec, dict) and "constant" in spec:
        return spec["constant"]
    return spec


@dataclass
class ProjectionState:
    tables: dict[str, dict[tuple[Any, ...], dict[str, Any]]] = field(default_factory=dict)

    def rows(self, table: str) -> list[dict[str, Any]]:
        return list(self.tables.get(table, {}).values())


class Projector:
    def __init__(self, mapping: dict[str, Any]):
        self.mapping = mapping
        self.state = ProjectionState()

    def apply(self, event: dict[str, Any]) -> None:
        event_type = event.get("event_type")
        config = self.mapping.get("events", {}).get(event_type)
        if not config:
            if self.mapping.get("unknown_event") == "reject":
                raise ProjectionError(f"evento sem projeção: {event_type}")
            return
        projections = config.get("projections")
        if projections:
            for projection in projections:
                self._apply_projection(event, projection)
            return
        dispatch = config.get("dispatch")
        if dispatch:
            selected = pointer(event, dispatch["pointer"])
            case = dispatch.get("cases", {}).get(selected)
            if not case:
                raise ProjectionError(f"dispatch sem caso para {selected}")
            projection = {
                "target": case["target"],
                "operation": config["operation"],
                "key": {case["id_field"]: "/payload/validacao_id"},
                "fields": dict(config.get("fields", {})),
                "provenance_profile": config.get("provenance_profile"),
            }
            projection["fields"][case["id_field"]] = projection["fields"].pop("validacao_id")
            self._apply_projection(event, projection)

    def _apply_projection(self, event: dict[str, Any], projection: dict[str, Any]) -> None:
        iterable = pointer(event, projection["iterate"]) if projection.get("iterate") else [None]
        if iterable is _MISSING or not isinstance(iterable, list):
            raise ProjectionError("iterate não resolveu para lista")
        for current in iterable:
            self._apply_row(event, projection, current)

    def _apply_row(self, event: dict[str, Any], projection: dict[str, Any], current: Any) -> None:
        table = projection["target"]
        operation = projection["operation"]
        row: dict[str, Any] = {}
        for field_name, source in projection.get("fields", {}).items():
            value = resolve(event, source, current)
            if value is not _MISSING:
                row[field_name] = value
        row.update(projection.get("constants", {}))

        profile_name = projection.get("provenance_profile")
        profile = self.mapping.get("provenance_profiles", {}).get(profile_name, {})
        for field_name, source in profile.items():
            value = resolve(event, source, current)
            if value is not _MISSING:
                row[field_name] = value

        table_store = self.state.tables.setdefault(table, {})
        key_fields = list(projection.get("key", {}))
        key_values = []
        for field_name, source in projection.get("key", {}).items():
            value = resolve(event, source, current)
            if value is _MISSING:
                value = row.get(field_name, _MISSING)
            if value is _MISSING:
                raise ProjectionError(f"chave ausente: {table}.{field_name}")
            key_values.append(value)
            row.setdefault(field_name, value)
        key = tuple(key_values)

        if operation == "finalize":
            if key not in table_store:
                raise ProjectionError(f"finalização sem criação: {table}{key}")
            target = table_store[key]
            for protected in projection.get("immutable_fields", []):
                if protected in row and protected in target and row[protected] != target[protected]:
                    raise ProjectionError(f"campo imutável alterado: {table}.{protected}")
            target.update(row)
            for field_name, derivation in projection.get("derived", {}).items():
                if derivation.get("function") == "monotonic_duration_ms":
                    start = int(target[derivation["start_field"]])
                    end = int(pointer(event, derivation["end_pointer"]))
                    target[field_name] = (end - start) // 1_000_000
            return

        if key in table_store:
            raise ProjectionError(f"chave duplicada: {table}{key}")
        table_store[key] = row


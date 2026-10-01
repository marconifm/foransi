from __future__ import annotations

import argparse
import json
from pathlib import Path

from .audit import audit


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="domlf-validate")
    parser.add_argument("jsonl", type=Path)
    parser.add_argument("--schema", type=Path)
    parser.add_argument("--skip-crypto", action="store_true", help="não recalcula JCS/hash")
    parser.add_argument("--require-complete-ledger", action="store_true")
    parser.add_argument("--json-report", type=Path)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    report = audit(args.jsonl, args.schema, not args.skip_crypto, args.require_complete_ledger)
    content = report.to_dict()
    if args.json_report:
        args.json_report.write_text(json.dumps(content, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(content, ensure_ascii=False, indent=2))
    return 0 if report.valid else 1


if __name__ == "__main__":
    raise SystemExit(main())


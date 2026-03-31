#!/usr/bin/env python3
import argparse
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="artifacts/reports/dependency-audit.md")
    args = parser.parse_args()
    p = Path(args.input)
    if not p.exists():
        raise FileNotFoundError(f"Missing audit file: {p}")
    content = p.read_text().lower()
    if "|" not in content:
        raise RuntimeError("Audit file has no table rows")
    if "deferred" in content:
        raise RuntimeError("Implementation blocked: deferred dependency present")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

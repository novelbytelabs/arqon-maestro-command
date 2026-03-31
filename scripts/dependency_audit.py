#!/usr/bin/env python3
import argparse
from pathlib import Path

TEST_LEVELS = ["unit", "integration", "e2e", "regression", "adversarial"]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="artifacts/reports/dependency-audit.md")
    args = parser.parse_args()
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    if not out.exists():
        lines = ["# Dependency Audit", "", "| Test Level | Dependency | Status | Notes |", "|---|---|---|---|"]
        for level in TEST_LEVELS:
            lines.append(f"| {level} | baseline-runtime | present_in_frozen_runtime | initial seed |")
        out.write_text("\n".join(lines) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

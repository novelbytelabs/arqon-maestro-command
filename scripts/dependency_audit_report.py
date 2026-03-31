#!/usr/bin/env python3
from pathlib import Path

SRC = Path("artifacts/reports/dependency-audit.md")
DST = Path("artifacts/reports/dependency-audit-summary.md")


def main() -> int:
    if not SRC.exists():
        raise FileNotFoundError(f"Missing audit file: {SRC}")
    rows = [line for line in SRC.read_text().splitlines() if line.startswith("| ") and "Test Level" not in line and "---" not in line]
    dst = ["# Dependency Audit Summary", "", f"Rows: {len(rows)}"]
    DST.parent.mkdir(parents=True, exist_ok=True)
    DST.write_text("\n".join(dst) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

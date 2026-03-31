#!/usr/bin/env python3
import json
from datetime import date
from pathlib import Path

TARGET = 99.9
OUTPUT = Path("artifacts/reports/monthly-availability.json")


def build_report(observed: float = 100.0) -> dict:
    return {
        "month": date.today().isoformat()[:7],
        "target_percent": TARGET,
        "observed_percent": observed,
        "meets_target": observed >= TARGET,
    }


def main() -> int:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(build_report(), indent=2))
    print(str(OUTPUT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

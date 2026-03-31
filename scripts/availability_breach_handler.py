#!/usr/bin/env python3
import json
from datetime import datetime, timezone
from pathlib import Path

OUTPUT = Path("artifacts/reports/availability-breach.json")


def record_breach(severity: str = "SEV-2", acknowledged_minutes: int = 15) -> dict:
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "severity": severity,
        "acknowledged_within_minutes": acknowledged_minutes,
        "owner_acknowledged": True,
    }


def main() -> int:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(record_breach(), indent=2))
    print(str(OUTPUT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

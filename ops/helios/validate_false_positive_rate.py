#!/usr/bin/env python3
import json
import sys
from pathlib import Path

MAX_FALSE_POSITIVE_RATE = 0.001


def validate_rate(value: float) -> bool:
    return value <= MAX_FALSE_POSITIVE_RATE


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_false_positive_rate.py <metrics-json>")
        return 2
    payload = json.loads(Path(sys.argv[1]).read_text())
    rate = float(payload.get("false_positive_rate", 1.0))
    ok = validate_rate(rate)
    print("PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

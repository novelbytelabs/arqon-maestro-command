#!/usr/bin/env python3
import json
import sys
from pathlib import Path

REQUIRED = {"audio_hash", "lane", "policy_outcome", "latency_ms", "timestamp"}


def validate_packet(packet: dict) -> bool:
    return REQUIRED.issubset(packet.keys())


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_evidence_schema.py <evidence-json>")
        return 2
    path = Path(sys.argv[1])
    packet = json.loads(path.read_text())
    ok = validate_packet(packet)
    print("PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

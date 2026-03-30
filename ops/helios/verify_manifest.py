#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

MANIFEST = Path("artifacts/manifests/parakeet-tdt_ctc-1.1b.manifest.json")


def sha256sum(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


if not MANIFEST.exists():
    raise SystemExit(f"FAIL: manifest not found: {MANIFEST}")

manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
required_provenance = [
    "adapter_type",
    "dataset_lineage",
    "license",
    "eval_results",
]
for key in required_provenance:
    if key not in manifest.get("provenance", {}):
        raise SystemExit(f"FAIL: missing provenance key: {key}")

artifacts = manifest.get("artifacts", [])
if not artifacts:
    raise SystemExit("FAIL: no artifacts listed")

for item in artifacts:
    path = Path(item["local"])
    if not path.exists():
        raise SystemExit(f"FAIL: missing artifact file: {path}")
    actual = sha256sum(path)
    if actual != item["sha256"]:
        raise SystemExit(f"FAIL: checksum mismatch for {path}")

print(f"PASS: verified {len(artifacts)} artifacts from {MANIFEST}")

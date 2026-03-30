#!/usr/bin/env python3
import hashlib
import json
import os
from pathlib import Path

from huggingface_hub import HfApi, hf_hub_download

MODEL_ID = "nvidia/parakeet-tdt_ctc-1.1b"
DEST = Path("artifacts/models/parakeet-tdt_ctc-1.1b")
MANIFEST = Path("artifacts/manifests/parakeet-tdt_ctc-1.1b.manifest.json")

REQUIRED_PATTERNS = [
    "*.nemo",
    "*.yaml",
    "*.json",
    "*.md",
    "*token*",
    "*vocab*",
    "*spm*",
]


def sha256sum(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


api = HfApi()
files = api.list_repo_files(MODEL_ID)

selected = []
for fn in files:
    l = fn.lower()
    if (
        l.endswith(".nemo")
        or l.endswith(".yaml")
        or l.endswith(".json")
        or l.endswith(".md")
        or "token" in l
        or "vocab" in l
        or "spm" in l
    ):
        selected.append(fn)

DEST.mkdir(parents=True, exist_ok=True)

entries = []
for remote_fn in sorted(set(selected)):
    local_path = Path(
        hf_hub_download(
            repo_id=MODEL_ID,
            filename=remote_fn,
            local_dir=str(DEST),
            local_dir_use_symlinks=False,
        )
    )
    entries.append(
        {
            "remote": remote_fn,
            "local": str(local_path),
            "size_bytes": local_path.stat().st_size,
            "sha256": sha256sum(local_path),
        }
    )

manifest = {
    "manifest_version": "1.0",
    "model_alias": "arqon-maestro-command",
    "base_model": {
        "id": MODEL_ID,
        "version": "hf-main",
    },
    "provenance": {
        "adapter_type": "none",
        "dataset_lineage": "TODO(dataset-lineage)",
        "license": "cc-by-4.0 (verify on model card)",
        "eval_results": "TODO(eval-results)",
    },
    "runtime_constraints": {
        "python": "3.10.19",
        "torch": "2.10.0",
        "numpy": "2.2.5",
        "protobuf": "4.25.8",
        "protoc": "29.3",
    },
    "required_patterns": REQUIRED_PATTERNS,
    "artifacts": entries,
}

MANIFEST.parent.mkdir(parents=True, exist_ok=True)
MANIFEST.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

print(f"Wrote manifest: {MANIFEST}")
print(f"Downloaded files: {len(entries)}")

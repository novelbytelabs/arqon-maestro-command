#!/usr/bin/env bash
set -euo pipefail

OUT="artifacts/reports/helios-baseline.md"
NOW="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

mkdir -p "$(dirname "$OUT")"

{
  echo "# Helios Baseline Snapshot"
  echo
  echo "Captured: $NOW"
  echo
  echo "## System"
  echo '```text'
  nvidia-smi | sed -n '1,15p'
  echo '```'
  echo
  echo "## Conda Environment"
  echo '```text'
  conda info --envs | sed -n '1,40p'
  echo '```'
  echo
  echo "## Core Toolchain"
  echo '```text'
  rustc --version || true
  cargo --version || true
  ./ops/helios/helios-run.sh python -V
  ./ops/helios/helios-run.sh protoc --version
  ./ops/helios/helios-run.sh python -m pip --version
  echo '```'
  echo
  echo "## Core Python Package Pins"
  echo '```text'
  ./ops/helios/helios-run.sh python -c "import numpy,torch,google.protobuf;print('numpy',numpy.__version__);print('torch',torch.__version__);print('protobuf',google.protobuf.__version__)"
  echo '```'
  echo
  echo "## Runtime Library Path"
  echo '```text'
  ./ops/helios/helios-run.sh python -c "import os;print(os.environ.get('LD_LIBRARY_PATH',''))"
  echo '```'
} > "$OUT"

echo "Wrote $OUT"

#!/usr/bin/env bash
set -euo pipefail

./ops/helios/capture_baseline.sh
./ops/helios/runtime_hygiene_gate.sh
./ops/helios/install_nemo_2_1.sh
./ops/helios/generate_contracts.sh
./ops/helios/helios-run.sh python ops/helios/download_parakeet_assets.py
./ops/helios/helios-run.sh python ops/helios/verify_manifest.py
./ops/helios/helios-run.sh python ops/helios/bridge_smoke_check.py
./ops/helios/helios-run.sh python ops/helios/audio_inference_smoke.py

echo "PASS: Helios compatibility-first bootstrap completed"

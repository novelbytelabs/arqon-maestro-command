#!/usr/bin/env bash
set -euo pipefail

CONSTRAINTS="ops/helios/constraints-helios.txt"

./ops/helios/helios-run.sh python -m pip install \
  --upgrade-strategy only-if-needed \
  --constraint "$CONSTRAINTS" \
  "nemo_toolkit[asr]==2.1.0"

./ops/helios/helios-run.sh python - <<'PY'
import numpy, torch
import google.protobuf

print('numpy', numpy.__version__)
print('torch', torch.__version__)
print('protobuf', google.protobuf.__version__)

assert numpy.__version__ == '2.2.5', 'numpy pin drifted'
assert torch.__version__.startswith('2.10.0'), 'torch pin drifted'
assert google.protobuf.__version__ == '4.25.8', 'protobuf pin drifted'
print('PASS: pinned core versions preserved')
PY

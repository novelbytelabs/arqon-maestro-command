# Model Start and Usage

This runbook explains how to start and validate the Command Lane model path in
frozen runtime.

## Prerequisites

- Runtime: `helios-gpu-118`
- No direct package installs in frozen runtime
- Model artifacts available under `artifacts/models/`

## Start/Validate Sequence

1. Generate contracts and run readiness smoke:

```bash
make helios-smoke
```

Expected artifact:

- `artifacts/reports/audio-inference-smoke.json`

2. Validate dependency completeness:

```bash
python3 scripts/dependency_audit.py
python3 scripts/dependency_audit_report.py
python3 scripts/validate_dependency_audit.py
```

3. Run test suites:

```bash
PYTHONPATH=. PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 pytest -q tests/unit tests/integration tests/e2e tests/regression tests/adversarial
```

## Minimal Local Usage Example

```bash
python3 - <<'PY'
from src.command_lane.api.commands import evaluate_command
print(evaluate_command({"transcript": "stop", "acoustic_confidence": 0.99, "authorized": True}))
PY
```

Expected behavior: deterministic terminal outcome (`granted`/`refused`/`escalated`).

## Operational Artifacts

- `artifacts/reports/audio-inference-smoke.json`
- `artifacts/reports/dependency-audit.md`
- `artifacts/reports/release-candidate-validation.md`
- `artifacts/reports/readiness-reproducibility.md`

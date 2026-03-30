# Quickstart: Implementation Readiness

## 1. Verify Frozen Runtime Readiness

Run:

```bash
make helios-smoke
```

Required artifact:
- `/home/irbsurfer/Projects/arqon/arqon-maestro-command/artifacts/reports/audio-inference-smoke.json`

## 2. Produce Dependency Completeness Audit

Create:
- `/home/irbsurfer/Projects/arqon/arqon-maestro-command/artifacts/reports/dependency-audit.md`

For each test level (unit/integration/e2e/regression/adversarial), list each
required dependency and status:
- `present_in_frozen_runtime`
- `provisioned_externally`
- `deferred`

**Rule**: If any dependency is `deferred`, implementation start is blocked.

## 3. Implementation Phases

- Phase A: dependency audit + environment readiness
- Phase B: command lane implementation
- Phase C: mandatory five test suites
- Phase D: CI merge gates

## 4. Merge Gate Checklist

- `make helios-smoke` PASS
- contract validation PASS
- evidence packet schema validation PASS
- unit PASS
- integration PASS
- e2e PASS
- regression PASS
- adversarial PASS
- dependency audit has zero `deferred`

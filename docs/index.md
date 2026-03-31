# Arqon Maestro Command Lane Docs

Arqon Maestro Command Lane is a control-first speech system for deterministic,
operator-safe command execution.

## First-Run Checklist (Every New AI/Dev Instance)

1. Read the constitution: `.specify/memory/constitution.md`.
2. Use frozen runtime env: `helios-gpu-118`.
3. Do not install dependencies in `helios-gpu-118`.
4. Run smoke gate:

```bash
make helios-smoke
```

5. Confirm output artifact exists:
   - `artifacts/reports/audio-inference-smoke.json`

## Non-Negotiable Runtime Pins

- `torch==2.10.0`
- `numpy==2.2.5`
- `protobuf==4.25.8`
- `protoc==29.3`

Dependency resolution is allowed only in approved provisioning environments with
auditable change records.

## Contract and Safety Invariants

- Command lane emits explicit terminal outcome: `granted`, `refused`, `escalated`.
- Fail-closed defaults on uncertainty or subsystem failure.
- Dictation lane never executes commands.
- Grammar + policy gates are mandatory and cannot be bypassed.
- Interrupt path (`stop`, `cancel`, etc.) remains available under degradation.

## Data and Protocol Rules

- Protobuf is authoritative for machine/infrastructure paths.
- JSON is only for human-facing APIs, dashboards, and debugging.
- Artifacts must be loaded from approved manifests with version + checksum.
- Promoted model aliases must preserve provenance:
  base model/version, adapter type (LoRA/QLoRA), dataset lineage, license,
  and evaluation results.

## Documentation Map

- `docs/architecture/command-lane.md`
- `docs/architecture/maestro-bridge.md`
- `docs/operations/model-start-and-usage.md`
- `docs/model-card-command-lane.md`
- `docs/operations/dependency-audit.md`
- `docs/operations/canary-rollout.md`
- `docs/operations/merge-gates.md`

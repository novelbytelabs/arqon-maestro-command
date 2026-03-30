# Implementation Plan: Arqon Maestro Command Lane

**Branch**: `001-develop-arqon-maestro` | **Date**: 2026-03-30 | **Spec**: `/home/irbsurfer/Projects/arqon/arqon-maestro-command/specs/001-develop-arqon-maestro/spec.md`
**Input**: Feature specification from `/home/irbsurfer/Projects/arqon/arqon-maestro-command/specs/001-develop-arqon-maestro/spec.md`

## Summary

Deliver a deterministic, fail-closed command lane with strict lane separation,
protobuf-first contracts, immutable runtime discipline, and hard merge gates.
Implementation is sequenced in explicit phases requested by the product owner:

- Phase A: dependency completeness audit + environment readiness
- Phase B: command lane implementation
- Phase C: full test suite (unit/integration/e2e/regression/adversarial)
- Phase D: CI enforcement + merge gates

## Phase Crosswalk

- Plan Phase A -> Tasks Phase 1-2
- Plan Phase B -> Tasks Phase 3-6
- Plan Phase C -> Tasks Phase 3-6 test tracks + Phase 7 validation
- Plan Phase D -> Tasks Phase 7

## Technical Context

**Language/Version**: Python 3.10.19 + Rust toolchain (stable)  
**Primary Dependencies**: NeMo 2.1.x, PyTorch 2.10.0, protobuf 4.25.8, protoc 29.3, WFST/GBNF grammar artifacts  
**Storage**: Repo-managed files for contracts/manifests/evidence/audit reports  
**Testing**: unit + integration + e2e + regression + adversarial suites; `make helios-smoke`  
**Target Platform**: Linux with frozen Conda runtime `helios-gpu-118`  
**Project Type**: single repository (specs + ops scripts + docs + contracts)  
**Performance Goals**: command-lane p95 decision latency < 200ms under BP-001; adapter fail-closed at <=150ms  
**Constraints**: no direct installs in frozen runtime; dependency resolution only in approved provisioning envs; protobuf-first machine paths  
**Scale/Scope**: canonical lane routing + deterministic command outcomes + audit-grade evidence + CI gates

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- Control-first grammar authority and deterministic terminal outcomes are explicitly
  enforced in scope. **PASS**
- Fail-closed safety remains default for uncertainty/timeouts/failures; high-impact
  confirmations auto-refuse in 5s. **PASS**
- Hot-path targets include p95 < 200ms and adapter timeout <=150ms. **PASS**
- Evidence contract requirements (`SpeechResult`, `CommandResult`, `EvidencePacket`)
  are explicit and test-gated. **PASS**
- Runtime constraints preserve frozen `helios-gpu-118`; direct installs prohibited.
  **PASS**
- Implementation Readiness Gate includes `make helios-smoke` pre-code and pre-merge
  with required artifact output. **PASS**
- Dependency Completeness Audit required before implementation start; deferred
  dependencies block start. **PASS**
- Five mandatory test categories enforced in CI. **PASS**

## Project Structure

### Documentation (this feature)

```text
/home/irbsurfer/Projects/arqon/arqon-maestro-command/specs/001-develop-arqon-maestro/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   ├── command-contracts.md
│   └── openapi.yaml
├── checklists/
│   └── requirements.md
└── tasks.md
```

### Source Code (repository root)

```text
/home/irbsurfer/Projects/arqon/arqon-maestro-command/
├── ops/helios/
├── artifacts/
├── docs/
├── specs/
├── README.md
├── Makefile
└── AGENTS.md
```

**Structure Decision**: single-repo architecture with planning artifacts in
`specs/001-develop-arqon-maestro`, runtime and validation tooling in `ops/helios`,
and evidence/audit outputs in `artifacts/reports`.

## Phase A: Dependency Completeness Audit + Environment Readiness

- Create `/home/irbsurfer/Projects/arqon/arqon-maestro-command/artifacts/reports/dependency-audit.md`.
- Record dependency status for each test level (unit/integration/e2e/regression/adversarial):
  `present_in_frozen_runtime`, `provisioned_externally`, or `deferred`.
- Enforce hard block if any dependency is `deferred` (per clarification).
- Run `make helios-smoke`; require PASS and artifact
  `/home/irbsurfer/Projects/arqon/arqon-maestro-command/artifacts/reports/audio-inference-smoke.json`.
- Run runtime hygiene gate (`ops/helios/runtime_hygiene_gate.sh`) and require
  zero direct-install violations in frozen runtime contexts.

## Phase B: Command Lane Implementation

- Implement lane routing with strict command vs dictation separation.
- Enforce grammar + policy gates; default fail-closed for uncertainty.
- Enforce high-impact confirmation timeout (5s -> auto-refuse).
- Enforce adapter timeout fail-closed at <=150ms.
- Emit contract-conformant `SpeechResult`, `CommandResult`, and `EvidencePacket`.
- Enforce protocol sovereignty on machine paths: accept protobuf, reject JSON
  with typed refusal reasons.

## Phase C: Full Test Suite

- Unit: parser/routing/policy logic determinism and timeout handling.
- Integration: adapter + grammar + policy + orchestrator behavior.
- E2E: utterance-to-decision-to-evidence flows.
- Regression: corpus stability, compatibility, and latency trend checks.
- Adversarial: OOG/malformed/hazard/bypass attempts with fail-closed assertions.
- Enforce high-impact false-positive threshold <=0.1%.
- Compute and publish high-impact false-positive rate from approved
  regression/adversarial outputs and fail the run on threshold breach.
- Compute monthly availability report inputs and validate SLO policy hooks for
  99.9% availability target.
- Validate availability breach handling: SEV-2 workflow starts within 15 minutes
  with on-call owner notification and corrective-action record.

## Phase D: CI Enforcement + Merge Gates

Required checks before merge:
- `make helios-smoke`
- protobuf contract validation
- evidence packet schema validation
- unit suite
- integration suite
- e2e suite
- regression suite
- adversarial suite
- dependency audit completeness check (no `deferred`)
- runtime hygiene gate (`ops/helios/runtime_hygiene_gate.sh`)
- false-positive threshold gate (`<=0.1%`)
- canary decision record + rollback drill artifact presence

## Risk Register

| Risk | Impact | Mitigation | Fallback |
|------|--------|------------|----------|
| Deferred dependency discovered at implementation start | Blocks progress by policy | Complete dependency audit first and resolve all deferred items | Move dependency to approved provisioning env; export immutable artifact and reclassify status |
| Frozen runtime mismatch with model stack | Runtime failure or degraded performance | Gate every change with `make helios-smoke` and pinned versions | Dual-env provisioning/training; import immutable artifacts back into frozen runtime |
| Contract drift between adapters and orchestrator | Decision/evidence incompatibility | Protobuf + evidence schema CI gates | Freeze adapter promotion, rollback to last known-good manifest |
| Latency drift above p95 target | UX and safety impact | Regression latency thresholds and profiling | Restrict feature path to degraded lane until budget restored |
| High-impact false positives exceed threshold | Unsafe command acceptance risk | Adversarial + regression gates with <=0.1% threshold | Temporary forced confirmation/refusal policy for impacted command set |

## Complexity Tracking

No constitution violations accepted in this plan.

## Post-Design Constitution Re-Check

After Phase 1 design artifact generation, all constitution gates remain **PASS**.

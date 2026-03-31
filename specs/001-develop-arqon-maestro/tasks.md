# Tasks: Arqon Maestro Command Lane

**Input**: Design documents from `/home/irbsurfer/Projects/arqon/arqon-maestro-command/specs/001-develop-arqon-maestro/`
**Prerequisites**: `/home/irbsurfer/Projects/arqon/arqon-maestro-command/specs/001-develop-arqon-maestro/plan.md`, `/home/irbsurfer/Projects/arqon/arqon-maestro-command/specs/001-develop-arqon-maestro/spec.md`, `/home/irbsurfer/Projects/arqon/arqon-maestro-command/specs/001-develop-arqon-maestro/research.md`, `/home/irbsurfer/Projects/arqon/arqon-maestro-command/specs/001-develop-arqon-maestro/data-model.md`, `/home/irbsurfer/Projects/arqon/arqon-maestro-command/specs/001-develop-arqon-maestro/contracts/`

**Tests**: Mandatory (unit, integration, e2e, regression, adversarial) per spec and constitution.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing.

## Phase 1: Setup (Project Initialization)

**Purpose**: Establish project scaffolding and baseline structure used by all stories.

- [X] T001 Create command-lane package scaffold in `src/command_lane/__init__.py`
- [X] T002 [P] Create command-lane API package scaffold in `src/command_lane/api/__init__.py`
- [X] T003 [P] Create policy configuration scaffold in `configs/lane_policy.yaml`
- [X] T004 [P] Create SLO configuration scaffold in `configs/slo_targets.yaml`
- [X] T005 [P] Create unit test package scaffold in `tests/unit/__init__.py`
- [X] T006 [P] Create integration test package scaffold in `tests/integration/__init__.py`
- [X] T007 [P] Create e2e test package scaffold in `tests/e2e/__init__.py`
- [X] T008 [P] Create regression test package scaffold in `tests/regression/__init__.py`
- [X] T009 [P] Create adversarial test package scaffold in `tests/adversarial/__init__.py`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Build shared readiness, contracts, and validation gates before story work.

- [X] T010 Implement dependency audit generator CLI in `scripts/dependency_audit.py`
- [X] T011 Implement dependency audit markdown renderer in `scripts/dependency_audit_report.py`
- [X] T012 Implement deferred-dependency hard-block validator in `scripts/validate_dependency_audit.py`
- [X] T013 [P] Implement canonical lane and terminal decision types in `src/command_lane/types.py`
- [X] T014 [P] Implement protobuf contract loader and guards in `src/command_lane/contracts.py`
- [X] T015 [P] Implement shared fail-closed error types in `src/command_lane/errors.py`
- [X] T016 Implement command-lane service pipeline shell in `src/command_lane/service.py`
- [X] T017 [P] Add test-suite and contract gate targets in `Makefile`
- [X] T018 [P] Wire baseline CI checks for smoke/dependency/tests in `.github/workflows/ci.yml`

**Checkpoint**: Foundation complete; user story phases can proceed.

---

## Phase 3: User Story 1 - Execute Commands Deterministically (Priority: P1) 🎯 MVP

**Goal**: Deterministic command outcomes with explicit refusal rationale.

**Independent Test**: Replay validated command corpus and verify every utterance ends in exactly one terminal decision (`granted`, `refused`, `escalated`).

### Tests for User Story 1

- [X] T019 [P] [US1] Add grammar gate unit tests in `tests/unit/test_command_grammar_gate.py`
- [X] T020 [P] [US1] Add fail-closed policy unit tests in `tests/unit/test_policy_fail_closed.py`
- [X] T021 [P] [US1] Add command decision integration tests in `tests/integration/test_command_decision_flow.py`
- [X] T022 [P] [US1] Add deterministic terminal outcome e2e tests in `tests/e2e/test_command_terminal_outcomes.py`
- [X] T023 [P] [US1] Add out-of-grammar adversarial refusal tests in `tests/adversarial/test_out_of_grammar_refusal.py`

### Implementation for User Story 1

- [X] T024 [P] [US1] Implement bounded grammar gate in `src/command_lane/grammar_gate.py`
- [X] T025 [P] [US1] Implement policy adjudication gate in `src/command_lane/policy_gate.py`
- [X] T026 [US1] Implement terminal authority resolver in `src/command_lane/decision_engine.py`
- [X] T027 [US1] Implement `/v1/commands/evaluate` handler in `src/command_lane/api/commands.py`
- [X] T028 [US1] Implement refusal rationale logging in `src/command_lane/decision_logging.py`

**Checkpoint**: US1 is independently testable and MVP-ready.

---

## Phase 4: User Story 2 - Keep Dictation Separate from Command Control (Priority: P1)

**Goal**: Ensure dictation output cannot trigger command execution.

**Independent Test**: Run mixed dictation corpus in dictation lane with zero command policy path invocation.

### Tests for User Story 2

- [ ] T029 [P] [US2] Add lane-routing exclusivity unit tests in `tests/unit/test_lane_router.py`
- [ ] T030 [P] [US2] Add dictation isolation integration tests in `tests/integration/test_dictation_isolation.py`
- [ ] T031 [P] [US2] Add lane-switch provenance e2e tests in `tests/e2e/test_lane_switch_provenance.py`
- [ ] T032 [P] [US2] Add homophone collision regression tests in `tests/regression/test_homophone_lane_collision.py`

### Implementation for User Story 2

- [ ] T033 [P] [US2] Implement canonical lane router in `src/command_lane/router.py`
- [ ] T034 [US2] Implement dictation command-path guard in `src/command_lane/dictation_guard.py`
- [ ] T035 [US2] Implement `/v1/utterances` intake handler in `src/command_lane/api/utterances.py`
- [ ] T036 [US2] Persist lane provenance metadata in `src/command_lane/provenance.py`

**Checkpoint**: US2 is independently functional and testable.

---

## Phase 5: User Story 3 - Maintain Low-Latency Hot-Path Control (Priority: P2)

**Goal**: Meet BP-001 latency target, prioritize interrupts, and enforce timeout safety.

**Independent Test**: Validate p95 <200ms under BP-001, adapter fail-closed at 150ms, and confirmation timeout auto-refusal at 5s.

### Tests for User Story 3

- [ ] T037 [P] [US3] Add adapter timeout unit tests in `tests/unit/test_adapter_timeout.py`
- [ ] T038 [P] [US3] Add interrupt-priority integration tests in `tests/integration/test_interrupt_priority.py`
- [ ] T039 [P] [US3] Add high-impact confirmation timeout e2e tests in `tests/e2e/test_confirmation_timeout.py`
- [ ] T040 [P] [US3] Add BP-001 latency regression benchmark tests in `tests/regression/test_latency_budget_bp001.py`
- [ ] T041 [P] [US3] Add rapid lane-toggle adversarial tests in `tests/adversarial/test_rapid_lane_toggling.py`

### Implementation for User Story 3

- [ ] T042 [P] [US3] Implement adapter timeout fail-closed enforcement in `src/command_lane/adapter_timeout.py`
- [ ] T043 [P] [US3] Implement confirmation challenge lifecycle in `src/command_lane/confirmation.py`
- [ ] T044 [US3] Implement interrupt command prioritization in `src/command_lane/interrupts.py`
- [ ] T045 [US3] Implement BP-001 latency metrics aggregation in `src/command_lane/metrics.py`
- [ ] T046 [US3] Configure 150ms timeout and 5s confirmation policy in `configs/lane_policy.yaml`

**Checkpoint**: US3 is independently functional and testable.

---

## Phase 6: User Story 4 - Preserve Audit-Grade Evidence and Contracts (Priority: P2)

**Goal**: Emit and validate contract-conformant `SpeechResult`, `CommandResult`, and `EvidencePacket` artifacts.

**Independent Test**: Validate contract/schema conformance across all processed utterances and adapter substitutions.

### Tests for User Story 4

- [ ] T047 [P] [US4] Add evidence packet completeness unit tests in `tests/unit/test_evidence_packet_fields.py`
- [ ] T048 [P] [US4] Add adapter contract compatibility integration tests in `tests/integration/test_adapter_contract_compatibility.py`
- [ ] T049 [P] [US4] Add evidence endpoint contract tests in `tests/integration/test_evidence_endpoint_contract.py`
- [ ] T050 [P] [US4] Add schema drift regression tests in `tests/regression/test_contract_schema_regression.py`

### Implementation for User Story 4

- [ ] T051 [P] [US4] Implement SpeechResult builder in `src/command_lane/speech_result_builder.py`
- [ ] T052 [P] [US4] Implement CommandResult builder in `src/command_lane/command_result_builder.py`
- [ ] T053 [P] [US4] Implement EvidencePacket builder and serializer in `src/command_lane/evidence.py`
- [ ] T054 [US4] Implement `/v1/evidence/{evidenceId}` handler in `src/command_lane/api/evidence.py`
- [ ] T055 [US4] Implement evidence schema gate script in `ops/helios/validate_evidence_schema.py`
- [ ] T056 [US4] Implement `/v1/readiness/dependency-audit` handler in `src/command_lane/api/readiness.py`

**Checkpoint**: US4 is independently functional and testable.

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Complete cross-story operational readiness and merge/release gates.

- [ ] T057 [P] Implement internal machine-path protocol guard (protobuf accept / JSON reject) in `src/command_lane/protocol_guard.py`
- [ ] T058 [P] Add protocol sovereignty integration tests in `tests/integration/test_protocol_sovereignty.py`
- [ ] T059 [P] Enforce runtime hygiene gate in CI via `ops/helios/runtime_hygiene_gate.sh` in `.github/workflows/ci.yml`
- [ ] T060 [P] Implement false-positive threshold gate parser and validator in `ops/helios/validate_false_positive_rate.py`
- [ ] T061 [P] Implement monthly availability report generator in `scripts/availability_report.py`
- [ ] T062 [P] Implement availability breach handler (SEV-2 <=15 min, owner ack) in `scripts/availability_breach_handler.py`
- [ ] T063 [P] Add canary rollout runbook in `docs/operations/canary-rollout.md`
- [ ] T064 [P] Implement rollback drill runner in `ops/helios/rollback_drill.sh`
- [ ] T065 [P] Wire canary/rollback evidence checks into CI in `.github/workflows/ci.yml`
- [ ] T066 Execute rollback drill for RC flow and store artifact in `artifacts/reports/rollback-drill-report.json`
- [ ] T067 [P] Add architecture and lane isolation documentation in `docs/architecture/command-lane.md`
- [ ] T068 [P] Add dependency audit operations guide in `docs/operations/dependency-audit.md`
- [ ] T069 Add merge-gate operations guide in `docs/operations/merge-gates.md`
- [ ] T070 Run full readiness validation and record RC report in `artifacts/reports/release-candidate-validation.md`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: No dependencies.
- **Phase 2 (Foundational)**: Depends on Phase 1 and blocks all story phases.
- **Phase 3-6 (User Stories)**: Depend on Phase 2; proceed in priority order or parallel by staffing.
- **Phase 7 (Polish & Cross-Cutting)**: Depends on completion of required story phases and must complete before merge/release.

### User Story Dependencies

- **US1 (P1)**: Starts after Phase 2; independent base for deterministic decisions.
- **US2 (P1)**: Starts after Phase 2; independent lane isolation story.
- **US3 (P2)**: Depends on Phase 2 and reuses US1 decision primitives.
- **US4 (P2)**: Depends on Phase 2 and reuses outputs from US1-US3.

### Dependency Graph (Story Completion Order)

- Foundation -> {US1, US2}
- US1 -> US3
- {US1, US2, US3} -> US4
- {US1, US2, US3, US4} -> Polish

---

## Parallel Execution Examples

### User Story 1

```bash
# Parallel tests
T019, T020, T021, T022, T023
# Parallel implementation primitives
T024, T025
```

### User Story 2

```bash
# Parallel tests
T029, T030, T031, T032
# Parallel implementation primitives
T033, T034
```

### User Story 3

```bash
# Parallel tests
T037, T038, T039, T040, T041
# Parallel implementation primitives
T042, T043
```

### User Story 4

```bash
# Parallel tests
T047, T048, T049, T050
# Parallel contract builders
T051, T052, T053
```

---

## Implementation Strategy

### MVP First (User Story 1)

1. Complete Phase 1 and Phase 2.
2. Complete Phase 3 (US1).
3. Validate deterministic outcome tests and smoke gates.
4. Demo MVP behavior.

### Incremental Delivery

1. Deliver US1 + US2 for deterministic control and lane safety.
2. Deliver US3 for latency/interrupt behavior.
3. Deliver US4 for audit and contract conformance.
4. Complete Phase 7 for operational readiness and merge/release gates.

### Parallel Team Strategy

1. Team completes Phase 1 and Phase 2 jointly.
2. Parallel workstreams: Team A (US1), Team B (US2).
3. Team C starts US3 after US1 primitives stabilize.
4. Team D executes US4 and Phase 7 cross-cutting gates.

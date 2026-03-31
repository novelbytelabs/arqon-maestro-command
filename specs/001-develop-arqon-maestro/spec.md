# Feature Specification: Arqon Maestro Command Lane

**Feature Branch**: `001-develop-arqon-maestro`  
**Created**: 2026-03-30  
**Status**: Ready for verification  
**Input**: User description: "Develop the Arqon Maestro Command Lane, a control-first speech system for deterministic, operator-safe execution of voice commands within the Arqon Maestro Voice Operating System. The system must prioritize deterministic accept/reject behavior, grammar authority, a bounded command language, and fail-closed safety. It needs to distinguish from a Dictation Lane, optimize for low-latency command acceptance, and integrate with a Rust hot-path orchestrator for audio processing, policy adjudication, and interrupt authority. Define the canonical interaction lanes and ensure compliance with command and evidence packet contracts."

## Clarifications

### Session 2026-03-30

- Q: What monthly command-lane availability target should define reliability gates? → A: 99.9% monthly.
- Q: What fail-closed adapter timeout budget should be enforced? → A: 150ms.
- Q: What false-positive ceiling should apply to high-impact commands? → A: <=0.1%.
- Q: What timeout should apply to high-impact confirmation prompts? → A: 5 seconds.
- Q: How should deferred dependency items affect implementation start? → A: Hard block implementation start.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Execute Commands Deterministically (Priority: P1)

As an operator, I can issue a supported voice command and receive a deterministic
outcome (execute or explicit refusal) so that control actions are predictable and
safe.

**Why this priority**: Deterministic command handling is the core product value and
safety baseline for Command Lane.

**Independent Test**: Can be fully tested by replaying a validated command corpus
and verifying each utterance produces one explicit terminal outcome (`granted`,
`refused`, or `escalated`) with no silent acceptance.

**Acceptance Scenarios**:

1. **Given** command mode and an in-grammar command, **When** the command is spoken,
   **Then** the system returns a parsed command intent and an explicit execution
   authority decision.
2. **Given** command mode and an out-of-grammar utterance, **When** audio is
   processed, **Then** the system refuses execution and records the refusal reason
   in evidence.
3. **Given** low confidence or policy failure, **When** a command candidate is
   evaluated, **Then** the system fails closed and never executes by default.

---

### User Story 2 - Keep Dictation Separate from Command Control (Priority: P1)

As an operator, I can dictate free-form speech without accidentally triggering
command execution so that writing and control remain safely isolated.

**Why this priority**: Lane separation prevents accidental actuation and is a
critical constitutional requirement.

**Independent Test**: Can be tested independently by sending mixed dictation-style
utterances while in dictation lane and asserting zero command execution attempts.

**Acceptance Scenarios**:

1. **Given** dictation lane, **When** free-form text is spoken, **Then** output is
   treated as transcription only and no command policy path is invoked.
2. **Given** a lane switch from dictation to command, **When** the next utterance is
   processed, **Then** routing follows the selected lane and evidence records lane
   provenance.

---

### User Story 3 - Maintain Low-Latency Hot-Path Control (Priority: P2)

As an operator, I get rapid command accept/reject outcomes so that voice control
feels immediate and interruptions remain responsive.

**Why this priority**: Low-latency response is required for practical command
control and interruption authority.

**Independent Test**: Can be tested with a timed command corpus and benchmark suite
that measures end-to-end acceptance/refusal latency.

**Acceptance Scenarios**:

1. **Given** healthy command lane operation, **When** a supported command is spoken,
   **Then** the command decision is emitted within the defined hot-path latency
   target.
2. **Given** an active operation and a stop/cancel utterance, **When** degraded or
   normal command lane is active, **Then** interrupt authority is prioritized and
   interruption evidence is emitted.

---

### User Story 4 - Preserve Audit-Grade Evidence and Contracts (Priority: P2)

As a platform maintainer, I can inspect command/evidence contracts for every
utterance so that policy decisions are auditable and adapters remain replaceable.

**Why this priority**: Evidence and stable contracts enable safety audits,
regression detection, and provider modularity.

**Independent Test**: Can be tested by validating generated SpeechResult,
CommandResult, and EvidencePacket records against the command contract schema.

**Acceptance Scenarios**:

1. **Given** any processed utterance, **When** a decision is made, **Then** evidence
   includes lane, confidence adjudication, policy outcome, latency, provider id,
   and timestamp.
2. **Given** an adapter replacement that honors the contract, **When** command corpus
   tests run, **Then** semantic command outcomes remain consistent.

### Edge Cases

- Utterance partially matches grammar but confidence is below threshold.
- Homophone collisions between command terms and dictation phrases.
- Rapid lane toggling while audio stream is active.
- Adapter timeout or transient failure during policy adjudication.
- Degraded command sub-lane activation while primary command lane is unavailable.
- High-impact command spoken without required confirmation context.

### Test Strategy Requirements

- **Unit**: Parser, lane-routing, and policy-decision logic tests MUST pass with
  deterministic outcomes and fail-closed defaults verified for uncertainty paths.
- **Integration**: Adapter + grammar + policy + orchestrator integration tests
  MUST pass, including timeout/unavailable adapter behavior and lane isolation.
- **End-to-End (E2E)**: Full utterance-to-decision flows MUST pass for command
  and dictation lanes with evidence packet emission validated.
- **Regression**: Command corpus and contract compatibility suites MUST pass with
  no behavioral drift in deterministic outcomes for approved fixtures.
- **Adversarial**: Out-of-grammar, malformed payload, phonetic hazard, and policy
  bypass-attempt tests MUST pass with explicit refusals and fail-closed behavior.

## Requirements *(mandatory)*

**Constitution Guardrails**: Define bounded command grammar and lexicon ownership,
fail-closed behavior (refusals + confirmations for high-impact actions), lane
separation (dictation cannot execute commands), hot-path latency expectations
(p95 < 200ms to accept commands), evidence packet emission, adapter boundaries
(constrained decoding against Maestro grammars), frozen env `helios-gpu-118`
(no new installs), infrastructure payloads in protobuf v4.25.8/protoc (JSON only
for human-facing surfaces), pinned core runtime versions unchanged
(`torch==2.10.0`, `numpy==2.2.5`, `protobuf==4.25.8`, `protoc==29.3`), approved
provisioning environment only for dependency resolution, mandatory dependency
completeness audit artifact `artifacts/reports/dependency-audit.md`, and required
implementation readiness gate via `make helios-smoke`.

### Functional Requirements

- **FR-001**: System MUST route every utterance to exactly one canonical lane from:
  `command_lane`, `dictation_lane`, `conversation_lane`, `translation_lane`,
  `search_explore_lane`, or degraded command sub-lane.
- **FR-002**: System MUST enforce bounded command language behavior in
  `command_lane`, where each command candidate is either accepted or explicitly
  rejected with a reason.
- **FR-003**: System MUST treat grammar and lexicon definitions as authoritative for
  command semantics, independent of ASR provider substitutions.
- **FR-004**: System MUST fail closed for uncertain command decisions and MUST
  require explicit confirmation for high-impact actions.
- **FR-005**: System MUST prevent dictation outputs from triggering command
  execution paths.
- **FR-006**: System MUST prioritize interrupt authority (`stop`, `cancel`, and
  degraded-lane interrupt vocabulary) over lower-priority command handling.
- **FR-007**: System MUST emit a SpeechResult contract for each utterance including
  transcript, lane, provider metadata, confidence data, endpoint metadata,
  elapsed processing time, and degraded state.
- **FR-008**: System MUST emit a CommandResult contract for command-lane decisions
  containing parsed command, structured intent, policy decision, execution
  authority status, and evidence linkage.
- **FR-009**: System MUST emit an EvidencePacket for command decisions containing
  audio hash, lane provenance, confidence adjudication, policy outcome, latency,
  adapter metadata, and timestamp.
- **FR-010**: System MUST support pluggable ASR adapters through a constrained
  contract boundary where adapter changes do not alter defined command semantics.
- **FR-011**: System MUST meet the command-lane low-latency target for acceptance or
  refusal decisions under benchmark profile BP-001: frozen `helios-gpu-118`
  runtime, warmed model state, one concurrent lane session, validated command
  corpus of at least 1,000 utterances, and median utterance duration of 1-4
  seconds.
- **FR-012**: System MUST use protobuf as the authoritative infrastructure wire
  format on internal machine paths and MUST reject infrastructure-level JSON
  payloads with typed refusal reasons.
- **FR-013**: Before implementation starts, repository MUST produce
  `artifacts/reports/dependency-audit.md` with dependency status by test level
  (unit/integration/e2e/regression/adversarial), and each dependency MUST be
  marked as present in frozen runtime, provisioned externally, or deferred.
- **FR-014**: System MUST require all five test categories (unit, integration,
  e2e, regression, adversarial) as mandatory for production readiness.
- **FR-015**: CI MUST require `make helios-smoke` to pass before merge.
- **FR-016**: CI MUST require contract validation checks to pass before merge.
- **FR-017**: CI MUST require evidence packet schema validation checks to pass
  before merge.
- **FR-018**: CI MUST enforce all five mandatory test categories as required
  checks before merge.
- **FR-019**: Runtime work MUST execute in frozen `helios-gpu-118` with no direct
  in-environment installs.
- **FR-020**: Dependency resolution/provisioning MUST occur only in approved
  provisioning environments with auditable records, including
  `artifacts/reports/provisioning-environment-audit.md` (environment identity,
  approval reference, operator, timestamp) and
  `artifacts/reports/provisioning-change-log.md` (dependency change entries with
  source and outcome).
- **FR-021**: Command-lane service availability MUST meet or exceed 99.9% monthly.
- **FR-022**: Adapter timeout handling MUST fail closed at 150ms or less for
  command-lane decisions.
- **FR-023**: High-impact command false-positive rate MUST be less than or equal
  to 0.1% on the validated adversarial and regression evaluation suites as a
  command safety policy threshold (policy target; enforcement defined by FR-029).
- **FR-024**: High-impact confirmation prompts MUST auto-refuse if explicit
  confirmation is not received within 5 seconds.
- **FR-025**: Implementation MUST NOT start while any dependency remains marked
  `deferred` in `artifacts/reports/dependency-audit.md`.
- **FR-026**: CI and pre-merge validation MUST run runtime hygiene enforcement to
  block direct package installs in frozen `helios-gpu-118`.
- **FR-027**: Internal machine-path interfaces MUST enforce and emit auditable
  typed refusal responses for any non-protobuf payload; this operationalizes
  FR-012 at runtime and in validation outputs.
- **FR-028**: Release operations MUST include documented canary and rollback
  procedures, and each release candidate MUST record rollback drill evidence.
- **FR-029**: CI MUST compute and enforce the high-impact false-positive threshold
  of less than or equal to 0.1% from approved regression/adversarial evaluation
  outputs. This CI gate is the enforcement mechanism for FR-023.
- **FR-030**: Operations MUST produce a monthly command-lane availability report
  and MUST trigger SLO breach handling when availability falls below 99.9%,
  including SEV-2 incident workflow initiation within 15 minutes, on-call owner
  notification, and corrective-action record creation in `artifacts/reports`.

### Key Entities *(include if feature involves data)*

- **UtteranceEnvelope**: Unit of processed speech containing transcript candidate,
  lane context, provider metadata, endpointing metadata, and timing values.
- **SpeechResult**: Standardized output contract for utterance recognition and lane
  assignment.
- **CommandResult**: Standardized command decision artifact with intent,
  parameters, policy decision, and execution authority.
- **EvidencePacket**: Immutable audit record for command decision provenance and
  policy rationale.
- **LanePolicyProfile**: Configuration object defining lane-specific routing,
  thresholds, and allowed authority behavior.
- **AdapterCapabilityProfile**: Contract metadata defining what each ASR adapter can
  provide while preserving Maestro-owned semantics.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of evaluated command-lane utterances produce an explicit terminal
  decision (`granted`, `refused`, or `escalated`) with no silent execution.
- **SC-002**: At least 99% of out-of-grammar utterances in the command corpus are
  refused and recorded with refusal rationale.
- **SC-003**: Command acceptance/refusal decisions complete within 200 ms at p95 for
  the validated command corpus under normal operating load.
- **SC-004**: 100% of processed command decisions emit valid SpeechResult,
  CommandResult, and EvidencePacket records that pass contract validation.
- **SC-005**: 0 verified incidents of dictation-lane utterances causing command
  execution during lane-isolation test runs.
- **SC-006**: 100% of required checks are green before merge (`make helios-smoke`,
  contract validation, evidence packet schema validation, and all five test
  categories).
- **SC-007**: 0 unresolved dependency gaps remain in
  `artifacts/reports/dependency-audit.md` before implementation starts.
- **SC-008**: A new AI/dev instance can reproduce the local readiness runbook
  (including `make helios-smoke`) without additional in-env installs, and the
  run MUST produce `artifacts/reports/readiness-reproducibility.md` capturing
  executed commands, runtime identity, and PASS/FAIL outcomes.
- **SC-009**: Command-lane monthly availability is at least 99.9% over the
  measured reporting window.
- **SC-010**: 100% of adapter timeout cases at or beyond 150ms result in explicit
  fail-closed outcomes (`refused` or `escalated`) with evidence emitted.
- **SC-011**: High-impact command false-positive rate is less than or equal to
  0.1% on the approved validation corpus.
- **SC-012**: 100% of unconfirmed high-impact prompts are auto-refused after
  5 seconds and emit evidence with timeout rationale.
- **SC-014**: 100% of CI and pre-merge runs execute runtime hygiene checks with
  zero direct-install violations in frozen runtime contexts.
- **SC-015**: 100% of internal machine-path JSON payload attempts are rejected
  with explicit typed refusal responses, while protobuf payloads continue to pass.
- **SC-016**: Every release candidate includes a canary decision record and a
  successful rollback drill artifact before promotion approval; successful means
  recovery to the last known-good manifest within 10 minutes with post-rollback
  `make helios-smoke` and contract validation passing.
- **SC-017**: CI fails any run where high-impact false-positive rate exceeds 0.1%
  on approved evaluation outputs.
- **SC-018**: Monthly availability report is generated for each reporting window
  and records command-lane availability at or above 99.9%; any breach initiates
  SEV-2 workflow within 15 minutes and records owner acknowledgment.

## Assumptions

- Operators intentionally select or invoke the intended interaction lane before
  issuing commands or dictation.
- Canonical lane set remains fixed for this feature scope, including degraded
  command sub-lane support.
- High-impact action classification is maintained by policy configuration and is
  available at decision time.
- Command corpus and phonetic hazard corpus are available for deterministic and
  latency validation.
- Arqon Maestro acts as command authority while downstream orchestration systems
  execute approved capabilities.
- Approved provisioning environments are available for dependency resolution and
  can produce auditable change records.

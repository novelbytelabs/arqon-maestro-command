# Feature Specification: Arqon Maestro Command Lane

**Feature Branch**: `001-develop-arqon-maestro`  
**Created**: 2026-03-30  
**Status**: Draft  
**Input**: User description: "Develop the Arqon Maestro Command Lane, a control-first speech system for deterministic, operator-safe execution of voice commands within the Arqon Maestro Voice Operating System. The system must prioritize deterministic accept/reject behavior, grammar authority, a bounded command language, and fail-closed safety. It needs to distinguish from a Dictation Lane, optimize for low-latency command acceptance, and integrate with a Rust hot-path orchestrator for audio processing, policy adjudication, and interrupt authority. Define the canonical interaction lanes and ensure compliance with command and evidence packet contracts."

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
  refusal decisions under normal operating conditions.
- **FR-012**: System MUST reject infrastructure-level JSON payloads on internal
  machine paths and use protobuf as the authoritative infrastructure wire format.
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
  provisioning environments with auditable records.

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
  (including `make helios-smoke`) without additional in-env installs.

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

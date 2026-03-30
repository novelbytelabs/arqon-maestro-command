<!--
Sync Impact Report
Version: 2.1.0 -> 2.2.0
Modified principles: IV.3 Test Discipline; IV.4 Quality Gates; IV.5 Automated Enforcement; V. Lifecycle and Automation
Added sections: none
Removed sections: none
Templates: ⚠ pending .specify/templates/plan-template.md; ⚠ pending .specify/templates/spec-template.md; ⚠ pending .specify/templates/tasks-template.md; ⚠ pending .specify/templates/commands/*.md (directory not present)
Follow-up TODOs: reconcile template language with mandatory Implementation Readiness Gate, Dependency Completeness Audit, and required five test-suite categories.
-->

# Arqon Maestro Command Lane Constitution

This document defines the non-negotiable principles that govern how Arqon Maestro
Command Lane is designed, evolved, and maintained. It exists to protect Command
Lane from accidental bloat, regression, silent breakage, and shortcuts that erode
operator trust. If a decision conflicts with this constitution, the decision is
wrong.

> Spec Kit Note: This constitution is the hard sandbox for all `/speckit.*`
> commands. Specs, plans, and tasks MUST NOT violate Sections II through XI.

---

# 0. The Integrity Imperative (Meta-Constitution)

"Amateurs practice until they get it right. Professionals practice until they
cannot get it wrong."

This section overrides all others. Violations are systemic failures.

## 0.1 Definition of Done (4-Pillar Standard)

A task is NEVER done until all four pillars are standing:

1. Implementation: Code exists, compiles, and handles edge cases.
2. Verification: Automated tests prove realistic behavior.
3. Documentation: Architecture, usage, and caveats are updated in `docs/` or
   `README.md`.
4. Evidence: Distinct proof of function exists (logs, traces, benchmarks,
   screenshots when appropriate).

Rule: Marking work complete without all four pillars is invalid.

## 0.2 Data Integrity and the Ban on Lazy Synthetics

Testing with trivial synthetic values is a constitution violation.

- Realism Mandate: Tests MUST mirror production complexity and adversarial input.
- Fuzzing Mandate: Inputs MUST be varied or fuzzed in parser and policy paths.
- No Happy Path Only: Tests MUST assert failure behavior (auth failure,
  malformed input, adapter outage, policy timeout).

## 0.3 Placeholder Prohibition

- Zero Stubs: `todo!()`, `unimplemented!()`, or equivalent placeholders are not
  allowed in claimed-complete features.
- Zero Unsafe Defaults: No insecure defaults without explicit dev-mode guardrails.
- Zero "Later": Required safety and policy behavior MUST be implemented now,
  not deferred to an undefined hardening phase.

## 0.4 Professional Standard

- Warnings are errors.
- Error swallowing is forbidden.
- Complexity without justification is rejected.

---

# I. Vision and Scope

## 1. Vision

Arqon Maestro Command Lane is the deterministic control plane for voice actuation.
It is built for governed command execution, not generic transcription benchmarking.

## 2. Scope

### 2.1 In Scope

Command Lane is responsible for:

- Acoustic-to-command candidate flow.
- Grammar-constrained decoding (GBNF/WFST).
- Policy gating (grammar, confidence, authorization, risk, mode).
- Deterministic execution authority decisions.
- Evidence packet generation and auditability.
- ASR adapter contracts with Maestro-owned semantics.

### 2.2 Out of Scope

- Free-form dictation authority.
- Long-running workflow execution (belongs to orchestration systems).
- Provider-owned command semantics.

## 3. Strategic Horizon

- Epoch 1 Foundation: deterministic command survivability and safety.
- Epoch 2 Platform: stronger policy programmability, richer adapter contracts.
- Epoch 3 Intelligence: scalable multi-lane coordination without compromising
  deterministic command control.

---

# II. Core Principles

### 1. Architectural Invariance (Control Stack)

The control stack is non-negotiable:

- Acoustic Front End.
- Constrained Decoder.
- Lexicon/Pronunciation layer.
- Grammar/Parser gate.
- Policy/Risk gate.
- Rust hot-path orchestrator.

Bypass Ban: No component may bypass grammar/policy gates for convenience.

### 2. Statelessness and Explicit State

- Process Ephemerality: Components MUST crash/restart without semantic drift.
- State Locality: Durable policy/config state MUST be explicit and recoverable.
- Memory Hygiene: In-memory state in hot paths MUST be bounded and reconstructible.

### 3. Protocol Sovereignty

- Protobuf on the wire for infrastructure (protobuf 4.25.8 with protoc).
- JSON reserved for human-facing APIs, debugging, and operator views.
- Protocol definitions are single source of truth.
- Deployment aliases are allowed, but every promoted model MUST record base model
  id/version, adapter type (LoRA/QLoRA), dataset lineage, license, and evaluation
  results in a provenance record.
- Model, tokenizer, grammar, and protobuf artifacts MUST be pinned by version and
  checksum and loaded only from approved manifests.

### 4. Future-Proofing Hooks

- Identity and capability metadata MAY evolve additively.
- Routing metadata MAY evolve additively.
- Safety middleware insertion points MUST remain explicit.

### 5. Semantic Versioning and Compatibility

- MAJOR: breaking contract/governance changes.
- MINOR: additive non-breaking capability.
- PATCH: clarifications and non-semantic refinements.

No stealth breaks in MINOR or PATCH.

### 6. Isolation and Bulkheads

Lane/session failures MUST remain localized. Noisy path behavior MUST NOT collapse
unrelated command handling.

### 7. Security by Design

- Zero trust across boundaries.
- Fail closed on safety/policy subsystem failures.
- Secure startup defaults required.

### 8. Programmable Safety

Policy behavior must remain configurable and testable with bounded execution.
Safety failures block traffic by default.

### 9. Command-as-Contract

Commands are governed intents, not free-form text blobs. Contract-first envelopes
are mandatory.

### 10. Delta-First Behavior

Prefer incremental state updates and explicit causality over full snapshots when
safe and practical.

### 11. Circuit-First Orchestration

Control flows are declared as explicit routes/policies, not hidden in ad hoc
handler coupling.

---

# III. Code Quality and Engineering Standards

1. Boring Code Manifesto: readability over cleverness.
2. Asynchronous Boundaries: no blocking I/O in hot paths.
3. Error Handling: typed, contextual, never swallowed.
4. Logging and Observability: structured logs with correlation IDs.
5. Configuration Discipline: startup validation; invalid config fails loud.
6. Deterministic State: explicit state-machine semantics in critical paths.
7. Protocol-First Definition: generated protocol code only.
8. Memory and Resource Guarantees: bounded allocations and caps.
9. Concurrency Safety and Ordering: backpressure and explicit sequencing.
10. Performance Discipline: no avoidable allocations in hot loops.
11. Interface Stability: stable internal contracts.
12. Dependency Hygiene: pinned, justified dependencies only.
13. Documentation Standards: behavior changes require doc updates.
14. Build Integrity: reproducible builds and verified artifacts.
15. Algebraic Preference: explicit control logic over opaque heuristics where
    feasible.

---

# IV. Testing Strategy and Quality Gates

## 1. TDD Standard

Specify -> Test -> Implement -> Refactor is the default workflow.

## 2. Coverage Expectations

Coverage MUST include:

- Routing and lane-selection edge cases.
- Policy and fail-closed behavior.
- Evidence packet integrity.
- Adapter compatibility and degradation.
- Protobuf envelope validation (valid, invalid, adversarial).

## 3. Test Discipline

- Unit, integration, end-to-end, regression, and adversarial test suites are
  mandatory for production readiness.
- Unit tests fast and isolated.
- Integration tests realistic.
- Flaky tests are critical bugs.
- Determinism required where controllable.

## 4. Quality Gates

No merge when protocol, policy, architecture, observability, or specification
requirements are violated.
Implementation Readiness Gate: `make helios-smoke` MUST pass before coding starts
on a feature branch, MUST pass again before merge, and MUST produce
`artifacts/reports/audio-inference-smoke.json`.
No adapter or model promotion is allowed without passing deterministic outcome,
fail-closed safety, p95 latency, false-positive, and evidence-packet contract
validation thresholds.

## 5. Automated Enforcement

CI and policy checks are mandatory enforcement mechanisms.
CI MUST enforce unit, integration, end-to-end, regression, and adversarial test
categories as required checks.

---

# V. Lifecycle and Automation

- CI/CD is the only production path.
- Immutable reproducible artifacts required.
- Supply chain security (pinning, provenance, signing/SBOM where applicable).
- Rolling compatibility and controlled deployment required.
- Canary and rollback procedures are mandatory.
- `helios-gpu-118` is frozen runtime; direct installs are prohibited.
- Dependency resolution/provisioning MUST occur only in approved provisioning
  environments with auditable change records.
- Dependency Completeness Audit is mandatory before implementation phase:
  repository MUST produce an auditable dependency list by test level
  (unit/integration/e2e/regression/adversarial), and each dependency MUST be
  marked as already present in frozen runtime, provisioned externally, or
  intentionally deferred. Hidden install assumptions are prohibited.

---

# VI. Operational Excellence

- SLOs and error budgets are explicit and enforced.
- Blameless postmortems required for severe incidents.
- Actionable on-call alerts only.
- Explicit retention and isolation of operational data.
- Graceful degradation over catastrophic failure.
- No silent recovery paths.

---

# VII. Governance and Amendment

1. Scope Protection: Command Lane remains deterministic control infrastructure.
2. Complexity Budget: major complexity increases require documented review.
3. Decision Making: constitution precedence over local convenience.
4. Amendments: must include rationale, impact, and traceability.
5. Interpretation: where ambiguous, maintainers document interpretation and
   update enforcement tooling.

---

# VIII. Performance and Hot-Path Invariants

1. Boundedness is Law: bounded queues, memory, and CPU budgets.
2. Hot-Path Constraints: no blocking operations in hot loops.
3. Throughput and Latency Behavior: deterministic degradation under load.
4. Capacity and Scaling Invariants: predictable horizontal scaling and no
   irreplaceable nodes.

---

# IX. Observability and Telemetry Contracts

1. Logs/metrics/traces are first-class requirements.
2. Telemetry contracts are versioned and stable.
3. Security and privacy rules apply to telemetry.
4. Operability requires reconstruction-capable signals.

---

# X. Data Governance and Retention

1. Data Classification: configuration, operational, history, security data.
2. Retention: explicit TTL or archival strategy required.
3. Isolation and Privacy: tenant/session scoping and least privilege.
4. Encryption and Key Management: encryption in transit/at rest and key lifecycle
   controls.

---

# XI. Internal Service Contracts and Complexity Escalation

1. Versioned internal contracts only; no hidden side channels.
2. Complexity triggers require design review and ADR records.
3. One obvious path per core concern; migration paths must sunset.
4. Governance integration with policy tooling and maintainers.

---

# XII. Glossary and Canonical Definitions

- Arqon Maestro Command Lane: deterministic voice command control system.
- Command Lane: execution-authoritative lane.
- Dictation Lane: transcription lane without execution authority.
- Degraded Command Sub-Lane: minimal emergency command vocabulary.
- Hot-Path Orchestrator: Rust real-time control component.
- EvidencePacket: auditable command execution evidence structure.
- ASR Adapter: replaceable provider integration with Maestro-owned semantics.
- Grammar Authority: Maestro-owned command language and decoding constraints.

---

**Version**: 2.2.0 | **Ratified**: 2026-03-30 | **Last Amended**: 2026-03-30

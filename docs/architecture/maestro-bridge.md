# Arqon Maestro Bridge

This document defines the runtime bridge between the Command Lane and Arqon
Maestro orchestration services.

## Bridge Responsibility

- Command Lane owns deterministic command interpretation and policy decisions.
- Arqon Maestro orchestrates capability execution after command authorization.
- Bridge calls must preserve lane context, evidence linkage, and fail-closed
  semantics.

## End-to-End Bridge Flow

1. Voice input enters Command Lane (`command_lane` or other canonical lane).
2. Grammar + policy gates produce `granted`, `refused`, or `escalated`.
3. On `granted`, a structured capability envelope is emitted to Maestro.
4. Maestro executes capability or routes to ArqonMCP.
5. Command Lane records evidence and returns operator-visible outcome.

## Required Envelope Fields

- `lane`
- `execution_authority`
- `intent`
- `policy_decision.reason`
- `evidence_packet_id` (or serialized packet reference)
- `timestamp`

## Safety Invariants

- `refused` and `escalated` decisions MUST NOT dispatch execution.
- Dictation lane traffic MUST NOT enter command execution bridge.
- Interrupt commands (`stop`, `cancel`, etc.) retain highest priority.
- Any adapter/policy uncertainty fails closed before bridge dispatch.

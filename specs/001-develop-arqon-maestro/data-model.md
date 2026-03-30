# Data Model: Arqon Maestro Command Lane

## Entities

### UtteranceEnvelope

- **Purpose**: Input unit entering lane-routing and policy flow.
- **Fields**:
  - `utterance_id` (string, unique)
  - `lane` (enum: command_lane, dictation_lane, conversation_lane,
    translation_lane, search_explore_lane, degraded_command_lane)
  - `provider_id` (string)
  - `audio_hash` (string)
  - `endpointing_metadata` (map)
  - `elapsed_ms` (integer)

### SpeechResult

- **Purpose**: Recognition output contract.
- **Fields**:
  - `transcript` (string)
  - `lane` (enum)
  - `acoustic_confidence` (float)
  - `provider_id` (string)
  - `elapsed_ms` (integer)
  - `degraded_state` (boolean)

### CommandResult

- **Purpose**: Deterministic command decision output.
- **Fields**:
  - `command` (string)
  - `intent.name` (string)
  - `policy_decision.reason` (string)
  - `execution_authority` (enum: granted/refused/escalated)
  - `evidence_packet` (embedded `EvidencePacket`)
- **Rule**: Exactly one terminal authority status per command-lane utterance.

### EvidencePacket

- **Purpose**: Immutable audit artifact for decisions.
- **Fields**:
  - `audio_hash` (string)
  - `lane` (enum)
  - `adapter_metadata` (map)
  - `confidence_adjudication` (string)
  - `policy_outcome` (string)
  - `latency_ms` (integer)
  - `timestamp` (ISO-8601)

### ConfirmationChallenge

- **Purpose**: High-impact command confirmation state.
- **Fields**:
  - `challenge_id` (string, unique)
  - `command_ref` (string)
  - `issued_at` (timestamp)
  - `expires_at` (timestamp = `issued_at + 5s`)
  - `status` (enum: pending, confirmed, auto_refused)
- **Rule**: Pending confirmation auto-transitions to `auto_refused` at 5s.

### DependencyAuditRecord

- **Purpose**: Readiness tracking by test category.
- **Fields**:
  - `test_level` (enum: unit, integration, e2e, regression, adversarial)
  - `dependency_name` (string)
  - `status` (enum: present_in_frozen_runtime, provisioned_externally, deferred)
  - `notes` (string)
- **Rule**: Implementation start blocked if any record status is `deferred`.

## State Transitions

### Command Decision

`received -> lane_routed -> grammar_checked -> policy_adjudicated -> {granted|refused|escalated}`

### High-Impact Confirmation

`pending -> confirmed`

`pending -> auto_refused` when no explicit confirmation within 5 seconds.

### Adapter Timeout Handling

If adapter processing reaches 150ms timeout threshold, state transitions to
`refused` (or `escalated` if policy requires), with evidence emitted.

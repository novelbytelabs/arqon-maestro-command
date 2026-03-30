# Arqon Maestro Command Lane

> **Status:** Active Development  
> **Architecture:** Control-First Speech System  
> **Authority Level:** High (Root) - Deterministic Action Control  

The Command Lane is the primary control system of Arqon Maestro, a Voice Operating System. Unlike generic speech recognition, the Command Lane is a **bounded control system** that ensures deterministic, operator-safe execution of voice commands.

---

## Table of Contents

1. [Overview](#overview)
2. [Tech Stack](#tech-stack)
3. [Architecture](#architecture)
4. [Lane Model](#lane-model)
5. [Command Contract](#command-contract)
6. [Grammar System](#grammar-system)
7. [Policy & Safety](#policy--safety)
8. [Rust Hot-Path Orchestrator](#rust-hot-path-orchestrator)
9. [Integration Points](#integration-points)
10. [Getting Started](#getting-started)
11. [Development Guide](#development-guide)
12. [Testing](#testing)
13. [AI Bootstrap (New Instance Checklist)](#ai-bootstrap-new-instance-checklist)
14. [Roadmap](#roadmap)

---

## Overview

### Core Principle

**The Command Lane is a control system, not a generic ASR benchmark lane.**

Command speech in Maestro must preserve Serenade/Kaldi-era controllability with modern CTC acoustic front-ends. The system prioritizes:

- **Deterministic accept/reject behavior** — commands must either be executed or explicitly rejected
- **Grammar authority** — Maestro owns command semantics, not the ASR engine
- **Bounded command language** — finite, enforceable command vocabulary
- **Fail-closed safety** — when uncertain, refuse to execute

### Command Lane vs Dictation Lane

| Aspect | Command Lane | Dictation Lane |
|--------|--------------|----------------|
| **Purpose** | Deterministic control | Free-form transcription |
| **Authority** | High (Root) | None (transcription only) |
| **Model** | Parakeet-CTC + Grammar | Qwen3-ASR |
| **Optimization** | Latency, safety, grammar match | Text accuracy, WER |
| **Output** | Executable commands | Raw text |
| **Fallback** | Degraded command sub-lane | Provider-flexible |

---

## Tech Stack

### Primary Components

| Component | Technology | Role |
|-----------|------------|------|
| **Acoustic Model** | Parakeet-CTC | First candidate for speech-to-text |
| **Grammar Engine** | WFST / GBNF | Deterministic command parsing |
| **Constrained Decoder** | WFST/Flashlight-class | Bounded decoding |
| **Lexicon Layer** | Maestro-owned mappings | Pronunciation control |
| **Policy Engine** | Maestro services | Authorization, escalation, fail-closed |
| **Hot-Path Orchestrator** | Rust | Low-latency audio processing |
| **Dynamic Lexicon** | Helios-Engine (Incremental Nyström Engine) | Runtime lexicon updates |

### Language & Frameworks

- **Core Orchestration:** Rust (memory safety, explicit concurrency, predictable fail-closed)
- **Grammar Definition:** GBNF (Grammatical Backus-Naur Form), WFST (Weighted Finite-State Transducers)
- **ASR Adapters:** Pluggable provider contracts
- **Runtime:** Local-first (no remote dependency for core commands)

---

## Architecture

### Control-First Stack

```
┌─────────────────────────────────────────────────────────────────┐
│                    Maestro Command Platform                     │
├─────────────────────────────────────────────────────────────────┤
│  1. Acoustic Front End      │ Parakeet-CTC (or equivalent)    │
├─────────────────────────────────────────────────────────────────┤
│  2. Constrained Decoder     │ WFST/Flashlight-class            │
├─────────────────────────────────────────────────────────────────┤
│  3. Lexicon/Pronunciation    │ Maestro-owned mappings           │
├─────────────────────────────────────────────────────────────────┤
│  4. Grammar/Parser Gate      │ In-grammar accept / OOG reject  │
├─────────────────────────────────────────────────────────────────┤
│  5. Policy/Risk Gate         │ Authorization, escalation,       │
│                              │ interrupt, fail-closed            │
├─────────────────────────────────────────────────────────────────┤
│  6. Rust Hot-Path            │ Audio ingress, lane routing,      │
│     Orchestrator             │ confidence adjudication           │
└─────────────────────────────────────────────────────────────────┘
```

### Ownership Model

```
┌─────────────────────────────────────────────────────────────────┐
│                     Maestro Command Platform                    │
│                     (Owns command semantics)                     │
├─────────────────────────────────────────────────────────────────┤
│  - Command language definition                                  │
│  - Grammar/compiler authority                                   │
│  - Lexicon/pronunciation control                               │
│  - Routing/policy/safety enforcement                           │
│  - Telemetry and provenance                                     │
│  - Engine adapter boundaries                                    │
├─────────────────────────────────────────────────────────────────┤
│                     Speech Engines = Adapters                   │
│                     (Replaceable, Maestro-owned semantics)      │
└─────────────────────────────────────────────────────────────────┘
```

---

## Lane Model

Maestro uses **five canonical interaction lanes** + one optional degraded sub-lane:

### A. Command Lane (`command_lane`)
- **Purpose:** Deterministic operating commands, reflex-adjacent recognition
- **Optimizes:** Latency, canonical command survivability, low ambiguity
- **Characteristics:** Local-first, hot-path compatible, fast endpointing

### B. Dictation Lane (`dictation_lane`)
- **Purpose:** Free text entry, code comments, prose
- **Optimizes:** Textual accuracy, punctuation, longer utterance handling
- **Characteristics:** Isolated from command execution authority

### C. Conversation Lane (`conversation_lane`)
- **Purpose:** Spoken back-and-forth with Nexus
- **Architecture:** `ASR → Nexus → TTS` (cascaded, transcript-first)
- **Characteristics:** Audit-first, explicit reasoning boundaries

### D. Translation Lane (`translation_lane`)
- **Purpose:** Speech-to-text translation, multilingual workflows
- **Characteristics:** Explicit language handling, bounded translate/execute disambiguation

### E. Search/Explore Lane (`search_explore_lane`)
- **Purpose:** Retrieval and exploration over docs, code, system state
- **Architecture:** Structured intent + tool routing + provenance
- **Characteristics:** Grammar-and-tool driven, not freeform

### F. Degraded Command Sub-Lane
- **Purpose:** Emergency fallback when primary command lane fails
- **Vocabulary:** stop, cancel, mute, pause, wake, sleep, yes, no, undo, repeat
- **Characteristics:** Tiny, reliable, local-only, bias toward refusal

### Lane Routing Rules

```
command mode     → command_lane
chooser mode     → command_lane  
repair mode      → command_lane
dictation mode   → dictation_lane
conversation     → conversation_lane
translation      → translation_lane
exploration      → search_explore_lane
```

---

## Command Contract

### Input Contract

Every speech result must include:

```typescript
interface SpeechResult {
  transcript: string;           // Raw transcription
  partials?: string[];          // Partial results if available
  lane: LaneType;               // Which lane processed this
  acoustic_confidence: number;  // ASR confidence score
  token_uncertainty?: number;   // Token-level uncertainty
  speaker_metadata?: SpeakerInfo;
  endpointing_metadata: EndpointInfo;
  provider_id: string;          // Which ASR provider
  elapsed_ms: number;          // Processing time
  degraded_state: boolean;      // Is system degraded?
}
```

### Output Contract

Command results must include:

```typescript
interface CommandResult {
  command: string;              // Parsed command
  intent: Intent;               // Structured intent
  parameters: Record<string, any>;
  policy_decision: PolicyDecision;
  execution_authority: 'granted' | 'refused' | 'escalated';
  evidence_packet: EvidencePacket;
}
```

### Evidence Packet

Every command execution generates:

```typescript
interface EvidencePacket {
  audio_hash: string;
  lane: LaneType;
  adapter_metadata: AdapterMeta;
  confidence_adjudication: string;
  policy_outcome: PolicyOutcome;
  latency_ms: number;
  timestamp: ISO8601;
}
```

---

## Grammar System

### Grammar Types

1. **GBNF (Grammatical Backus-Naur Form)**
   - Human-readable grammar definition
   - Used for command structure definition
   - Example: `command = "focus" (terminal | window | application)`

2. **WFST (Weighted Finite-State Transducers)**
   - Optimized for runtime decoding
   - Enables constrained decoding
   - Phonetic/pronunciation integration

### Grammar Compilation Pipeline

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  GBNF Source │ ──► │   Compiler   │ ──► │    WFST     │
└──────────────┘     └──────────────┘     └──────────────┘
                                                    │
                     ┌──────────────────────────────┘
                     ▼
              ┌──────────────┐
              │  Decoder     │
              │  Constraints │
              └──────────────┘
```

### Command Corpus Categories

| Category | Examples |
|----------|----------|
| **Reflex** | stop, cancel, undo, mute |
| **Core Commands** | focus terminal, run cargo build, open definition |
| **Phonetic Hazards** | Commands with similar phonetic profiles |
| **Dictation Controls** | enter dictation, new paragraph, etc. |

---

## Policy & Safety

### Policy Layers

1. **Grammar Gate** — Is this in-grammar?
2. **Confidence Gate** — Is confidence above threshold?
3. **Authorization Gate** — Does speaker have permission?
4. **Risk Gate** — Is this a high-impact action?
5. **Mode Gate** — Is this allowed in current mode?

### Fail-Closed Behavior

When policy confidence is insufficient:
- **Default to REFUSE** — never execute uncertain commands
- **Escalate to chooser** — human decision for ambiguous cases
- **Preserve evidence** — log for audit and learning

### High-Impact Action Requirements

For dangerous commands (file deletion, system changes):
- Speaker-aware authorization checks
- Explicit confirmation required
- Mode-aware capability constraints

---

## Rust Hot-Path Orchestrator

The Rust orchestrator is the real-time bridge between acoustic perception and governed command control.

### Responsibilities

1. **Audio Ingress & Endpointing**
   - Stream PCM frames
   - Run VAD/endpointing
   - Preserve timestamped chunk boundaries

2. **Lane Routing & Adapter Lifecycle**
   - Route utterances to command vs dictation paths
   - Manage adapter health and fallback
   - Keep interrupt vocabulary available under degradation

3. **Policy & Confidence Adjudication**
   - Fuse confidence, grammar, and risk signals
   - Route low-trust outcomes to clarification/escalation/refusal
   - Never bypass policy gates for high-risk actions

4. **Interrupt Authority**
   - Prioritize stop/cancel commands
   - Keep interrupt path locally available
   - Deterministic kill signaling to active flows

5. **Evidence & Provenance**
   - Emit evidence packets per utterance
   - Audio hash, lane metadata, confidence rationale
   - Latency and policy outcome tracking

### Non-Functional Requirements

- **Latency:** Must fit hot-path budget (~200ms command acceptance)
- **Memory:** Predictable memory usage, no GC pauses
- **Concurrency:** Explicit async handling
- **Safety:** Fail-closed by default

---

## Integration Points

### With ArqonMCP

```
1. Human speaks to Maestro
2. Maestro parses command into structured envelope
3. Maestro submits capability request to ArqonMCP
4. ArqonMCP routes via speed ladder and capability fabric
5. ArqonMCP executes/composes workflow
6. Maestro mediates confirmations, progress, escalation
```

**Key Rule:** Maestro invokes and mediates workflows; ArqonMCP orchestrates them.

### With Nexus

- Nexus refines intent before Maestro execution
- Nexus provides personal context
- Maestro owns deterministic operating control
- Conversation lane: `ASR → Nexus → TTS`

### With Other Lanes

- Dictation lane isolated from command authority
- Lane switching must not stall command acceptance
- Degraded command sub-lane activates on primary failure

---

## Getting Started

### Prerequisites

```bash
# Rust toolchain
rustup default stable
rustup target add x86_64-unknown-linux-gnu

# For ASR integration
# - Parakeet-CTC model files
# - WFST decoder library (Flashlight or equivalent)

# Build tools
cargo >= 1.70
```

### Initial Setup

```bash
# Clone the repository
git clone https://github.com/arqon/arqon-maestro-command.git
cd arqon-maestro-command

# Install dependencies
cargo build

# Run tests
cargo test

# Run with sample commands
cargo run --example basic_command
```

### Project Structure

```
arqon-maestro-command/
├── src/
│   ├── main.rs              # Entry point
│   ├── orchestrator/       # Rust hot-path orchestration
│   ├── grammar/            # GBNF/WFST grammar system
│   ├── policy/             # Policy engine
│   ├── adapters/           # ASR engine adapters
│   ├── lexicon/            # Lexicon management
│   └── evidence/           # Evidence packet generation
├── grammars/               # GBNF grammar definitions
├── models/                 # ASR model files
├── tests/                  # Integration tests
├── docs/                   # Architecture docs
└── README.md
```

---

## Development Guide

### Running the Command Lane

```bash
# Development mode with logging
cargo run -- --log-level debug

# Release mode
cargo run --release

# With specific ASR provider
cargo run -- --provider parakeet-ctc
```

### Adding New Commands

1. Define in GBNF grammar:
   ```bnf
   command = "newcommand" target
   target = "file" | "folder" | "project"
   ```

2. Compile to WFST:
   ```bash
   cargo run --bin grammar-compiler -- grammars/newcommands.gbnf
   ```

3. Add policy rules in `src/policy/`

4. Add tests in `tests/commands/`

### Testing Commands

```bash
# Unit tests
cargo test --lib

# Integration tests
cargo test --test integration

# Command corpus tests
cargo test --test corpus

# Latency benchmarks
cargo bench
```

---

## Testing

### Benchmark Dimensions

| Metric | Description |
|--------|-------------|
| p50 latency | 50th percentile command response |
| p95 latency | 95th percentile command response |
| exact-match rate | Commands recognized correctly |
| false-positive rate | Dangerous commands wrongly accepted |
| grammar compatibility | In-grammar command survival |
| OOG rejection rate | Out-of-grammar rejection accuracy |

### Test Corpora

1. **Reflex Corpus:** stop, cancel, undo, mute
2. **Core Command Corpus:** focus, open, run, next, previous...
3. **Phonetic Hazard Corpus:** Known risky command pairs
4. **Dictation Corpus:** Prose, code comments, notes
5. **Degraded Corpus:** Reduced vocabulary survival

---

## AI Bootstrap (New Instance Checklist)

Use this checklist for every new AI/dev instance on this repo.

### 1) Environment and Version Guardrails

- Primary runtime is frozen `helios-gpu-118`.
- Do not install or upgrade packages directly in `helios-gpu-118`.
- Keep core pins immutable:
  - `torch==2.10.0`
  - `numpy==2.2.5`
  - `protobuf==4.25.8`
  - `protoc==29.3`
- Any dependency resolution/provisioning happens only in an approved provisioning
  environment, with auditable change records.

### 2) One-Command Helios Sanity Gate

Run this before implementation and before merge:

```bash
make helios-smoke
```

This executes:
- runtime hygiene gate
- protobuf contract generation/validation
- bridge smoke check
- audio inference smoke + evidence emission

Expected artifact:
- `artifacts/reports/audio-inference-smoke.json`

### 3) Contract and Safety Invariants

- Command lane is deterministic: each command yields `granted`, `refused`, or
  `escalated`.
- Fail closed on uncertainty, adapter failure, or policy ambiguity.
- Grammar/policy gates are mandatory and must not be bypassed.
- Dictation lane has zero command execution authority.
- Interrupt authority (`stop`, `cancel`, etc.) stays available under degradation.

### 4) Wire Format and Artifact Integrity

- Protobuf is authoritative for infrastructure/machine paths.
- JSON is for human-facing APIs/debug views only.
- Model/tokenizer/grammar/protobuf artifacts must be pinned by version + checksum.
- Load artifacts only from approved manifests.
- Preserve model provenance for promoted aliases: base model/version, adapter type
  (LoRA/QLoRA), dataset lineage, license, and eval results.

### 5) Test Expectations by Level

- Unit: parsing, policy decisions, lane routing logic.
- Integration: adapter boundaries, grammar + policy + orchestrator interactions.
- End-to-end: utterance -> lane -> command decision -> evidence packet.
- Regression: command corpus stability + contract compatibility.
- Adversarial: OOG input, phonetic hazards, malformed payloads, timeout/failure
  paths; verify fail-closed behavior.

---

## Roadmap

### Phase 1: Core Infrastructure
- [ ] Rust hot-path orchestrator baseline
- [ ] Parakeet-CTC adapter integration
- [ ] Basic GBNF grammar compiler
- [ ] Policy engine skeleton
- [ ] Evidence packet system

### Phase 2: Command Language
- [ ] Complete command grammar
- [ ] WFST constrained decoder integration
- [ ] Lexicon management system
- [ ] Confidence adjudication

### Phase 3: Safety & Policy
- [ ] Authorization framework
- [ ] Fail-closed behavior
- [ ] Degraded command sub-lane
- [ ] Speaker identity integration

### Phase 4: Production
- [ ] Performance optimization
- [ ] Comprehensive testing
- [ ] Documentation
- [ ] Release v1.0

---

## References

- [Command Lane Architecture Memo](./docs/command-lane-architecture-memo.md)
- [Lane Separation Strategy](./docs/lane-separation-strategy.md)
- [STT Strategy By Lane](./docs/stt-strategy-by-lane.md)
- [Rust Hot-Path Orchestration](./docs/rust-hot-path-orchestration.md)
- [Maestro Actuation Stack](./docs/maestro-actuation-and-control-stack.md)
- [Nexus/Maestro/ArqonMCP Boundary](./docs/nexus-maestro-arqonmcp-boundary.md)

---

## License

This project is part of Arqon Maestro. See parent repository for license details.

---

**Last Updated:** 2026-03-30  
**Architecture Status:** Canonical  
**Version:** 0.2.0

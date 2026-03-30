# Research: Arqon Maestro Command Lane

## Decision: Runtime Immutability

- **Decision**: Keep `helios-gpu-118` frozen for runtime execution.
- **Rationale**: Prevents dependency drift in deterministic command-safety paths.
- **Alternatives considered**:
  - Mutable runtime installs (rejected: reproducibility risk)
  - Per-developer divergent environments (rejected: validation inconsistency)

## Decision: Readiness Gate Timing

- **Decision**: Require `make helios-smoke` before coding and before merge.
- **Rationale**: Catches runtime/contract regressions at earliest practical points.
- **Alternatives considered**:
  - Merge-only gate (rejected: delayed failure detection)

## Decision: Adapter Timeout

- **Decision**: Fail closed at adapter timeout >= 150ms.
- **Rationale**: Balances responsiveness and command-lane p95 budget (<200ms).
- **Alternatives considered**:
  - 120ms (rejected: higher false-refusal risk)
  - 180ms (rejected: reduced headroom for policy/evidence stages)

## Decision: High-Impact Confirmation Timeout

- **Decision**: Auto-refuse after 5 seconds without explicit confirmation.
- **Rationale**: Strong safety posture without impractical operator response window.
- **Alternatives considered**:
  - 3s (rejected: too aggressive for human response)
  - 8s (rejected: larger accidental-execution exposure window)

## Decision: False-Positive Threshold

- **Decision**: High-impact command false-positive ceiling <= 0.1%.
- **Rationale**: Safety-critical threshold that remains operationally achievable.
- **Alternatives considered**:
  - <=0.2% (rejected: weaker safety margin)
  - <=0.05% (rejected: high tuning risk early-phase)

## Decision: Dependency Audit Enforcement

- **Decision**: Hard-block implementation start if any dependency remains
  `deferred`.
- **Rationale**: Eliminates hidden install assumptions and downstream rework.
- **Alternatives considered**:
  - Allow deferrals for non-critical suites (rejected: policy ambiguity)
  - ADR exception path (rejected: weakens deterministic readiness gate)

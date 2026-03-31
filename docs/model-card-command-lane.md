# Model Card: Arqon Maestro Command Lane

## Model Identity

- Name: Command Lane Acoustic + Grammar Control Stack
- Runtime: `helios-gpu-118`
- Primary acoustic path: Parakeet TDT/CTC family (adapter-based)
- Command semantics authority: Maestro-owned grammar/policy, not provider-owned

## Intended Use

- Deterministic operator command execution in `command_lane`
- Safety-first command refusal under uncertainty
- Auditable command decisions with evidence packet emission

## Out-of-Scope Use

- Free-form dictation authority
- Unbounded conversational autonomy
- Provider-defined command semantics bypassing Maestro grammar/policy

## Key Safety Controls

- Grammar gate: bounded vocabulary and patterns
- Policy gate: auth + confidence + risk checks
- Fail-closed default on uncertainty, timeout, or policy failure
- Interrupt priority (`stop`, `cancel`) preserved
- Dictation isolation from command execution

## Performance/Quality Targets

- p95 command decision latency < 200ms under BP-001
- Adapter timeout fail-closed at <=150ms
- High-impact false-positive threshold <=0.1%
- Confirmation timeout auto-refusal at 5 seconds

## Evaluation and Evidence

- Unit/integration/e2e/regression/adversarial suites required
- Runtime readiness via `make helios-smoke`
- Evidence artifacts generated in `artifacts/reports/`

## Limitations

- Behavior depends on approved grammar and policy configuration versions
- Requires frozen runtime and approved provisioning path for reproducibility
- Not intended for direct production deployment without CI gate compliance

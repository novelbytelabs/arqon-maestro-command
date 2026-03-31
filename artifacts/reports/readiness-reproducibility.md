# Readiness Reproducibility Replay

- Replay Timestamp (UTC): 2026-03-31T01:15:50Z
- Replay Operator: novyteai <novyte00@gmail.com>
- Branch: 001-develop-arqon-maestro
- Baseline Commit: eea7f64
- Runtime Identity: helios-gpu-118

## Fresh-Instance Replay Steps

1.  -> PASS
2.  -> PASS
3.  -> PASS
4. ./ops/helios/generate_contracts.sh
PASS: generated protobuf descriptor: /home/irbsurfer/Projects/arqon/arqon-maestro-command/ops/helios/generated/command_contracts.desc
./ops/helios/runtime_hygiene_gate.sh
./ops/helios/helios-run.sh python ops/helios/bridge_smoke_check.py
PASS: protobuf-backed contract validation
Loading model from: artifacts/models/parakeet-tdt_ctc-1.1b/parakeet-tdt_ctc-1.1b.nemo
[NeMo I 2026-03-30 21:16:16 mixins:176] Tokenizer SentencePieceTokenizer initialized with 1024 tokens
[NeMo I 2026-03-30 21:16:18 features:305] PADDING: 0
[NeMo I 2026-03-30 21:16:27 rnnt_models:226] Using RNNT Loss : tdt
    Loss tdt_kwargs: {'fastemit_lambda': 0.0, 'clamp': -1.0, 'durations': [0, 1, 2, 3, 4], 'sigma': 0.02, 'omega': 0.1}
[NeMo I 2026-03-30 21:16:27 rnnt_models:226] Using RNNT Loss : tdt
    Loss tdt_kwargs: {'fastemit_lambda': 0.0, 'clamp': -1.0, 'durations': [0, 1, 2, 3, 4], 'sigma': 0.02, 'omega': 0.1}
[NeMo I 2026-03-30 21:16:27 rnnt_models:226] Using RNNT Loss : tdt
    Loss tdt_kwargs: {'fastemit_lambda': 0.0, 'clamp': -1.0, 'durations': [0, 1, 2, 3, 4], 'sigma': 0.02, 'omega': 0.1}
[NeMo I 2026-03-30 21:16:32 save_restore_connector:275] Model EncDecHybridRNNTCTCBPEModel was successfully restored from /home/irbsurfer/Projects/arqon/arqon-maestro-command/artifacts/models/parakeet-tdt_ctc-1.1b/parakeet-tdt_ctc-1.1b.nemo.
PASS: loaded NeMo ASR model class=EncDecHybridRNNTCTCBPEModel
PASS: bridge smoke check

./ops/helios/helios-run.sh python ops/helios/audio_inference_smoke.py
[NeMo I 2026-03-30 21:16:51 mixins:176] Tokenizer SentencePieceTokenizer initialized with 1024 tokens
[NeMo I 2026-03-30 21:16:53 features:305] PADDING: 0
[NeMo I 2026-03-30 21:17:02 rnnt_models:226] Using RNNT Loss : tdt
    Loss tdt_kwargs: {'fastemit_lambda': 0.0, 'clamp': -1.0, 'durations': [0, 1, 2, 3, 4], 'sigma': 0.02, 'omega': 0.1}
[NeMo I 2026-03-30 21:17:02 rnnt_models:226] Using RNNT Loss : tdt
    Loss tdt_kwargs: {'fastemit_lambda': 0.0, 'clamp': -1.0, 'durations': [0, 1, 2, 3, 4], 'sigma': 0.02, 'omega': 0.1}
[NeMo I 2026-03-30 21:17:03 rnnt_models:226] Using RNNT Loss : tdt
    Loss tdt_kwargs: {'fastemit_lambda': 0.0, 'clamp': -1.0, 'durations': [0, 1, 2, 3, 4], 'sigma': 0.02, 'omega': 0.1}
[NeMo I 2026-03-30 21:17:08 save_restore_connector:275] Model EncDecHybridRNNTCTCBPEModel was successfully restored from /home/irbsurfer/Projects/arqon/arqon-maestro-command/artifacts/models/parakeet-tdt_ctc-1.1b/parakeet-tdt_ctc-1.1b.nemo.
[NeMo I 2026-03-30 21:17:08 rnnt_models:226] Using RNNT Loss : tdt
    Loss tdt_kwargs: {'fastemit_lambda': 0.0, 'clamp': -1.0, 'durations': [0, 1, 2, 3, 4], 'sigma': 0.02, 'omega': 0.1}
PASS: audio inference smoke (951 ms)
Wrote: artifacts/reports/audio-inference-smoke.json -> PASS

## Replay Outputs

- Dependency audit: 
- Dependency audit summary: 
- Audio inference smoke: 

## Result

Readiness runbook reproduced without additional in-environment installs.

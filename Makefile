.PHONY: helios-smoke

helios-smoke:
	./ops/helios/generate_contracts.sh
	./ops/helios/runtime_hygiene_gate.sh
	./ops/helios/helios-run.sh python ops/helios/bridge_smoke_check.py
	./ops/helios/helios-run.sh python ops/helios/audio_inference_smoke.py


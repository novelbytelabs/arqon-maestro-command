.PHONY: helios-smoke test-unit test-integration test-e2e test-regression test-adversarial contracts-check evidence-schema-check

helios-smoke:
	./ops/helios/generate_contracts.sh
	./ops/helios/runtime_hygiene_gate.sh
	./ops/helios/helios-run.sh python ops/helios/bridge_smoke_check.py
	./ops/helios/helios-run.sh python ops/helios/audio_inference_smoke.py

test-unit:
	python -m pytest tests/unit -q

test-integration:
	python -m pytest tests/integration -q

test-e2e:
	python -m pytest tests/e2e -q

test-regression:
	python -m pytest tests/regression -q

test-adversarial:
	python -m pytest tests/adversarial -q

contracts-check:
	python ops/helios/protobuf_contracts.py

evidence-schema-check:
	python -c "print('evidence schema check placeholder until validator is implemented')"

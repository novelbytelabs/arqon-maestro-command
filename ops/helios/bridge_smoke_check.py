#!/usr/bin/env python3
import json
import sys
from pathlib import Path

from protobuf_contracts import load_contract_classes


def require_present(name: str, value):
    if value in ("", None):
        raise SystemExit(f"FAIL: {name} is required")


def add_generated_path() -> None:
    helios_ops = Path("ops/helios").resolve()
    if str(helios_ops) not in sys.path:
        sys.path.insert(0, str(helios_ops))


def validate_protobuf_contracts() -> None:
    add_generated_path()

    try:
        classes = load_contract_classes()
    except Exception as exc:
        raise SystemExit(f"FAIL: protobuf contract load failed: {exc}")

    SpeechResult = classes["SpeechResult"]
    CommandResult = classes["CommandResult"]
    EvidencePacket = classes["EvidencePacket"]
    Intent = classes["Intent"]
    PolicyDecision = classes["PolicyDecision"]

    speech = SpeechResult(
        transcript="focus terminal",
        partials=["focus", "focus terminal"],
        lane="command_lane",
        acoustic_confidence=0.96,
        token_uncertainty=0.04,
        provider_id="nvidia/parakeet-tdt_ctc-1.1b",
        elapsed_ms=124,
        degraded_state=False,
    )
    speech.endpointing_metadata["eou"] = "true"

    evidence = EvidencePacket(
        audio_hash="sha256:demo",
        lane="command_lane",
        confidence_adjudication="accepted",
        policy_outcome="granted",
        latency_ms=124,
        timestamp="2026-03-30T00:00:00Z",
    )
    evidence.adapter_metadata["model"] = "parakeet-tdt_ctc-1.1b"

    command = CommandResult(
        command="focus terminal",
        intent=Intent(name="focus_terminal"),
        policy_decision=PolicyDecision(reason="in_grammar_high_conf"),
        execution_authority="granted",
        evidence_packet=evidence,
    )

    # Contract checks backed by protobuf schema + basic business constraints.
    require_present("SpeechResult.transcript", speech.transcript)
    require_present("SpeechResult.lane", speech.lane)
    require_present("SpeechResult.provider_id", speech.provider_id)
    if speech.elapsed_ms <= 0:
        raise SystemExit("FAIL: SpeechResult.elapsed_ms must be > 0")

    require_present("CommandResult.command", command.command)
    require_present("CommandResult.intent.name", command.intent.name)
    require_present(
        "CommandResult.execution_authority", command.execution_authority
    )

    require_present("EvidencePacket.audio_hash", evidence.audio_hash)
    require_present("EvidencePacket.lane", evidence.lane)
    require_present("EvidencePacket.timestamp", evidence.timestamp)
    if evidence.latency_ms <= 0:
        raise SystemExit("FAIL: EvidencePacket.latency_ms must be > 0")

    # Serialize/parse roundtrip to guarantee schema compatibility.
    speech_roundtrip = SpeechResult()
    speech_roundtrip.ParseFromString(speech.SerializeToString())
    command_roundtrip = CommandResult()
    command_roundtrip.ParseFromString(command.SerializeToString())
    evidence_roundtrip = EvidencePacket()
    evidence_roundtrip.ParseFromString(evidence.SerializeToString())

    if speech_roundtrip.transcript != speech.transcript:
        raise SystemExit("FAIL: SpeechResult protobuf roundtrip mismatch")
    if command_roundtrip.intent.name != command.intent.name:
        raise SystemExit("FAIL: CommandResult protobuf roundtrip mismatch")
    if evidence_roundtrip.audio_hash != evidence.audio_hash:
        raise SystemExit("FAIL: EvidencePacket protobuf roundtrip mismatch")

    print("PASS: protobuf-backed contract validation")


def smoke_load_parakeet() -> None:
    try:
        from nemo.collections.asr.models import ASRModel
    except Exception as exc:
        raise SystemExit(f"FAIL: NeMo import failed: {exc}")

    manifest_path = Path("artifacts/manifests/parakeet-tdt_ctc-1.1b.manifest.json")
    if not manifest_path.exists():
        raise SystemExit("FAIL: manifest missing for model smoke")

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    nemo_files = [
        entry["local"]
        for entry in manifest.get("artifacts", [])
        if entry["local"].endswith(".nemo")
    ]
    if not nemo_files:
        raise SystemExit("FAIL: no .nemo artifact found in manifest")

    model_path = nemo_files[0]
    print(f"Loading model from: {model_path}")
    model = ASRModel.restore_from(model_path, map_location="cpu")
    print(f"PASS: loaded NeMo ASR model class={model.__class__.__name__}")


def main() -> None:
    validate_protobuf_contracts()
    smoke_load_parakeet()
    print("PASS: bridge smoke check")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
import hashlib
import json
import math
import os
import struct
import sys
import time
import wave
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

from protobuf_contracts import load_contract_classes


def add_generated_path() -> None:
    helios_ops = Path("ops/helios").resolve()
    if str(helios_ops) not in sys.path:
        sys.path.insert(0, str(helios_ops))


def sha256sum(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def write_sine_wav(path: Path, sample_rate: int = 16000, seconds: float = 1.0) -> None:
    num_samples = int(sample_rate * seconds)
    freq = 440.0
    amp = 0.2

    path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(path), "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        for i in range(num_samples):
            v = amp * math.sin(2.0 * math.pi * freq * i / sample_rate)
            wf.writeframesraw(struct.pack("<h", int(v * 32767)))


def parse_transcript(result) -> str:
    if isinstance(result, list) and result:
        first = result[0]
        if isinstance(first, str):
            return first
        if hasattr(first, "text"):
            return str(first.text)
        return str(first)
    return ""


def ensure_numpy_sctypes_compat() -> None:
    # NeMo 2.1.x still touches np.sctypes, removed in NumPy 2.x.
    if hasattr(np, "sctypes"):
        return

    np.sctypes = {
        "int": [np.int8, np.int16, np.int32, np.int64],
        "uint": [np.uint8, np.uint16, np.uint32, np.uint64],
        "float": [np.float16, np.float32, np.float64],
        "complex": [np.complex64, np.complex128],
        "others": [np.bool_, np.object_, np.str_, np.bytes_],
    }


def main() -> None:
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

    try:
        from nemo.collections.asr.models import ASRModel
    except Exception as exc:
        raise SystemExit(f"FAIL: NeMo import failed: {exc}")

    ensure_numpy_sctypes_compat()

    manifest_path = Path("artifacts/manifests/parakeet-tdt_ctc-1.1b.manifest.json")
    if not manifest_path.exists():
        raise SystemExit("FAIL: manifest missing")

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    nemo_files = [
        entry["local"]
        for entry in manifest.get("artifacts", [])
        if entry["local"].endswith(".nemo")
    ]
    if not nemo_files:
        raise SystemExit("FAIL: no .nemo file in manifest")

    model_path = nemo_files[0]
    wav_path = Path("artifacts/reports/smoke_input.wav")
    write_sine_wav(wav_path)

    model = ASRModel.restore_from(model_path, map_location="cpu")

    start = time.perf_counter()
    output = model.transcribe(audio=[str(wav_path)], batch_size=1)
    elapsed_ms = int((time.perf_counter() - start) * 1000)

    transcript = parse_transcript(output)
    audio_hash = f"sha256:{sha256sum(wav_path)}"
    now_iso = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace(
        "+00:00", "Z"
    )

    speech = SpeechResult(
        transcript=transcript,
        lane="command_lane",
        acoustic_confidence=0.0,
        provider_id="nvidia/parakeet-tdt_ctc-1.1b",
        elapsed_ms=max(elapsed_ms, 1),
        degraded_state=False,
    )
    speech.endpointing_metadata["smoke"] = "true"

    known_commands = {"focus terminal", "stop", "cancel", "mute", "pause"}
    cleaned = transcript.strip().lower()
    if cleaned in known_commands:
        policy_reason = "in_grammar"
        execution_authority = "granted"
    else:
        # Fail-closed default for unknown/empty transcript.
        policy_reason = "out_of_grammar_or_uncertain"
        execution_authority = "refused"

    evidence = EvidencePacket(
        audio_hash=audio_hash,
        lane="command_lane",
        confidence_adjudication="smoke_unscored",
        policy_outcome=execution_authority,
        latency_ms=max(elapsed_ms, 1),
        timestamp=now_iso,
    )
    evidence.adapter_metadata["model"] = "parakeet-tdt_ctc-1.1b"

    command = CommandResult(
        command=cleaned,
        intent=Intent(name=cleaned.replace(" ", "_") or "none"),
        policy_decision=PolicyDecision(reason=policy_reason),
        execution_authority=execution_authority,
        evidence_packet=evidence,
    )

    # Schema-backed roundtrip checks.
    for msg_cls, msg in (
        (SpeechResult, speech),
        (CommandResult, command),
        (EvidencePacket, evidence),
    ):
        parsed = msg_cls()
        parsed.ParseFromString(msg.SerializeToString())

    max_latency_ms = int(os.environ.get("MAX_SMOKE_LATENCY_MS", "10000"))
    if elapsed_ms > max_latency_ms:
        raise SystemExit(
            f"FAIL: inference latency {elapsed_ms}ms exceeds MAX_SMOKE_LATENCY_MS={max_latency_ms}"
        )

    report = {
        "model_path": model_path,
        "input_wav": str(wav_path),
        "elapsed_ms": elapsed_ms,
        "max_smoke_latency_ms": max_latency_ms,
        "transcript": transcript,
        "execution_authority": execution_authority,
        "policy_reason": policy_reason,
        "evidence_packet": {
            "audio_hash": audio_hash,
            "lane": evidence.lane,
            "policy_outcome": evidence.policy_outcome,
            "latency_ms": evidence.latency_ms,
            "timestamp": evidence.timestamp,
        },
    }

    out_path = Path("artifacts/reports/audio-inference-smoke.json")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

    print(f"PASS: audio inference smoke ({elapsed_ms} ms)")
    print(f"Wrote: {out_path}")


if __name__ == "__main__":
    main()

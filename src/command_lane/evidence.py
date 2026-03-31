import json
from datetime import datetime, timezone


def build_evidence_packet(
    audio_hash: str,
    lane: str,
    policy_outcome: str,
    latency_ms: int,
    confidence_adjudication: str = "",
    adapter_metadata: dict | None = None,
) -> dict:
    return {
        "audio_hash": audio_hash,
        "lane": lane,
        "adapter_metadata": adapter_metadata or {},
        "confidence_adjudication": confidence_adjudication,
        "policy_outcome": policy_outcome,
        "latency_ms": int(latency_ms),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


def serialize_evidence_packet(packet: dict) -> str:
    return json.dumps(packet, sort_keys=True)

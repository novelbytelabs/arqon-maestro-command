from src.command_lane.evidence import build_evidence_packet


_EVIDENCE_STORE: dict[str, dict] = {}


def store_evidence(evidence_id: str, packet: dict) -> None:
    _EVIDENCE_STORE[evidence_id] = packet


def get_evidence(evidence_id: str) -> dict:
    if evidence_id not in _EVIDENCE_STORE:
        _EVIDENCE_STORE[evidence_id] = build_evidence_packet(
            audio_hash="unknown",
            lane="command_lane",
            policy_outcome="unknown",
            latency_ms=0,
        )
    return _EVIDENCE_STORE[evidence_id]

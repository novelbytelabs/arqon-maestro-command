from src.command_lane.types import Lane


def build_speech_result(payload: dict) -> dict:
    lane = payload.get("lane", Lane.COMMAND.value)
    return {
        "transcript": str(payload.get("transcript", "")),
        "lane": lane,
        "acoustic_confidence": float(payload.get("acoustic_confidence", 0.0)),
        "provider_id": str(payload.get("provider_id", "unknown")),
        "elapsed_ms": int(payload.get("elapsed_ms", 0)),
        "degraded_state": lane == Lane.DEGRADED_COMMAND.value,
    }

from src.command_lane.dictation_guard import block_command_path_for_dictation
from src.command_lane.errors import FailClosedError
from src.command_lane.provenance import build_lane_provenance
from src.command_lane.router import route_utterance
from src.command_lane.types import Lane


def submit_utterance(payload: dict) -> dict:
    transcript = str(payload.get("transcript", ""))
    selected_lane = str(payload.get("lane", "")).strip()
    provider_id = str(payload.get("provider_id", "unknown"))
    elapsed_ms = int(payload.get("elapsed_ms", 0))
    confidence = float(payload.get("acoustic_confidence", 0.0))
    previous_lane = payload.get("previous_lane")

    decision = route_utterance(selected_lane)
    provenance = build_lane_provenance(decision.lane, previous_lane=previous_lane)

    response = {
        "transcript": transcript,
        "lane": decision.lane.value,
        "acoustic_confidence": confidence,
        "provider_id": provider_id,
        "elapsed_ms": elapsed_ms,
        "degraded_state": decision.lane == Lane.DEGRADED_COMMAND,
        "lane_provenance": provenance,
    }

    try:
        block_command_path_for_dictation(decision.lane)
    except FailClosedError:
        response["command_path_blocked"] = True

    return response

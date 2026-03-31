from datetime import datetime, timezone

from src.command_lane.types import Lane


def build_lane_provenance(current_lane: Lane, previous_lane: str | None = None) -> dict:
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "previous_lane": previous_lane,
        "current_lane": current_lane.value,
        "transition": "switch" if previous_lane and previous_lane != current_lane.value else "steady",
    }

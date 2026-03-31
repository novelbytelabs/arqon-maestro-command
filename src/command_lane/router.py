from dataclasses import dataclass

from src.command_lane.errors import FailClosedError
from src.command_lane.types import Lane


@dataclass(frozen=True)
class RoutingDecision:
    lane: Lane
    reason: str


def route_utterance(selected_lane: str) -> RoutingDecision:
    """Route to exactly one canonical lane or fail closed."""
    normalized = selected_lane.strip().lower()
    try:
        lane = Lane(normalized)
    except ValueError as exc:
        raise FailClosedError(f"invalid_lane:{selected_lane}") from exc
    return RoutingDecision(lane=lane, reason="operator_selected_lane")

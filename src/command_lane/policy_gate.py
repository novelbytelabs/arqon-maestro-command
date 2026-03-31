from dataclasses import dataclass

from src.command_lane.errors import FailClosedError


MIN_CONFIDENCE = 0.65


@dataclass(frozen=True)
class PolicyOutcome:
    allow: bool
    reason: str


def adjudicate(confidence: float, authorized: bool = True) -> PolicyOutcome:
    if not authorized:
        raise FailClosedError("authorization_failed")
    if confidence < MIN_CONFIDENCE:
        raise FailClosedError("low_confidence")
    return PolicyOutcome(allow=True, reason="policy_allow")

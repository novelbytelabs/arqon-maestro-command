from src.command_lane.grammar_gate import parse_command
from src.command_lane.policy_gate import adjudicate
from src.command_lane.types import Authority, Decision


def evaluate_candidate(text: str, confidence: float, authorized: bool = True) -> Decision:
    parsed = parse_command(text)
    policy = adjudicate(confidence=confidence, authorized=authorized)
    if parsed and policy.allow:
        return Decision(authority=Authority.GRANTED, reason="granted")
    return Decision(authority=Authority.ESCALATED, reason="unexpected_state")

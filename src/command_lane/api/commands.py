from src.command_lane.decision_engine import evaluate_candidate
from src.command_lane.errors import FailClosedError
from src.command_lane.types import Authority


def evaluate_command(payload: dict) -> dict:
    text = payload.get("transcript", "")
    confidence = float(payload.get("acoustic_confidence", 0.0))
    authorized = bool(payload.get("authorized", True))
    try:
        decision = evaluate_candidate(text=text, confidence=confidence, authorized=authorized)
        return {
            "execution_authority": decision.authority.value,
            "reason": decision.reason,
            "command": text,
        }
    except FailClosedError as exc:
        return {
            "execution_authority": Authority.REFUSED.value,
            "reason": str(exc),
            "command": text,
        }

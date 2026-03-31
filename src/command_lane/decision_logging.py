from datetime import datetime, timezone


def build_decision_log(command: str, authority: str, reason: str) -> dict:
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "command": command,
        "authority": authority,
        "reason": reason,
    }

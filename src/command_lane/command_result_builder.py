def build_command_result(command: str, authority: str, reason: str, evidence_packet: dict) -> dict:
    return {
        "command": command,
        "intent": {"name": command},
        "policy_decision": {"reason": reason},
        "execution_authority": authority,
        "evidence_packet": evidence_packet,
    }

INTERRUPT_VOCABULARY = {"stop", "cancel", "abort", "emergency stop"}


def prioritize_interrupt(candidates: list[str]) -> str:
    normalized = [c.strip().lower() for c in candidates]
    for token in normalized:
        if token in INTERRUPT_VOCABULARY:
            return token
    return normalized[0] if normalized else ""

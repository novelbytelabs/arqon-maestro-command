from src.command_lane.contracts import ensure_contracts_present


def bootstrap_service() -> None:
    ensure_contracts_present()

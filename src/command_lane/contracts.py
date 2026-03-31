from pathlib import Path


CONTRACT_PROTO = Path("ops/helios/contracts/command_contracts.proto")


def ensure_contracts_present() -> None:
    if not CONTRACT_PROTO.exists():
        raise FileNotFoundError(f"Missing contract file: {CONTRACT_PROTO}")

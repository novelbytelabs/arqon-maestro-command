from src.command_lane.errors import FailClosedError


ADAPTER_TIMEOUT_MS = 150


def enforce_adapter_timeout(elapsed_ms: int) -> None:
    if elapsed_ms >= ADAPTER_TIMEOUT_MS:
        raise FailClosedError("adapter_timeout")

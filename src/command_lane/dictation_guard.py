from src.command_lane.errors import FailClosedError
from src.command_lane.types import Lane


def block_command_path_for_dictation(lane: Lane) -> None:
    """Ensure dictation lane cannot continue on command execution path."""
    if lane == Lane.DICTATION:
        raise FailClosedError("dictation_command_path_blocked")

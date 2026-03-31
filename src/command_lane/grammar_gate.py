from dataclasses import dataclass

from src.command_lane.errors import FailClosedError


SUPPORTED_COMMANDS = {
    "stop",
    "cancel",
    "pause",
    "resume",
    "open settings",
    "increase volume",
    "decrease volume",
}


@dataclass(frozen=True)
class ParsedCommand:
    raw: str
    normalized: str


def parse_command(text: str) -> ParsedCommand:
    normalized = " ".join(text.strip().lower().split())
    if not normalized or normalized not in SUPPORTED_COMMANDS:
        raise FailClosedError(f"out_of_grammar:{normalized}")
    return ParsedCommand(raw=text, normalized=normalized)

from dataclasses import dataclass
from enum import Enum


class Lane(str, Enum):
    COMMAND = "command_lane"
    DICTATION = "dictation_lane"
    CONVERSATION = "conversation_lane"
    TRANSLATION = "translation_lane"
    SEARCH = "search_explore_lane"
    DEGRADED_COMMAND = "degraded_command_lane"


class Authority(str, Enum):
    GRANTED = "granted"
    REFUSED = "refused"
    ESCALATED = "escalated"


@dataclass(frozen=True)
class Decision:
    authority: Authority
    reason: str

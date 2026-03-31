from dataclasses import dataclass
from datetime import datetime, timedelta, timezone


CONFIRMATION_TIMEOUT_SECONDS = 5


@dataclass(frozen=True)
class ConfirmationChallenge:
    challenge_id: str
    command_ref: str
    issued_at: datetime
    expires_at: datetime
    status: str


def issue_challenge(challenge_id: str, command_ref: str, issued_at: datetime | None = None) -> ConfirmationChallenge:
    issued = issued_at or datetime.now(timezone.utc)
    return ConfirmationChallenge(
        challenge_id=challenge_id,
        command_ref=command_ref,
        issued_at=issued,
        expires_at=issued + timedelta(seconds=CONFIRMATION_TIMEOUT_SECONDS),
        status="pending",
    )


def evaluate_challenge(challenge: ConfirmationChallenge, now: datetime | None = None, confirmed: bool = False) -> str:
    if confirmed:
        return "confirmed"
    check_time = now or datetime.now(timezone.utc)
    if check_time >= challenge.expires_at:
        return "auto_refused"
    return "pending"

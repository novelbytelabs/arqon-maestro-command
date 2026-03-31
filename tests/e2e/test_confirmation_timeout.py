import unittest
from datetime import timedelta

from src.command_lane.confirmation import evaluate_challenge, issue_challenge


class ConfirmationTimeoutTests(unittest.TestCase):
    def test_high_impact_auto_refuses_after_five_seconds(self) -> None:
        challenge = issue_challenge("ch-1", "delete-all")
        status = evaluate_challenge(challenge, now=challenge.issued_at + timedelta(seconds=5))
        self.assertEqual(status, "auto_refused")


if __name__ == "__main__":
    unittest.main()

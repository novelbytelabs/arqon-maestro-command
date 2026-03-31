import unittest

from src.command_lane.errors import FailClosedError
from src.command_lane.policy_gate import adjudicate


class PolicyGateTests(unittest.TestCase):
    def test_low_confidence_fails_closed(self) -> None:
        with self.assertRaises(FailClosedError):
            adjudicate(confidence=0.30, authorized=True)

    def test_authorization_failure_fails_closed(self) -> None:
        with self.assertRaises(FailClosedError):
            adjudicate(confidence=0.99, authorized=False)

    def test_valid_candidate_allows(self) -> None:
        outcome = adjudicate(confidence=0.90, authorized=True)
        self.assertTrue(outcome.allow)


if __name__ == "__main__":
    unittest.main()

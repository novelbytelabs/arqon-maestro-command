import unittest

from src.command_lane.api.commands import evaluate_command


class CommandDecisionFlowTests(unittest.TestCase):
    def test_valid_command_granted(self) -> None:
        result = evaluate_command({"transcript": "stop", "acoustic_confidence": 0.99, "authorized": True})
        self.assertEqual(result["execution_authority"], "granted")


if __name__ == "__main__":
    unittest.main()

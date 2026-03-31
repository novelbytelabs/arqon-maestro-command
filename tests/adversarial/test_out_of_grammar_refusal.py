import unittest

from src.command_lane.api.commands import evaluate_command


class OutOfGrammarRefusalTests(unittest.TestCase):
    def test_adversarial_payload_refused(self) -> None:
        result = evaluate_command({"transcript": "rm -rf /", "acoustic_confidence": 1.0, "authorized": True})
        self.assertEqual(result["execution_authority"], "refused")


if __name__ == "__main__":
    unittest.main()

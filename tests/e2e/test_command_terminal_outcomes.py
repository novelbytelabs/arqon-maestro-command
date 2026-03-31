import unittest

from src.command_lane.api.commands import evaluate_command


class CommandTerminalOutcomeTests(unittest.TestCase):
    def test_corpus_has_terminal_outcomes(self) -> None:
        corpus = [
            {"transcript": "stop", "acoustic_confidence": 0.98, "authorized": True},
            {"transcript": "cancel", "acoustic_confidence": 0.82, "authorized": True},
            {"transcript": "unknown phrase", "acoustic_confidence": 0.99, "authorized": True},
        ]
        for item in corpus:
            result = evaluate_command(item)
            self.assertIn(result["execution_authority"], {"granted", "refused", "escalated"})


if __name__ == "__main__":
    unittest.main()

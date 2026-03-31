import unittest

from src.command_lane.api.utterances import submit_utterance


class DictationIsolationTests(unittest.TestCase):
    def test_dictation_never_enters_command_path(self) -> None:
        result = submit_utterance(
            {
                "utterance_id": "utt-001",
                "lane": "dictation_lane",
                "transcript": "pause",
                "provider_id": "adapter-a",
                "elapsed_ms": 12,
                "acoustic_confidence": 0.98,
            }
        )
        self.assertEqual(result["lane"], "dictation_lane")
        self.assertTrue(result["command_path_blocked"])


if __name__ == "__main__":
    unittest.main()

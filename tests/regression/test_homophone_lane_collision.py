import unittest

from src.command_lane.api.utterances import submit_utterance


class HomophoneLaneCollisionTests(unittest.TestCase):
    def test_command_homophone_in_dictation_stays_isolated(self) -> None:
        result = submit_utterance(
            {
                "utterance_id": "utt-homo",
                "lane": "dictation_lane",
                "transcript": "please pause this sentence here",
                "provider_id": "adapter-a",
                "elapsed_ms": 15,
                "acoustic_confidence": 0.91,
            }
        )
        self.assertEqual(result["lane"], "dictation_lane")
        self.assertTrue(result["command_path_blocked"])


if __name__ == "__main__":
    unittest.main()

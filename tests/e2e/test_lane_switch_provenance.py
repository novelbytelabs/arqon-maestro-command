import unittest

from src.command_lane.api.utterances import submit_utterance


class LaneSwitchProvenanceTests(unittest.TestCase):
    def test_lane_switch_records_transition(self) -> None:
        _ = submit_utterance(
            {
                "utterance_id": "utt-a",
                "lane": "dictation_lane",
                "transcript": "draft a note",
                "provider_id": "adapter-a",
                "elapsed_ms": 11,
            }
        )
        switched = submit_utterance(
            {
                "utterance_id": "utt-b",
                "lane": "command_lane",
                "previous_lane": "dictation_lane",
                "transcript": "stop",
                "provider_id": "adapter-a",
                "elapsed_ms": 10,
            }
        )
        provenance = switched["lane_provenance"]
        self.assertEqual(provenance["previous_lane"], "dictation_lane")
        self.assertEqual(provenance["current_lane"], "command_lane")
        self.assertEqual(provenance["transition"], "switch")


if __name__ == "__main__":
    unittest.main()

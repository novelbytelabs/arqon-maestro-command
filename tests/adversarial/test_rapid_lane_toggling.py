import unittest

from src.command_lane.api.utterances import submit_utterance


class RapidLaneTogglingTests(unittest.TestCase):
    def test_rapid_toggling_keeps_single_lane_decisions(self) -> None:
        lanes = ["dictation_lane", "command_lane", "dictation_lane", "command_lane"]
        previous = None
        for idx, lane in enumerate(lanes, start=1):
            result = submit_utterance(
                {
                    "utterance_id": f"utt-{idx}",
                    "lane": lane,
                    "previous_lane": previous,
                    "transcript": "stop" if lane == "command_lane" else "draft note",
                    "provider_id": "adapter-a",
                    "elapsed_ms": 12,
                }
            )
            self.assertEqual(result["lane"], lane)
            previous = lane


if __name__ == "__main__":
    unittest.main()

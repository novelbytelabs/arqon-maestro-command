import unittest

from src.command_lane.errors import FailClosedError
from src.command_lane.router import route_utterance


class LaneRouterTests(unittest.TestCase):
    def test_routes_to_one_canonical_lane(self) -> None:
        decision = route_utterance("dictation_lane")
        self.assertEqual(decision.lane.value, "dictation_lane")

    def test_invalid_lane_fails_closed(self) -> None:
        with self.assertRaises(FailClosedError):
            route_utterance("random_lane")


if __name__ == "__main__":
    unittest.main()

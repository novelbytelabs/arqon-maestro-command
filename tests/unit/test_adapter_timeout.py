import unittest

from src.command_lane.adapter_timeout import enforce_adapter_timeout
from src.command_lane.errors import FailClosedError


class AdapterTimeoutTests(unittest.TestCase):
    def test_timeout_fails_closed_at_threshold(self) -> None:
        with self.assertRaises(FailClosedError):
            enforce_adapter_timeout(150)

    def test_under_threshold_allows(self) -> None:
        enforce_adapter_timeout(149)


if __name__ == "__main__":
    unittest.main()

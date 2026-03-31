import unittest

from src.command_lane.errors import FailClosedError
from src.command_lane.protocol_guard import enforce_machine_protocol


class ProtocolSovereigntyTests(unittest.TestCase):
    def test_json_rejected_for_machine_path(self) -> None:
        with self.assertRaises(FailClosedError):
            enforce_machine_protocol("application/json")

    def test_protobuf_allowed_for_machine_path(self) -> None:
        enforce_machine_protocol("application/protobuf")


if __name__ == "__main__":
    unittest.main()

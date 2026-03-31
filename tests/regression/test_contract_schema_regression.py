import unittest

from ops.helios.validate_evidence_schema import validate_packet


class ContractSchemaRegressionTests(unittest.TestCase):
    def test_schema_validator_rejects_missing_required_fields(self) -> None:
        self.assertFalse(validate_packet({"audio_hash": "abc"}))

    def test_schema_validator_accepts_required_fields(self) -> None:
        packet = {
            "audio_hash": "abc",
            "lane": "command_lane",
            "policy_outcome": "granted",
            "latency_ms": 10,
            "timestamp": "2026-03-30T00:00:00Z",
        }
        self.assertTrue(validate_packet(packet))


if __name__ == "__main__":
    unittest.main()

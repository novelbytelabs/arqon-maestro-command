import unittest

from src.command_lane.evidence import build_evidence_packet


class EvidencePacketFieldsTests(unittest.TestCase):
    def test_required_fields_exist(self) -> None:
        packet = build_evidence_packet(
            audio_hash="abc",
            lane="command_lane",
            policy_outcome="granted",
            latency_ms=80,
        )
        required = {"audio_hash", "lane", "policy_outcome", "latency_ms", "timestamp"}
        self.assertTrue(required.issubset(packet.keys()))


if __name__ == "__main__":
    unittest.main()

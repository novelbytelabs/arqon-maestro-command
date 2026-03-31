import unittest

from src.command_lane.api.evidence import get_evidence, store_evidence
from src.command_lane.evidence import build_evidence_packet


class EvidenceEndpointContractTests(unittest.TestCase):
    def test_evidence_endpoint_returns_contract_fields(self) -> None:
        evidence_id = "ev-001"
        store_evidence(evidence_id, build_evidence_packet("abc", "command_lane", "granted", 9))
        payload = get_evidence(evidence_id)
        self.assertIn("audio_hash", payload)
        self.assertIn("timestamp", payload)


if __name__ == "__main__":
    unittest.main()

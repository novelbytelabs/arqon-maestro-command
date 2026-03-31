import unittest

from src.command_lane.command_result_builder import build_command_result
from src.command_lane.evidence import build_evidence_packet
from src.command_lane.speech_result_builder import build_speech_result


class AdapterContractCompatibilityTests(unittest.TestCase):
    def test_speech_and_command_contract_shapes(self) -> None:
        speech = build_speech_result(
            {
                "transcript": "stop",
                "lane": "command_lane",
                "acoustic_confidence": 0.99,
                "provider_id": "adapter-a",
                "elapsed_ms": 10,
            }
        )
        evidence = build_evidence_packet("abc", "command_lane", "granted", 10)
        command = build_command_result("stop", "granted", "policy_allow", evidence)
        self.assertIn("transcript", speech)
        self.assertIn("execution_authority", command)
        self.assertIn("evidence_packet", command)


if __name__ == "__main__":
    unittest.main()

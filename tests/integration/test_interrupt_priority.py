import unittest

from src.command_lane.interrupts import prioritize_interrupt


class InterruptPriorityTests(unittest.TestCase):
    def test_interrupt_is_prioritized_over_normal_command(self) -> None:
        selected = prioritize_interrupt(["increase volume", "stop"])
        self.assertEqual(selected, "stop")


if __name__ == "__main__":
    unittest.main()

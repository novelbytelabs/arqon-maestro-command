import unittest

from src.command_lane.errors import FailClosedError
from src.command_lane.grammar_gate import parse_command


class GrammarGateTests(unittest.TestCase):
    def test_in_grammar_command_parses(self) -> None:
        parsed = parse_command("stop")
        self.assertEqual(parsed.normalized, "stop")

    def test_out_of_grammar_fails_closed(self) -> None:
        with self.assertRaises(FailClosedError):
            parse_command("drop all tables")


if __name__ == "__main__":
    unittest.main()

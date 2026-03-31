import unittest

from src.command_lane.metrics import compute_p95, within_bp001_budget


class LatencyBudgetRegressionTests(unittest.TestCase):
    def test_bp001_regression_budget_holds(self) -> None:
        corpus = [110, 125, 130, 140, 145, 150, 155, 160, 165, 180]
        self.assertTrue(within_bp001_budget(corpus, target_ms=200))
        self.assertLess(compute_p95(corpus), 200)


if __name__ == "__main__":
    unittest.main()

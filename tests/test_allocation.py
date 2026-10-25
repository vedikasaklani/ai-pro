import unittest
from allocation import Bid, proportional_fair, priority_auction, vcg, jain_index, welfare


class AllocationTests(unittest.TestCase):
    def setUp(self):
        self.bids = {"a": Bid(100, 1), "b": Bid(100, 1), "c": Bid(100, 1)}

    def test_proportional_fair_respects_budget_and_caps(self):
        result = proportional_fair(self.bids, 100)
        self.assertEqual(sum(result.allocations.values()), 100)
        self.assertLessEqual(max(result.allocations.values()) - min(result.allocations.values()), 1)

    def test_priority_prefers_high_bid(self):
        result = priority_auction({"a": Bid(100, 1), "b": Bid(100, 3)}, 100)
        self.assertEqual(result.allocations, {"a": 0, "b": 100})

    def test_vcg_is_efficient_and_charges_externality(self):
        result = vcg({"a": Bid(100, 1), "b": Bid(100, 3)}, 100)
        self.assertEqual(result.allocations, {"a": 0, "b": 100})
        self.assertEqual(result.payments["b"], 100)

    def test_fairness_and_welfare(self):
        self.assertAlmostEqual(jain_index([10, 10, 10]), 1.0)
        self.assertAlmostEqual(jain_index([100, 0]), 0.5)
        self.assertEqual(welfare({"a": 2, "b": 3}), 5)


if __name__ == "__main__":
    unittest.main()

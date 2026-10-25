import itertools
import math
import unittest
from allocation import Bid, proportional_fair, priority_auction, vcg, jain_index, welfare
from agents import Agent, Task, make_agents, STRATEGIES
from simulation import run_episode, MECHANISMS


class AllocationTests(unittest.TestCase):
    def setUp(self):
        self.bids = {"a": Bid(100, 1), "b": Bid(100, 1), "c": Bid(100, 1)}

    def test_proportional_fair_respects_budget_and_caps(self):
        result = proportional_fair(self.bids, 100)
        self.assertEqual(sum(result.allocations.values()), 100)
        self.assertLessEqual(max(result.allocations.values()) - min(result.allocations.values()), 1)

    def test_proportional_fair_is_optimal(self):
        bids = {"a": Bid(8, 1), "b": Bid(5, 3), "c": Bid(10, 2)}
        got = proportional_fair(bids, 12).allocations

        def score(x):
            return sum(bids[k].value_per_token * math.log(1 + x[k]) for k in bids)
        best = max((dict(zip(bids, xs)) for xs in itertools.product(range(9), range(6), range(11)) if sum(xs) == 12),
                   key=score)
        self.assertAlmostEqual(score(got), score(best))

    def test_priority_prefers_high_bid_and_charges_bid(self):
        result = priority_auction({"a": Bid(100, 1), "b": Bid(100, 3)}, 100)
        self.assertEqual(result.allocations, {"a": 0, "b": 100})
        self.assertEqual(result.payments, {"a": 0, "b": 300})

    def test_vcg_is_efficient_and_charges_externality(self):
        result = vcg({"a": Bid(100, 1), "b": Bid(100, 3)}, 100)
        self.assertEqual(result.allocations, {"a": 0, "b": 100})
        self.assertEqual(result.payments, {"a": 0, "b": 100})

    def test_whole_mode_grants_full_requests_or_nothing(self):
        bids = {"a": Bid(10, 1), "b": Bid(10, 1), "c": Bid(4, 0.5)}
        for mech in MECHANISMS.values():
            alloc = mech(bids, 15, whole=True).allocations
            self.assertTrue(all(alloc[k] in (0, bids[k].request) for k in bids), alloc)
        # Proportional fairness would split 15 three ways; whole mode pools it into a + c by priority.
        self.assertEqual(proportional_fair(bids, 15, whole=True).allocations, {"a": 10, "b": 0, "c": 4})

    def test_fairness_and_welfare(self):
        self.assertAlmostEqual(jain_index([10, 10, 10]), 1.0)
        self.assertAlmostEqual(jain_index([100, 0]), 0.5)
        self.assertEqual(welfare({"a": 2, "b": 3}), 5)


class SimulationTests(unittest.TestCase):
    def test_budget_never_exceeded_and_tokens_accounted(self):
        for mech, strategy, seed, noise, whole in itertools.product(MECHANISMS, STRATEGIES, range(5), (0, 0.4), (False, True)):
            agents = make_agents(5, 4, strategy, seed, noise)
            budget = sum(a.remaining_tokens for a in agents) // 3
            r = run_episode(agents, mech, budget, whole=whole)
            self.assertLessEqual(r["tokens_spent"], budget)
            self.assertEqual(sum(r["allocations"].values()), r["tokens_spent"])
            self.assertEqual(r["tokens_spent"] + r["unspent_tokens"], budget)

    def test_aware_agent_declines_partial_grant_and_gets_refund(self):
        agent = Agent("a", [Task(estimate=100, tokens=80, value=50)], "mechanism_aware")
        self.assertEqual(agent.consume(60, 100), 60)  # declined: all 60 tokens go back, nothing wasted
        self.assertEqual((agent.completed_tasks, agent.wasted_tokens), (0, 0))
        self.assertEqual(agent.consume(100, 100), 20)  # task really costs 80: 20 refunded
        self.assertEqual(agent.completed_tasks, 1)

    def test_aware_agent_retries_bigger_after_cut_off(self):
        agent = Agent("a", [Task(estimate=100, tokens=130, value=50)], "mechanism_aware")
        self.assertEqual(agent.consume(100, 100), 0)  # cut off at 100: all wasted
        self.assertEqual(agent.wasted_tokens, 100)
        retry = agent.bid("vcg").request
        self.assertEqual(retry, 150)
        agent.consume(retry, retry)
        self.assertEqual(agent.completed_tasks, 1)

    def test_workload_is_paired_across_strategies(self):
        naive, aware = make_agents(4, 4, "naive", 7), make_agents(4, 4, "mechanism_aware", 7)
        self.assertEqual([a.tasks for a in naive], [a.tasks for a in aware])

    def test_awareness_cuts_waste_under_proportional_fair(self):
        waste = {}
        for strategy in ("naive", "mechanism_aware"):
            agents = make_agents(5, 4, strategy, 0)
            waste[strategy] = run_episode(agents, "proportional_fair", sum(a.remaining_tokens for a in agents) // 4)["wasted_tokens"]
        self.assertLess(waste["mechanism_aware"], waste["naive"])


if __name__ == "__main__":
    unittest.main()

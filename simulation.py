"""Run a multi-round allocation episode against one fixed token budget."""
from allocation import proportional_fair, priority_auction, vcg, jain_index, welfare

MECHANISMS = {"proportional_fair": proportional_fair, "priority_auction": priority_auction, "vcg": vcg}


def run_episode(agents, mechanism: str, budget: int, whole: bool = False, cost_per_token: float = 3e-6,
                max_rounds: int = 100, trace=None) -> dict:
    """Agents re-bid each round on what is left of the budget until it, their demand, or progress runs out.

    whole=True makes the allocator fund complete requests only (partial grants are pooled and re-spent).
    `trace`, if given, is called after each round with (round, bids, allocations, refunds, budget_left).
    """
    allocator = MECHANISMS[mechanism]
    left = budget
    used = {a.agent_id: 0 for a in agents}
    transfers = 0.0
    rounds = 0
    while left > 0 and rounds < max_rounds:
        bids = {a.agent_id: a.bid(mechanism) for a in agents if a.tasks}
        if not bids:
            break
        result = allocator(bids, left, whole=whole)
        if not any(result.allocations.values()):
            break  # no remaining request fits in what is left
        refunds = {}
        for a in agents:
            if a.agent_id in bids:
                got = result.allocations[a.agent_id]
                refunds[a.agent_id] = a.consume(got, bids[a.agent_id].request)
                used[a.agent_id] += got - refunds[a.agent_id]
                if got > refunds[a.agent_id]:  # declined grants are not charged
                    transfers += result.payments[a.agent_id]
        spent = sum(result.allocations.values()) - sum(refunds.values())
        left -= spent
        rounds += 1
        if trace:
            trace(rounds, bids, result.allocations, refunds, left)
        if not spent:
            break  # every grant was declined or nothing was granted
    assert left >= 0, "budget overspent"
    completed = sum(a.completed_tasks for a in agents)
    offered = sum(a.completed_tasks + len(a.tasks) for a in agents)
    values = {a.agent_id: a.completed_value for a in agents}
    tokens_spent = budget - left
    return {"mechanism": mechanism, "allocations": used, "rounds": rounds,
            "success_rate": completed / offered if offered else 0.0,
            "tokens_spent": tokens_spent, "total_cost": tokens_spent * cost_per_token,
            "wasted_tokens": sum(a.wasted_tokens for a in agents),
            "unspent_tokens": left, "cut_off_calls": sum(a.cut_off for a in agents),
            "jain_index": jain_index(used.values()), "welfare": welfare(values),
            "welfare_per_budget": welfare(values) / budget if budget else 0.0,
            "transfers": transfers}

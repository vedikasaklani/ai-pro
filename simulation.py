"""Run a single deterministic allocation round."""
from allocation import proportional_fair, priority_auction, vcg, jain_index, welfare

MECHANISMS = {"proportional_fair": proportional_fair, "priority_auction": priority_auction, "vcg": vcg}


def run_round(agents, mechanism: str, budget: int, cost_per_token: float = 0.00001) -> dict:
    allocator = MECHANISMS[mechanism]
    bids = {a.agent_id: a.bid(mechanism) for a in agents}
    result = allocator(bids, budget)
    for a in agents:
        a.consume(result.allocations[a.agent_id])
    completed = sum(a.completed_tasks for a in agents)
    offered = sum(a.completed_tasks + len(a.tasks) for a in agents)
    values = {a.agent_id: a.completed_value for a in agents}
    spent = sum(result.allocations.values())
    return {"mechanism": mechanism, "allocations": result.allocations, "payments": result.payments,
            "success_rate": completed / offered if offered else 0.0, "total_cost": spent * cost_per_token,
            "tokens_spent": spent, "jain_index": jain_index(result.allocations.values()),
            "welfare": welfare(values), "welfare_per_budget": welfare(values) / budget if budget else 0.0}

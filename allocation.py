"""Discrete token allocation mechanisms and common evaluation metrics."""
from dataclasses import dataclass
import math
from typing import Mapping


@dataclass(frozen=True)
class Bid:
    request: int
    value_per_token: float

    def __post_init__(self):
        if self.request < 0 or self.value_per_token < 0:
            raise ValueError("request and value_per_token must be non-negative")


@dataclass
class AllocationResult:
    allocations: dict[str, int]
    payments: dict[str, float]


def _validate(bids: Mapping[str, Bid], budget: int) -> None:
    if budget < 0:
        raise ValueError("budget must be non-negative")


def proportional_fair(bids: Mapping[str, Bid], budget: int) -> AllocationResult:
    """Greedy discrete maximizer for weighted log utility with request caps."""
    _validate(bids, budget)
    out = {k: 0 for k in bids}
    for _ in range(min(budget, sum(b.request for b in bids.values()))):
        eligible = [k for k, b in bids.items() if out[k] < b.request and b.value_per_token > 0]
        if not eligible:
            break
        # Discrete marginal gain in bid_i * log(1 + x_i).
        chosen = max(eligible, key=lambda k: (bids[k].value_per_token * math.log((2 + out[k]) / (1 + out[k])), k))
        out[chosen] += 1
    return AllocationResult(out, {k: 0.0 for k in bids})


def priority_auction(bids: Mapping[str, Bid], budget: int) -> AllocationResult:
    """Allocate each token to the highest declared per-token bid."""
    _validate(bids, budget)
    out = {k: 0 for k in bids}
    order = sorted(bids, key=lambda k: (-bids[k].value_per_token, k))
    left = budget
    for k in order:
        amount = min(left, bids[k].request)
        out[k] = amount
        left -= amount
        if left == 0:
            break
    return AllocationResult(out, {k: 0.0 for k in bids})


def vcg(bids: Mapping[str, Bid], budget: int) -> AllocationResult:
    """Efficient discrete allocation; VCG externality payments, per token."""
    _validate(bids, budget)
    out = {k: 0 for k in bids}
    order = sorted(bids, key=lambda k: (-bids[k].value_per_token, k))
    left = budget
    for k in order:
        amount = min(left, bids[k].request)
        out[k] = amount
        left -= amount
        if not left:
            break
    total = sum(out[k] * bids[k].value_per_token for k in bids)
    payments = {}
    for excluded in bids:
        others = [k for k in bids if k != excluded]
        counterfactual = {k: 0 for k in others}
        for _ in range(min(budget, sum(bids[k].request for k in others))):
            eligible = [k for k in others if counterfactual[k] < bids[k].request]
            if not eligible:
                break
            chosen = max(eligible, key=lambda k: (bids[k].value_per_token, k))
            counterfactual[chosen] += 1
        others_without = sum(counterfactual[k] * bids[k].value_per_token for k in others)
        others_with = sum(out[k] * bids[k].value_per_token for k in others)
        payments[excluded] = max(0.0, others_without - others_with)
    return AllocationResult(out, payments)


def jain_index(values) -> float:
    vals = [max(0.0, float(v)) for v in values]
    denom = len(vals) * sum(v * v for v in vals)
    return (sum(vals) ** 2 / denom) if denom else 1.0


def welfare(values: Mapping[str, float]) -> float:
    return sum(values.values())

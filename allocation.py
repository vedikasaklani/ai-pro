"""Discrete token allocation mechanisms and common evaluation metrics."""
from dataclasses import dataclass
import heapq
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


def _greedy(bids: Mapping[str, Bid], budget: int, exclude: str | None = None, whole: bool = False) -> dict[str, int]:
    """Fill requests in descending bid order; optimal for linear per-token values.

    whole=True never grants part of a request: a request that does not fit is skipped
    and the tokens go to the next-priority request that does.
    """
    out = {k: 0 for k in bids if k != exclude}
    left = budget
    for k in sorted(out, key=lambda k: (-bids[k].value_per_token, k)):
        if whole and bids[k].request > left:
            continue
        out[k] = min(left, bids[k].request)
        left -= out[k]
    return out


def proportional_fair(bids: Mapping[str, Bid], budget: int, whole: bool = False) -> AllocationResult:
    """Exact discrete maximizer of sum(bid_i * log(1 + x_i)) with request caps, no payments.

    whole=True pools every partial grant and re-spends the pool on whole requests by bid priority.
    """
    _validate(bids, budget)
    out = {k: 0 for k in bids}
    # Marginal gains are decreasing per agent, so unit-by-unit greedy is optimal.
    heap = [(-b.value_per_token * math.log(2), k) for k, b in bids.items() if b.request and b.value_per_token > 0]
    heapq.heapify(heap)
    left = budget
    while left and heap:
        _, k = heapq.heappop(heap)
        out[k] += 1
        left -= 1
        if out[k] < bids[k].request:
            heapq.heappush(heap, (-bids[k].value_per_token * math.log((2 + out[k]) / (1 + out[k])), k))
    if whole:
        short = {k: b for k, b in bids.items() if out[k] < b.request}
        pool = left + sum(out[k] for k in short)
        out.update(_greedy(short, pool, whole=True))
    return AllocationResult(out, {k: 0.0 for k in bids})


def priority_auction(bids: Mapping[str, Bid], budget: int, whole: bool = False) -> AllocationResult:
    """First-price priority auction: highest bid served first, winners pay their own bid."""
    _validate(bids, budget)
    out = _greedy(bids, budget, whole=whole)
    return AllocationResult(out, {k: out[k] * bids[k].value_per_token for k in bids})


def vcg(bids: Mapping[str, Bid], budget: int, whole: bool = False) -> AllocationResult:
    """Efficient allocation; each agent pays the declared value it displaces from others.

    With whole=True the greedy fill is a knapsack heuristic, so truthfulness is no longer guaranteed.
    """
    _validate(bids, budget)
    out = _greedy(bids, budget, whole=whole)
    payments = {}
    for i in bids:
        without_i = _greedy(bids, budget, exclude=i, whole=whole)
        others_without = sum(x * bids[k].value_per_token for k, x in without_i.items())
        others_with = sum(out[k] * bids[k].value_per_token for k in bids if k != i)
        payments[i] = max(0.0, others_without - others_with)
    return AllocationResult(out, payments)


def jain_index(values) -> float:
    vals = [max(0.0, float(v)) for v in values]
    denom = len(vals) * sum(v * v for v in vals)
    return (sum(vals) ** 2 / denom) if denom else 1.0


def welfare(values: Mapping[str, float]) -> float:
    return sum(values.values())

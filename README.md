# Mechanism-Aware Multi-Agent LLM Resource Allocation

Small, reproducible simulation of agents competing for a fixed token budget. It uses deterministic task workloads and does not call an LLM API; token use and cost are therefore explicit and repeatable.

## Shared interface

Each allocator accepts `{agent_id: bid/request}` and an integer budget, and returns `{agent_id: allocated_tokens}`. Inputs are token requests plus per-token bids, represented by `Bid(request, value_per_token)`. Allocation is capped by each request and by the budget. The VCG mechanism additionally exposes payments in its result metadata; its tokens allocated are still bounded by the shared budget.

Tasks have a token requirement, a value, and a success value. Agents process tasks in queue order when their allocation covers the requirement. Task value is earned only on completion; partial funding consumes allocated tokens but does not complete a task. Cost is allocated tokens times the configured cost per token, capped by the common token budget. This makes success rate (completed tasks / offered tasks), welfare (sum of completed task values), cost, and welfare per budget measurable.

## Implemented pieces

- `allocation.py`: proportional-fair allocation (weighted log utility with request caps), bid-priority allocation, and welfare-maximizing VCG allocation over discrete token units; Jain fairness and welfare helpers.
- `agents.py`: task queues, greedy naive bids, and mechanism-aware bids.
- `simulation.py`: one round of requests, allocation, task completion, and hard budget accounting.
- `experiments.py`: matrix across three mechanisms, two agent strategies, varied budgets and agent counts; CSV output and charts when matplotlib is installed.
- `tests/`: toy-input unit tests for the mechanisms and fairness calculations.

## Run

From this directory:

```powershell
python -m unittest discover -s tests
python experiments.py --output results
```

The experiment runner writes `results.csv` and an SVG comparison chart (or `comparison.png` when matplotlib is installed). It uses synthetic fixed task values and does not need network access or API credentials.

## Modeling notes and scope

All three policies receive the same requests. Proportional fairness maximizes `sum(bid_i * log(1 + allocation_i))` subject to request caps and the budget, using discrete token allocation. Priority auction assigns units in descending bid order. VCG assigns discrete units by declared marginal values and charges each winner the externality imposed on others; values are fixed per token in this model. The simulation reports token spend separately from VCG transfers, since a transfer is not an LLM token cost. Mechanism-aware agents submit requests based on queued task demand and calibrate bids to their task value and the mechanism; naive agents request all remaining work and bid aggressively. These are controlled toy strategies, not claims about strategic truthfulness of LLMs.

The report outline and interpretation guide are in `REPORT.md`. Literature references supplied with the project brief are recorded there as leads and should be verified before formal submission.

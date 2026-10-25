# Report: Mechanism-Aware Multi-Agent LLM Resource Allocation

Alvin Neal (24BYB0021), Kinjal Sinha (24BYB0066), Vedika Saklani (24BYB0006)

## Research question
Does mechanism awareness improve social welfare per unit of budget? Agents that adapt their requests and bids to the allocation rule are compared with agents that request greedily. We also ask how this trades off against task success and allocation fairness, and which allocator design avoids paying for unfinished work.

## Setup
- **Resource:** one hard token budget, set to 25%, 50% or 75% of estimated task demand. Cost is $3 per 1M tokens.
- **Workload:** each agent has 4 tasks with an estimated cost of 50–300 tokens, worth 0.5–3× that estimate. Workloads are seeded (30 seeds), and every strategy sees the same workload for a given seed.
- **Cost uncertainty:** the real cost is the estimate × uniform(1 − noise, 1 + noise), with noise 0 (exact) or 0.4. Agents see only the estimate, just as real LLM output length is unknown before the call.
- **Completion rule:** a task earns its value only if its grant covers its real cost. Otherwise the call is cut off and the tokens it used are wasted. Billing is per token used, so unused grant is refunded to the pool.
- **Episodes:** agents re-bid each round on the remaining budget, until the budget runs out, the work runs out, or nothing can be funded.
- **Mechanisms:**
  - *Proportional fairness* (primary): maximizes Σ wᵢ·log(1+xᵢ), with request caps and no payments.
  - *First-price priority auction*: highest bid first, winners pay their bid.
  - *VCG*: efficient for the declared values, each agent pays its externality.
- **Allocator designs:**
  - *Split*: the mechanism's allocation is handed out as is, partial grants included.
  - *Whole*: complete requests only. Under proportional fairness, partial grants are pooled and the pool funds whole requests in bid-priority order.
- **Strategies:**
  - *Naive*: requests its whole estimated backlog, bids 2× its best value rate, and runs whatever it receives.
  - *Mechanism-aware*: requests one task at the 95th percentile of its cost error. It declines smaller grants, returns unused tokens, and retries 1.5× larger after a cut-off. It bids truthfully under VCG and proportional fairness and shades to 0.8× under pay-as-bid.
  - *Mixed*: one naive agent among aware ones, the "misbehaving agent" case from the problem statement.

## Results (5 agents, costs ±40%, mean of 30 seeds; see `results/summary.md` for all settings)

Value per budget token, with Jain's index in brackets:

| Budget | Prop. fair, split, naive | Prop. fair, split, aware | **Prop. fair, whole, aware** | VCG, split, naive | VCG, whole, aware |
|---|---|---|---|---|---|
| 25% | 0.78 (0.98) | 0.49 (0.54) | **1.81** (0.55) | 1.61 (0.32) | 1.83 (0.57) |
| 50% | 1.35 (0.98) | 1.24 (0.82) | **1.77** (0.84) | 1.63 (0.54) | 1.76 (0.84) |
| 75% | 1.49 (0.98) | 1.41 (0.92) | **1.70** (0.89) | 1.63 (0.79) | 1.70 (0.90) |

Where the budget goes at 25% (proportional fairness):

| Design | Wasted on cut-off calls | Never used |
|---|---|---|
| Split, naive | 65% | 0% |
| Split, aware | 1% | 75% |
| Whole, aware | 4% | 10% |

- **Other agent counts:** at 3 and 10 agents with a 25% budget, whole + aware gives 1.47 and 1.95 value per token, against 0.69 and 0.78 for split + naive.
- **Exact costs:** with no cost noise, whole + aware reaches 1.85 with zero waste.

## Discussion
- **Does awareness help?** Yes, but only when the allocator cooperates. Under a split allocator, aware agents stop wasting tokens by declining grants they cannot finish. Proportional fairness then re-splits the same thin slices round after round, so the budget sits idle. Pairing aware agents with a whole-request allocator turns the same budget into 2.3× the value.
- **Fairness vs efficiency.** Splitting evenly maximizes Jain's index (0.98) and destroys value under a tight budget. Whole grants are lumpy: fairness falls to 0.55 at a 25% budget and recovers to 0.84–0.89 as the budget loosens. This is the central trade-off the project set out to measure.
- **The allocator rewards honest requests.** Under the whole-request design, a naive agent's full backlog rarely fits, so naive populations earn 1.36 against 1.81 for aware ones. Asking for what you need becomes the winning strategy without any payment.
- **The mechanism matters less once requests are whole.** All three mechanisms reach 1.81–1.83. Their differences show up in payments (VCG transfers fall 3,931 → 1,179 with aware agents) and in fairness under a split allocator.
- **A misbehaving agent.** With one naive hog among declining aware agents under a split allocator, the hog absorbs what the others decline (Jain 0.24). The whole-request design limits this (0.38) because the hog's oversized request rarely fits.
- **Priority vs VCG.** Per-token values are linear in this model, so for identical bids both auctions produce the same allocation. They differ in payments and in the incentive to shade bids.

## Positioning against the literature
- Dütting et al. (WWW 2024) design truthful auctions over LLM outputs. Our VCG baseline is the classical truthful mechanism. The result that truthful bidding sharply lowers VCG transfers is consistent with that line of work.
- The auction-based allocation papers (Agora, the auction-based communication paper) allocate units by bid. Our auction baselines show the downside: a single over-bidding agent drives fairness down.
- Budget-constrained systems (BudgetMLAgent, BAMAS, ZEBRA, Agent Contracts) enforce a hard spend cap. We enforce the same cap and add two results: *how* agents request against it matters, and an allocator should fund whole requests instead of slicing.
- Self-Resource Allocation (arXiv:2504.02051) asks whether an LLM can allocate on its own judgment. Here the allocation rule is explicit, and only the agents' requests adapt.

Verify bibliographic details and preprint status against the original papers before formal submission.

## Limitations
- The workload is synthetic and no live LLM is called. Cost noise is uniform and independent per task; real output lengths are skewed and correlated.
- The agent strategies are fixed heuristics, not learned or LLM-generated.
- The whole-request pool is filled by bid priority, which favours efficiency over fairness. A fairness-first pooling order (for example, least-served agent first) is a natural variant to test.
- Under `whole=True`, VCG runs on a greedy knapsack, so it is no longer guaranteed to be truthful.
- Proportional fairness has no payments, so inflating a bid is free under it.
- Natural next steps: replace the agents with LLM bidders that estimate their own costs, measure real token use per task, and try fairness-first pooling.

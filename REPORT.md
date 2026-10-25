# Report outline and experiment protocol

## Research question
Does adapting agent requests and bids to the allocation rule improve completed task value per token budget, and how does that trade off against task completion and allocation fairness?

## Experiment matrix
Run all three mechanisms (proportional fairness, bid-priority, VCG), both strategies (naive, mechanism-aware), agent counts 3/5/10, and token budgets 100/250/500. Each agent receives four deterministic tasks. `experiments.py` emits one row per configuration with task success rate, token cost, Jain's index, welfare, and welfare per budget.

## Suggested report sections
1. Abstract and research question
2. Motivation and related work
3. Mechanisms and agent strategies
4. Workload, metrics, and experimental protocol
5. Results (CSV tables and welfare-per-budget chart)
6. Discussion: efficiency/fairness trade-offs and whether awareness helps
7. Limitations and conclusion

## Literature leads from the project brief
The supplied brief points to Dütting, Mirrokni, Paes Leme, Xu, and Zuo, “Mechanism Design for Large Language Models” (WWW 2024; arXiv:2310.10826); BudgetMLAgent (arXiv:2411.07464); and classical market-based multi-agent allocation work. It also lists newer preprints on auction-based LLM task allocation and budget-aware orchestration. Treat the newer references and all bibliographic details as leads: verify publication status, titles, authors, and claims against the original papers before submission.

## Interpretation caveats
This is a deterministic synthetic benchmark, not a live LLM evaluation. Agent values are declared task values; mechanism-aware agents use a simple rule-specific bid heuristic. VCG payments are reported separately from API token cost. The model supports a transparent comparison but does not establish truthful bidding or general performance on real workloads.

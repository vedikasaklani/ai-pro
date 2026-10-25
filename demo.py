"""Live walkthrough: one shared budget, watched round by round, then all designs side by side."""
import argparse
import statistics
import sys
from agents import make_agents, STRATEGIES
from simulation import run_episode, MECHANISMS

COLOR = sys.stdout.isatty()


def style(text, code):
    return f"\033[{code}m{text}\033[0m" if COLOR else text


def bold(t): return style(t, "1")
def dim(t): return style(t, "2")
def green(t): return style(t, "32")
def yellow(t): return style(t, "33")
def red(t): return style(t, "31")


def heading(text):
    print("\n" + bold(text))
    print(dim("─" * 86))


def bar(part, whole, width=20):
    filled = min(width, round(width * part / whole)) if whole else 0
    return "█" * filled + dim("░" * (width - filled))


def budget_for(args, agents):
    return round(args.budget_ratio * sum(a.remaining_tokens for a in agents))


def explain(args, agents, budget):
    heading("HOW THIS IS TESTED WITHOUT AN LLM")
    print("Each agent stands in for an LLM agent; each task has a token cost and a value. Instead of calling a")
    print("model we deduct the task's tokens from the shared budget, exactly as an API bill would.")
    print(f"  • Agents only know an ESTIMATE. The real cost is revealed when the task runs (±{args.noise:.0%} here).")
    print("  • A call that runs out of tokens is cut off: tokens used are lost, nothing is delivered.")
    print("  • Billing is per token used, so a finished task hands back whatever it did not need.")
    print("  • Same seed = same tasks for every strategy, so every comparison is like-for-like.")

    heading(f"THE WORKLOAD  (seed {args.seed})")
    print(f"{args.agents} agents × 4 tasks ≈ {sum(a.remaining_tokens for a in agents):,} tokens of work (estimated).  "
          f"Shared budget: {bold(f'{budget:,} tokens')} ({args.budget_ratio:.0%})")
    print(dim("  each cell: estimated tokens → real tokens · value points\n"))
    for a in agents:
        print(f"  {a.agent_id:<9}" + "".join(f"{f'{t.estimate}→{t.tokens} · {t.value:.0f}pt':>19}" for t in a.tasks))


DESIGNS = [
    ("naive", False, "1. NAIVE agents, fair split",
     "Agents ask for their whole backlog; the allocator splits the budget evenly."),
    ("mechanism_aware", False, "2. AWARE agents, fair split",
     "Agents ask for one task + safety margin and DECLINE grants too small to finish it."),
    ("mechanism_aware", True, "3. AWARE agents, whole-request allocator",
     "Partial grants are pooled and spent on complete requests, highest priority first."),
]


def walkthrough(args, strategy, whole, title, blurb):
    agents = make_agents(args.agents, 4, strategy, args.seed, args.noise)
    by_id = {a.agent_id: a for a in agents}
    budget = budget_for(args, agents)
    before = {a.agent_id: (0, 0, 0) for a in agents}
    heading(f"{title}   [{args.mechanism.replace('_', ' ')}]")
    print(dim(f"  {blurb}"))

    def trace(rnd, bids, alloc, refunds, left):
        print(f"\n  Round {rnd}" + dim(f"   (budget left after round: {left:,})"))
        print(dim(f"  {'agent':<9}{'asked':>7}{'bid/tok':>9}{'granted':>9}  {'granted vs asked':<20}  outcome"))
        for k, b in bids.items():
            a, got, back = by_id[k], alloc.get(k, 0), refunds.get(k, 0)
            done = a.completed_tasks - before[k][0]
            wasted = a.wasted_tokens - before[k][1]
            declined = a.declined - before[k][2]
            before[k] = (a.completed_tasks, a.wasted_tokens, a.declined)
            outcome = []
            if done:
                outcome.append(green(f"✓ {done} task{'s' * (done > 1)} done"))
            if declined:
                outcome.append(yellow(f"↩ declined, {back} returned"))
            elif back:
                outcome.append(dim(f"{back} unused returned"))
            if wasted:
                outcome.append(red(f"✗ cut off, {wasted} tok wasted"))
            print(f"  {k:<9}{b.request:>7}{b.value_per_token:>9.2f}{got:>9}  {bar(got, b.request)}  "
                  f"{', '.join(outcome) or dim('—')}")

    r = run_episode(agents, args.mechanism, budget, whole=whole, trace=trace)
    waste, unspent = r["wasted_tokens"] / budget, r["unspent_tokens"] / budget
    value = f"{r['welfare']:,.0f} pts"
    print(f"\n  Result: value {bold(value)}  ·  tasks done {r['success_rate']:.0%}  ·  "
          f"wasted {(red if waste > 0.2 else green)(f'{waste:.0%}')}  ·  "
          f"left unused {(yellow if unspent > 0.2 else green)(f'{unspent:.0%}')}  ·  fairness {r['jain_index']:.2f}")


def summary(args):
    heading(f"EVERY DESIGN  (mean over {args.seeds} workloads, {args.agents} agents, budget {args.budget_ratio:.0%}, "
            f"cost noise ±{args.noise:.0%})")
    print(f"  {'mechanism':<19}{'allocator':<11}{'agents':<17}{'value/token':>12}{'tasks done':>11}{'fairness':>10}"
          f"{'wasted':>8}{'unused':>8}")
    rows = {}
    for mech in MECHANISMS:
        for allocator, whole in (("split", False), ("whole", True)):
            for strategy in STRATEGIES:
                runs = []
                for seed in range(args.seeds):
                    agents = make_agents(args.agents, 4, strategy, seed, args.noise)
                    budget = budget_for(args, agents)
                    r = run_episode(agents, mech, budget, whole=whole)
                    runs.append((r["welfare_per_budget"], r["success_rate"], r["jain_index"],
                                 r["wasted_tokens"] / budget, r["unspent_tokens"] / budget))
                rows[mech, allocator, strategy] = [statistics.mean(col) for col in zip(*runs)]
    best = max(v[0] for v in rows.values())
    for i, ((mech, allocator, strategy), (w, s, j, waste, unused)) in enumerate(rows.items()):
        if i and i % (2 * len(STRATEGIES)) == 0:
            print()
        w_text = f"{w:>12.2f}"
        print(f"  {mech.replace('_', ' '):<19}{allocator:<11}{strategy.replace('_', ' '):<17}"
              f"{bold(green(w_text)) if w == best else w_text}{s:>11.0%}{j:>10.2f}{waste:>8.0%}{unused:>8.0%}")
    print(dim("\n  value/token = value of completed tasks ÷ budget.  fairness = Jain's index (1.0 = perfectly even).\n"
              "  split = allocator may hand out partial grants; whole = complete requests only.\n"
              "  mixed = one naive 'hog' agent among aware agents."))


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--agents", type=int, default=5)
    p.add_argument("--budget-ratio", type=float, default=0.25, help="budget as a share of estimated demand")
    p.add_argument("--noise", type=float, default=0.4, help="real cost = estimate × uniform(1-noise, 1+noise)")
    p.add_argument("--mechanism", choices=MECHANISMS, default="proportional_fair")
    p.add_argument("--seed", type=int, default=0, help="workload shown in the round-by-round trace")
    p.add_argument("--seeds", type=int, default=30, help="workloads averaged in the final table")
    args = p.parse_args()

    agents = make_agents(args.agents, 4, "naive", args.seed, args.noise)
    explain(args, agents, budget_for(args, agents))
    for design in DESIGNS:
        walkthrough(args, *design)
    summary(args)


if __name__ == "__main__":
    main()

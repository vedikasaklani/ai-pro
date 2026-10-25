"""Menu-driven terminal explorer for the allocator. Run: python tui.py"""
import argparse
import copy
import os
import statistics
import subprocess
import sys
from pathlib import Path
import demo
from demo import bold, dim, green, yellow, red, bar, heading, budget_for
from agents import make_agents, STRATEGIES
from simulation import run_episode, MECHANISMS

HERE = Path(__file__).resolve().parent
ALLOCATORS = {"split": False, "whole": True}


def clear():
    os.system("cls" if os.name == "nt" else "clear")  # also enables ANSI colors on Windows consoles


def pause():
    input(dim("\n  Press Enter to return to the menu… "))


def choose(prompt, options):
    """Numbered pick from a list; Enter keeps the first option."""
    for i, o in enumerate(options, 1):
        print(f"    {bold(str(i))}  {o.replace('_', ' ')}")
    while True:
        raw = input(f"  {prompt} [1]: ").strip() or "1"
        if raw.isdigit() and 1 <= int(raw) <= len(options):
            return options[int(raw) - 1]
        print(red("    Pick one of the numbers above."))


def ask_number(prompt, cast, current, lo, hi):
    while True:
        raw = input(f"  {prompt} ({lo}–{hi}) [{current}]: ").strip()
        if not raw:
            return current
        try:
            value = cast(raw)
            if lo <= value <= hi:
                return value
        except ValueError:
            pass
        print(red(f"    Enter a number between {lo} and {hi}."))


def settings_line(args):
    return (f"{args.agents} agents · budget {args.budget_ratio:.0%} of demand · cost noise ±{args.noise:.0%} · "
            f"{args.mechanism.replace('_', ' ')} · trace seed {args.seed} · {args.seeds} seeds averaged")


# ── screens ──────────────────────────────────────────────────────────────────

def screen_how_it_works(args):
    agents = make_agents(args.agents, 4, "naive", args.seed, args.noise)
    demo.explain(args, agents, budget_for(args, agents))
    heading("THE PIECES")
    print(f"  {bold('Mechanisms')} decide how a round's budget is split:")
    print("    proportional fair  spreads tokens so nobody is starved (maximizes Σ bid·log(1+tokens))")
    print("    priority auction   highest bid served first; winners pay their bid")
    print("    vcg                highest bid first; each winner pays the value it blocks for others")
    print(f"  {bold('Allocators')} decide whether a grant may be partial:")
    print("    split              hand out whatever the mechanism computes, partial grants included")
    print("    whole              pool partial grants and fund complete requests, highest priority first")
    print(f"  {bold('Agents')}:")
    print("    naive              asks for its whole backlog, inflates its bid, runs whatever it gets")
    print("    mechanism aware    asks for one task + safety margin, declines partial grants,")
    print("                       returns unused tokens, retries 1.5× larger after a cut-off")
    print("    mixed              one naive 'hog' among aware agents")


def screen_walkthrough(args):
    for design in demo.DESIGNS:
        demo.walkthrough(args, *design)


def screen_custom_run(args):
    heading("CUSTOM RUN — pick a design and watch it round by round")
    run_args = copy.copy(args)
    run_args.mechanism = choose("Mechanism", list(MECHANISMS))
    strategy = choose("Agents", list(STRATEGIES))
    allocator = choose("Allocator", list(ALLOCATORS))
    demo.walkthrough(run_args, strategy, ALLOCATORS[allocator],
                     f"{strategy.replace('_', ' ').upper()} agents, {allocator} allocator", settings_line(run_args))


def screen_agents(args):
    heading("AGENT DRILL-DOWN — who got what, and what they did with it")
    run_args = copy.copy(args)
    run_args.mechanism = choose("Mechanism", list(MECHANISMS))
    strategy = choose("Agents", list(STRATEGIES))
    allocator = choose("Allocator", list(ALLOCATORS))
    agents = make_agents(args.agents, 4, strategy, args.seed, args.noise)
    budget = budget_for(args, agents)
    r = run_episode(agents, run_args.mechanism, budget, whole=ALLOCATORS[allocator])
    used = r["allocations"]
    top = max(used.values()) or 1
    heading(f"{run_args.mechanism.replace('_', ' ')} · {strategy.replace('_', ' ')} · {allocator}  "
            f"(seed {args.seed}, budget {budget:,} tokens)")
    print(dim(f"  {'agent':<9}{'type':<10}{'tokens used':>12}  {'share of budget':<20}{'done':>6}{'value':>8}"
              f"{'wasted':>8}{'declined':>10}{'cut off':>9}"))
    for a in agents:
        print(f"  {a.agent_id:<9}{a.strategy.replace('mechanism_', ''):<10}{used[a.agent_id]:>12}  "
              f"{bar(used[a.agent_id], top)}{a.completed_tasks:>4}/4{a.completed_value:>8.0f}"
              f"{(red if a.wasted_tokens else dim)(f'{a.wasted_tokens:>8}')}{a.declined:>10}{a.cut_off:>9}")
    value = f"{r['welfare']:,.0f} pts"
    print(f"\n  Total value {bold(value)} · tasks done {r['success_rate']:.0%} · "
          f"wasted {r['wasted_tokens'] / budget:.0%} · unused {r['unspent_tokens'] / budget:.0%} · "
          f"fairness {r['jain_index']:.2f} · rounds {r['rounds']} · cost ${r['total_cost']:.4f}")


def mean_metrics(args, mechanism, strategy, whole, ratio):
    runs = []
    for seed in range(args.seeds):
        agents = make_agents(args.agents, 4, strategy, seed, args.noise)
        budget = round(ratio * sum(a.remaining_tokens for a in agents))
        r = run_episode(agents, mechanism, budget, whole=whole)
        runs.append((r["welfare_per_budget"], r["jain_index"], r["wasted_tokens"] / budget))
    return [statistics.mean(c) for c in zip(*runs)]


def screen_sweep(args):
    heading("BUDGET SWEEP — how each design behaves as the budget grows")
    metric = choose("Show", ["value per token", "fairness (Jain)", "tokens wasted"])
    col = ["value per token", "fairness (Jain)", "tokens wasted"].index(metric)
    designs = [("naive", "split"), ("mechanism_aware", "split"), ("mechanism_aware", "whole")]
    ratios = (0.1, 0.25, 0.4, 0.5, 0.75, 1.0)
    data = {d: [mean_metrics(args, args.mechanism, d[0], ALLOCATORS[d[1]], r)[col] for r in ratios] for d in designs}
    top = max(max(v) for v in data.values()) or 1
    heading(f"{metric} · {args.mechanism.replace('_', ' ')} · {args.agents} agents · ±{args.noise:.0%} noise · "
            f"mean of {args.seeds} seeds")
    paint = {designs[0]: red, designs[1]: yellow, designs[2]: green}
    for i, ratio in enumerate(ratios):
        print(f"  budget {ratio:>4.0%}")
        for d in designs:
            v = data[d][i]
            label = f"{d[0].replace('mechanism_', '')}, {d[1]}"
            text = f"{v:.0%}" if col == 2 else f"{v:.2f}"
            print(f"    {label:<14}{paint[d](bar(v, top, 40))} {text}")
    print(dim("\n  Bars are scaled to the largest value on this screen."))


def screen_settings(args):
    while True:
        clear()
        heading("SETTINGS")
        fields = [("Agents", "agents"), ("Budget (share of demand)", "budget_ratio"), ("Cost noise (±)", "noise"),
                  ("Mechanism for walkthrough / sweep", "mechanism"), ("Trace seed (which workload)", "seed"),
                  ("Seeds averaged in tables", "seeds")]
        for i, (label, key) in enumerate(fields, 1):
            print(f"    {bold(str(i))}  {label:<36}{getattr(args, key)}")
        print(f"    {bold('0')}  back")
        pick = input("\n  Change which? ").strip()
        if pick in ("", "0"):
            return
        if pick == "1":
            args.agents = ask_number("Agents", int, args.agents, 2, 20)
        elif pick == "2":
            args.budget_ratio = ask_number("Budget share", float, args.budget_ratio, 0.05, 1.0)
        elif pick == "3":
            args.noise = ask_number("Noise", float, args.noise, 0.0, 0.9)
        elif pick == "4":
            args.mechanism = choose("Mechanism", list(MECHANISMS))
        elif pick == "5":
            args.seed = ask_number("Seed", int, args.seed, 0, 10_000)
        elif pick == "6":
            args.seeds = ask_number("Seeds", int, args.seeds, 1, 200)


def screen_tests(args):
    heading("RUNNING THE TEST SUITE")
    subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"], cwd=HERE)


def screen_experiments(args):
    heading("FULL EXPERIMENT MATRIX → results/")
    subprocess.run([sys.executable, "experiments.py"], cwd=HERE)


MENU = [
    ("How it works (and how we test without an LLM)", screen_how_it_works),
    ("Walkthrough: naive → aware → whole-request allocator", screen_walkthrough),
    ("Compare every design (averaged table)", demo.summary),
    ("Custom run: pick mechanism, agents, allocator", screen_custom_run),
    ("Agent drill-down: per-agent tokens, tasks, waste", screen_agents),
    ("Budget sweep: chart a metric as the budget grows", screen_sweep),
    ("Settings", screen_settings),
    ("Run the test suite", screen_tests),
    ("Run the full experiment matrix (writes results/)", screen_experiments),
]


def main():
    args = argparse.Namespace(agents=5, budget_ratio=0.25, noise=0.4, mechanism="proportional_fair", seed=0, seeds=30)
    while True:
        clear()
        print(bold("  MECHANISM-AWARE MULTI-AGENT RESOURCE ALLOCATOR"))
        print(dim("  " + settings_line(args)))
        print(dim("  " + "─" * 70))
        for i, (label, _) in enumerate(MENU, 1):
            print(f"    {bold(str(i))}  {label}")
        print(f"    {bold('q')}  quit")
        pick = input("\n  Choose: ").strip().lower()
        if pick in ("q", "quit", "exit"):
            return
        if pick.isdigit() and 1 <= int(pick) <= len(MENU):
            label, screen = MENU[int(pick) - 1]
            clear()
            screen(args)
            if screen is not screen_settings:
                pause()


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print()

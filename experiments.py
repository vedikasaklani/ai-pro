"""Run the mechanism x strategy x budget x agent-count matrix over many seeds."""
import argparse
import csv
import statistics
from pathlib import Path
from agents import make_agents, STRATEGIES
from simulation import run_episode, MECHANISMS

AGENT_COUNTS = (3, 5, 10)
BUDGET_RATIOS = (0.25, 0.5, 0.75)  # budget as a share of total (estimated) task demand
NOISE_LEVELS = (0.0, 0.4)  # real task cost = estimate x uniform(1 - noise, 1 + noise)
ALLOCATORS = {"split": False, "whole": True}  # whole = fund complete requests only
METRICS = ("success_rate", "total_cost", "tokens_spent", "wasted_tokens", "unspent_tokens", "cut_off_calls",
           "jain_index", "welfare", "welfare_per_budget", "transfers", "rounds")
COLORS = {"naive": "#2a78d6", "mechanism_aware": "#eb6834", "mixed": "#1baf7a"}


def run_matrix(seeds: int = 30, tasks_per_agent: int = 4):
    rows = []
    for noise in NOISE_LEVELS:
        for allocator, whole in ALLOCATORS.items():
            for n in AGENT_COUNTS:
                for ratio in BUDGET_RATIOS:
                    for mechanism in MECHANISMS:
                        for strategy in STRATEGIES:
                            for seed in range(seeds):
                                agents = make_agents(n, tasks_per_agent, strategy, seed, noise)
                                budget = round(ratio * sum(a.remaining_tokens for a in agents))
                                row = run_episode(agents, mechanism, budget, whole=whole)
                                rows.append({"noise": noise, "allocator": allocator, "agent_count": n,
                                             "budget_ratio": ratio, "budget": budget, "seed": seed, "strategy": strategy,
                                             "mechanism": mechanism, **{k: row[k] for k in METRICS}})
    return rows


def summarize(rows):
    groups = {}
    for r in rows:
        key = (r["noise"], r["allocator"], r["agent_count"], r["budget_ratio"], r["mechanism"], r["strategy"])
        groups.setdefault(key, []).append(r)
    out = []
    for (noise, allocator, n, ratio, mech, strat), g in groups.items():
        s = {"noise": noise, "allocator": allocator, "agent_count": n, "budget_ratio": ratio,
             "mechanism": mech, "strategy": strat, "runs": len(g)}
        for m in METRICS:
            s[m] = statistics.mean(r[m] for r in g)
        s["waste_rate"] = statistics.mean(r["wasted_tokens"] / r["budget"] for r in g)
        s["unspent_rate"] = statistics.mean(r["unspent_tokens"] / r["budget"] for r in g)
        s["welfare_per_budget_sd"] = statistics.stdev(r["welfare_per_budget"] for r in g) if len(g) > 1 else 0.0
        out.append(s)
    return out


def markdown_table(summary, n, ratio, noise):
    lines = [f"### Agents = {n}, budget = {ratio:.0%} of demand, cost noise = ±{noise:.0%} (mean over seeds)", "",
             "| Allocator | Mechanism | Strategy | Welfare / budget | Success | Jain | Wasted | Unspent | Transfers |",
             "|---|---|---|---|---|---|---|---|---|"]
    for s in summary:
        if s["agent_count"] == n and s["budget_ratio"] == ratio and s["noise"] == noise:
            lines.append(f"| {s['allocator']} | {s['mechanism']} | {s['strategy']} | {s['welfare_per_budget']:.3f} ± "
                         f"{s['welfare_per_budget_sd']:.3f} | {s['success_rate']:.1%} | {s['jain_index']:.3f} | "
                         f"{s['waste_rate']:.1%} | {s['unspent_rate']:.1%} | {s['transfers']:.0f} |")
    return "\n".join(lines)


def svg_chart(summary, n, ratio, noise, allocator):
    """Three grouped-bar panels (one per metric), bars colored by strategy."""
    panels = [("welfare_per_budget", "Welfare per budget token"), ("success_rate", "Task success rate"),
              ("jain_index", "Fairness (Jain's index)")]
    mechs = list(MECHANISMS)
    data = {(s["mechanism"], s["strategy"]): s for s in summary if s["agent_count"] == n and s["budget_ratio"] == ratio
            and s["noise"] == noise and s["allocator"] == allocator}
    pw, ph, top, left_pad = 300, 220, 70, 40
    width = len(panels) * pw + 20
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{top + ph + 70}" '
           f'viewBox="0 0 {width} {top + ph + 70}" font-family="system-ui, sans-serif">',
           f'<rect width="100%" height="100%" fill="#fcfcfb"/>',
           f'<text x="20" y="26" font-size="16" font-weight="600" fill="#0b0b0b">{allocator.capitalize()} allocator: '
           f'{n} agents, budget {ratio:.0%} of demand, cost noise ±{noise:.0%}</text>']
    x = 20
    for strategy, color in COLORS.items():  # legend
        svg.append(f'<rect x="{x}" y="40" width="12" height="12" rx="2" fill="{color}"/>'
                   f'<text x="{x + 18}" y="50" font-size="12" fill="#52514e">{strategy}</text>')
        x += 140
    for p, (metric, label) in enumerate(panels):
        ox = 10 + p * pw
        vmax = max(d[metric] for d in data.values()) * 1.15 or 1
        base = top + ph
        svg.append(f'<text x="{ox + left_pad}" y="{top - 4}" font-size="12" fill="#0b0b0b">{label}</text>')
        svg.append(f'<line x1="{ox + left_pad}" y1="{base}" x2="{ox + pw - 10}" y2="{base}" stroke="#c3c2b7"/>')
        gw = (pw - left_pad - 20) / len(mechs)
        bw = (gw - 16) / len(COLORS)
        for g, mech in enumerate(mechs):
            gx = ox + left_pad + g * gw + 8
            for b, (strategy, color) in enumerate(COLORS.items()):
                v = data[(mech, strategy)][metric]
                h = (ph - 20) * v / vmax
                bx = gx + b * bw
                svg.append(f'<rect x="{bx + 1:.1f}" y="{base - h:.1f}" width="{bw - 2:.1f}" height="{h:.1f}" rx="2" fill="{color}">'
                           f'<title>{mech} / {strategy}: {v:.3f}</title></rect>')
                svg.append(f'<text x="{bx + bw / 2:.1f}" y="{base - h - 4:.1f}" font-size="9" text-anchor="middle" '
                           f'fill="#52514e">{v:.2f}</text>')
            svg.append(f'<text x="{gx + gw / 2 - 8:.1f}" y="{base + 16}" font-size="10" text-anchor="middle" '
                       f'fill="#52514e">{mech.replace("_", " ")}</text>')
    svg.append("</svg>")
    return "\n".join(svg)


def write_csv(path, rows):
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="results")
    parser.add_argument("--seeds", type=int, default=30)
    args = parser.parse_args()
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)
    rows = run_matrix(args.seeds)
    summary = summarize(rows)
    write_csv(out / "results.csv", rows)
    write_csv(out / "summary.csv", summary)
    tables = [markdown_table(summary, 5, r, noise) for noise in reversed(NOISE_LEVELS) for r in BUDGET_RATIOS]
    (out / "summary.md").write_text("\n\n".join(tables) + "\n", encoding="utf-8")
    for allocator in ALLOCATORS:
        (out / f"comparison_{allocator}.svg").write_text(svg_chart(summary, 5, 0.25, 0.4, allocator), encoding="utf-8")
    print(tables[0])
    print(f"\nWrote {len(rows)} runs ({len(summary)} configurations) to {out}/")


if __name__ == "__main__":
    main()

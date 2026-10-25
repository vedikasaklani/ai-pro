"""Run the requested mechanism/strategy/budget/agent-count matrix."""
import argparse
import csv
from pathlib import Path
from agents import make_agents
from simulation import run_round, MECHANISMS


def run_matrix():
    rows = []
    for n in (3, 5, 10):
        for budget in (100, 250, 500):
            for mechanism in MECHANISMS:
                for strategy in ("naive", "mechanism_aware"):
                    agents = make_agents(n, 4, strategy)
                    row = run_round(agents, mechanism, budget)
                    rows.append({"agent_count": n, "budget": budget, "strategy": strategy,
                                 "mechanism": mechanism, **{k: row[k] for k in
                                 ("success_rate", "total_cost", "tokens_spent", "jain_index", "welfare", "welfare_per_budget")}})
    return rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="results")
    args = parser.parse_args()
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)
    rows = run_matrix()
    with (out / "results.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    try:
        import matplotlib.pyplot as plt
        for strategy in ("naive", "mechanism_aware"):
            group = [r for r in rows if r["strategy"] == strategy and r["agent_count"] == 5]
            for mech in MECHANISMS:
                series = [r for r in group if r["mechanism"] == mech]
                plt.plot([r["budget"] for r in series], [r["welfare_per_budget"] for r in series], marker="o", label=f"{strategy}: {mech}")
        plt.xlabel("Token budget")
        plt.ylabel("Welfare per token budget")
        plt.legend()
        plt.tight_layout()
        plt.savefig(out / "comparison.png", dpi=160)
        plt.close()
    except ImportError:
        # Keep the chart artifact available in minimal Python installations.
        colors = {"naive": "#2563eb", "mechanism_aware": "#dc2626"}
        labels = list(MECHANISMS)
        points = []
        for strategy in ("naive", "mechanism_aware"):
            for mech in labels:
                series = [r for r in rows if r["strategy"] == strategy and r["agent_count"] == 5 and r["mechanism"] == mech]
                coords = [(80 + i * 220, 300 - r["welfare_per_budget"] * 1200) for i, r in enumerate(series)]
                points.append((strategy, mech, " ".join(f"{x},{y:.1f}" for x, y in coords)))
        svg = ['<svg xmlns="http://www.w3.org/2000/svg" width="800" height="380" viewBox="0 0 800 380">',
               '<rect width="100%" height="100%" fill="white"/>',
               '<text x="400" y="25" text-anchor="middle" font-family="sans-serif" font-size="17">Welfare per token budget (5 agents)</text>',
               '<path d="M60 300 H740 M60 60 V300" stroke="#444" fill="none"/>',
               '<text x="400" y="350" text-anchor="middle" font-family="sans-serif">Token budget: 100, 250, 500</text>']
        for strategy, mech, coords in points:
            svg.append(f'<polyline points="{coords}" fill="none" stroke="{colors[strategy]}" stroke-width="2"/>')
            svg.append(f'<text x="70" y="{45 + len(svg) * 14}" font-family="sans-serif" font-size="11" fill="{colors[strategy]}">{strategy}: {mech}</text>')
        svg.append('</svg>')
        (out / "comparison.svg").write_text("\n".join(svg), encoding="utf-8")
        print("matplotlib unavailable; wrote SVG chart")
    print(f"Wrote {len(rows)} experiment rows to {out}")


if __name__ == "__main__":
    main()

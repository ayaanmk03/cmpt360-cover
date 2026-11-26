"""Plot the benchmark results from runtime.csv."""

import csv
from pathlib import Path
from statistics import median

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def plot_series(ax, rows, series, size_column, xlabel, title):
    groups = {}
    for row in rows:
        if row["series"] == series:
            groups.setdefault(int(row[size_column]), []).append(row)

    sizes = sorted(groups)
    for column, label, marker, color in [
        ("baseline_ms", "Exhaustive search", "o", "#a6431b"),
        ("faster_ms", "Interval DP", "s", "#176878"),
    ]:
        times = [median(float(row[column]) for row in groups[n]) for n in sizes]
        ax.plot(sizes, times, marker=marker, color=color, label=label)

    ax.set(title=title, xlabel=xlabel, yscale="log")
    ax.set_xticks(sizes)
    ax.grid(axis="y", alpha=0.25)


def main():
    results = Path(__file__).parent / "results"
    with (results / "runtime.csv").open(newline="") as file:
        rows = list(csv.DictReader(file))

    fig, axes = plt.subplots(1, 2, figsize=(9, 4), sharey=True)
    plot_series(axes[0], rows, "sprinklers", "sprinklers", "Sprinklers",
                "20 trees and 20 cacti")
    plot_series(axes[1], rows, "plants", "trees", "Trees and cacti (count of each)",
                "10 sprinklers")
    axes[0].set_ylabel("Median runtime (ms, log scale)")
    axes[0].yaxis.set_major_formatter("{x:g}")
    axes[0].legend(frameon=False)
    fig.suptitle("Cover algorithm runtimes", fontweight="bold")
    fig.tight_layout()
    output = results / "runtime_comparison.png"
    fig.savefig(output, dpi=220)
    plt.close(fig)
    print(f"Saved {output.name}")


if __name__ == "__main__":
    main()

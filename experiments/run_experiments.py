"""Run from the project root with python3 -m experiments.run_experiments."""

import csv
from pathlib import Path
from random import Random
from statistics import median
from time import perf_counter_ns

from baseline import exhaustive_cover
from fasterAlgo import faster_cover


def make_instance(seed, sprinkler_count, plant_count):
    """Generate nested instances with plant_count trees and as many cacti."""
    rng = Random(seed)
    points = rng.sample(range(400), 400)
    trees = points[:200]
    cacti = points[200:]

    # Four fixed sprinklers cover the whole line, so every instance is feasible.
    anchors = [50, 150, 250, 350]
    candidates = [p for p in range(400) if p not in anchors]
    rng.shuffle(candidates)
    positions = anchors + candidates
    radii = [50] * len(anchors) + [rng.randint(5, 40) for _ in candidates]
    return trees[:plant_count], cacti[:plant_count], positions[:sprinkler_count], radii[:sprinkler_count]


def measure(solver, instance):
    times = []
    for _ in range(3):
        start = perf_counter_ns()
        result = solver(*instance)
        times.append((perf_counter_ns() - start) / 1_000_000)
    return result, median(times)


def main():
    settings = [('sprinklers', k, 20) for k in (6, 8, 10, 12, 14)]
    settings += [('plants', 10, n) for n in (5, 10, 20, 40, 80)]
    rows = []
    for series, k, n in settings:
        for seed in (360, 361, 362):
            instance = make_instance(seed, k, n)
            baseline, baseline_ms = measure(exhaustive_cover, instance)
            faster, faster_ms = measure(faster_cover, instance)
            if baseline is None or faster is None or baseline[1] != faster[1]:
                raise ValueError(f"Unexpected result for {series=}, {k=}, {n=}, {seed=}")
            rows.append((series, k, n, n, seed, baseline[1], baseline_ms, faster_ms))
        print(f"{series:10}  sprinklers={k:2}  trees={n:2}  cacti={n:2}  3 seeds matched")

    output = Path(__file__).parent / 'results' / 'runtime.csv'
    output.parent.mkdir(exist_ok=True)
    with output.open('w', newline='') as file:
        writer = csv.writer(file, lineterminator='\n')
        writer.writerow(('series', 'sprinklers', 'trees', 'cacti', 'seed',
                         'watered_cacti', 'baseline_ms', 'faster_ms'))
        writer.writerows(rows)
    print(f"Saved {len(rows)} timing comparisons to {output.name}")


if __name__ == '__main__':
    main()

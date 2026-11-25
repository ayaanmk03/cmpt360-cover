from bisect import bisect_left, bisect_right
from math import inf

from baseline import sprinkler_intervals


def faster_cover(oranges, cacti, positions, radii):
    """Return (selected positions, watered cactus count), or None if infeasible."""
    intervals = sprinkler_intervals(positions, radii)
    if not oranges:
        return [], 0

    trees = sorted(oranges)
    cactus_points = sorted(cacti)
    order = sorted(range(len(intervals)), key=lambda i: intervals[i][1])

    # Each pair of ranks bounds the plants inside one closed interval.
    tree_spans = []
    cactus_spans = []
    for index in order:
        left, right = intervals[index]
        tree_spans.append((bisect_left(trees, left), bisect_right(trees, right)))
        cactus_spans.append((bisect_left(cactus_points, left), bisect_right(cactus_points, right)))

    # cost[j] is the minimum for a cover ending at j with no missed tree
    # up to its right endpoint. To remove a contained sprinkler we need
    # chains with both endpoints which are strictly increasing.
    cost = [inf] * len(order)
    parent = [None] * len(order)
    best_end = None
    for j, index in enumerate(order):
        left, right = intervals[index]
        trees_before, trees_through = tree_spans[j]
        cacti_before, cacti_through = cactus_spans[j]
        if trees_before == 0:
            cost[j] = cacti_through - cacti_before

        for i in range(j):
            prev_left, prev_right = intervals[order[i]]
            if prev_left >= left or prev_right >= right or tree_spans[i][1] < trees_before:
                continue
            # Any overlap is already watered by the preceding interval.
            added = cacti_through - max(cacti_before, cactus_spans[i][1])
            candidate = cost[i] + added
            if candidate < cost[j]:
                cost[j] = candidate
                parent[j] = i

        if trees_through == len(trees) and cost[j] < inf:
            if best_end is None or cost[j] < cost[best_end]:
                best_end = j

    if best_end is None:
        return None

    selected = []
    current = best_end
    while current is not None:
        selected.append(order[current])
        current = parent[current]
    return [positions[i] for i in sorted(selected)], cost[best_end]

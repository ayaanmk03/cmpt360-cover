from itertools import combinations


def sprinkler_intervals(positions, radii):
    """Return each sprinkler's inclusive (left, right) interval in input order."""
    if len(positions) != len(radii):
        raise ValueError("Each sprinkler must have one radius.")

    intervals = []
    for position, radius in zip(positions, radii):
        if radius < 0:
            raise ValueError("Sprinkler radii must be nonnegative.")
        intervals.append((position - radius, position + radius))

    return intervals


def exhaustive_cover(oranges, cacti, positions, radii):
    """Return (selected positions, watered cactus count), or None if infeasible."""
    intervals = sprinkler_intervals(positions, radii)
    best = None

    for size in range(len(intervals) + 1):
        for selected in combinations(range(len(intervals)), size):
            def is_watered(point):
                return any(intervals[i][0] <= point <= intervals[i][1] for i in selected)

            if not all(is_watered(orange) for orange in oranges):
                continue

            # Check each cactus once even if several sprinklers reach it.
            count = sum(is_watered(cactus) for cactus in cacti)
            if best is None or count < best[1]:
                best = ([positions[i] for i in selected], count)
                if count == 0:
                    return best

    return best

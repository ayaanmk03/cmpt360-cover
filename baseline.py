from itertools import combinations


def sprinkler_intervals(positions, radii):
    """Return each sprinkler's inclusive (left, right) interval in input order.

    Pair each position with the radius at the same index. Raise ValueError
    if the lengths differ or any radius is negative.
    """
    if len(positions) != len(radii):
        raise ValueError("Each sprinkler must have one radius.")

    intervals = []
    for position, radius in zip(positions, radii):
        if radius < 0:
            raise ValueError("Sprinkler radii must be nonnegative.")
        intervals.append((position - radius, position + radius))

    return intervals


def exhaustive_cover(oranges, cacti, positions, radii):
    """Cover every orange tree while minimizing the number of cacti watered.

    oranges and cacti contain plant positions. Each cactus counts once even
    when several selected sprinklers reach it. Return the selected sprinkler
    positions in input order and the minimum cactus count as a pair.
    Return ([], 0) for no orange trees or None if full coverage is impossible.
    """
    intervals = sprinkler_intervals(positions, radii)
    best = None

    for size in range(len(intervals) + 1):
        for selected in combinations(range(len(intervals)), size):
            def is_watered(point):
                """Return whether any selected sprinkler reaches this position."""
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

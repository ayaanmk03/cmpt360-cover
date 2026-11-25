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

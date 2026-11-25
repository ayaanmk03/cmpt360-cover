import random
import unittest

from baseline import exhaustive_cover
from fasterAlgo import faster_cover


class FasterCoverTests(unittest.TestCase):
    def test_touching_intervals_count_shared_endpoint_once(self):
        result = faster_cover([4, 0], [2], [3, 1], [1, 1])
        self.assertEqual(result, ([3, 1], 1))

    def test_gap_can_leave_cacti_dry(self):
        result = faster_cover([0, 10], [5], [5, 0, 10], [5, 0, 0])
        self.assertEqual(result, ([0, 10], 0))

    def test_gap_cannot_skip_an_orange(self):
        self.assertIsNone(faster_cover([0, 5, 10], [], [0, 10], [1, 1]))

    def test_nested_intervals_with_same_right_endpoint(self):
        # Both intervals end at 4. Only the shorter one spares the cactus at 0.
        self.assertEqual(faster_cover([4], [0], [2, 3], [2, 1]), ([3], 0))

    def test_no_oranges(self):
        self.assertEqual(faster_cover([], [1], [1], [1]), ([], 0))

    def test_no_sprinklers(self):
        self.assertIsNone(faster_cover([0], [], [], []))

    def test_seeded_cases_against_exhaustive_search(self):
        rng = random.Random(360)
        for case in range(300):
            positions = rng.sample(range(-6, 7), rng.randrange(8))
            radii = [rng.randrange(5) for _ in positions]
            oranges = rng.sample(range(-8, 9), rng.randrange(7))
            cacti = rng.sample(range(-8, 9), rng.randrange(7))
            with self.subTest(case=case):
                expected = exhaustive_cover(oranges, cacti, positions, radii)
                result = faster_cover(oranges, cacti, positions, radii)
                if expected is None:
                    self.assertIsNone(result)
                    continue

                self.assertIsNotNone(result)
                selected, count = result
                self.assertEqual(count, expected[1])

                # Verify the returned sprinklers even when optimal subsets tie.
                radius_at = dict(zip(positions, radii))
                def watered(point):
                    return any(abs(point - p) <= radius_at[p] for p in selected)

                self.assertTrue(all(watered(tree) for tree in oranges))
                self.assertEqual(sum(watered(cactus) for cactus in cacti), count)

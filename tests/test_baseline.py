import unittest

from baseline import exhaustive_cover, sprinkler_intervals


class BaselineTests(unittest.TestCase):
    def test_readme_example(self):
        result = exhaustive_cover([2, 6, 11], [4, 8, 14], [3, 7, 12], [2, 2, 1])
        self.assertEqual(result, ([3, 7, 12], 2))

    def test_two_narrow_sprinklers_spare_the_middle_cactus(self):
        # The sprinkler at 5 reaches both trees but also waters the cactus.
        result = exhaustive_cover([0, 10], [5], [5, 0, 10], [5, 0, 0])
        self.assertEqual(result, ([0, 10], 0))

    def test_shared_cactus_counts_once(self):
        result = exhaustive_cover([0, 4], [2], [1, 3], [1, 1])
        self.assertEqual(result, ([1, 3], 1))

    def test_no_oranges(self):
        self.assertEqual(exhaustive_cover([], [2], [2], [1]), ([], 0))

    def test_no_sprinklers(self):
        self.assertIsNone(exhaustive_cover([2], [], [], []))

    def test_one_orange_out_of_reach(self):
        self.assertIsNone(exhaustive_cover([0, 3], [], [0], [2]))

    def test_no_cacti_and_trees_at_both_endpoints(self):
        self.assertEqual(exhaustive_cover([-2, 2], [], [0], [2]), ([0], 0))

    def test_intervals_preserve_order_and_zero_radius(self):
        self.assertEqual(sprinkler_intervals([5, -1], [0, 2]), [(5, 5), (-3, 1)])

    def test_missing_radius(self):
        with self.assertRaises(ValueError):
            sprinkler_intervals([1, 2], [1])

    def test_negative_radius(self):
        with self.assertRaises(ValueError):
            sprinkler_intervals([1], [-1])

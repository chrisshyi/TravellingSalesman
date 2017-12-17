from unittest import TestCase
from tsp import generate_all_subsets, Point
from math import isclose


class TestTsp(TestCase):
    def test_generate_subset(self):
        subsets = generate_all_subsets(3, {1, 2, 3, 4}, 1, 3)
        self.assertTrue(len(subsets), 2)
        self.assertTrue({1, 2, 3} in subsets)
        self.assertTrue({1, 3, 4} in subsets)

    def test_generate_subset_larger(self):
        subsets = generate_all_subsets(3, {1, 2, 3, 4, 5}, 1, 3)
        self.assertTrue(len(subsets), 3)
        self.assertTrue({1, 3, 2} in subsets)
        self.assertTrue({1, 2, 3} in subsets)
        self.assertTrue({1, 3, 4} in subsets)
        self.assertTrue({1, 3, 5} in subsets)

    def test_point_distance(self):
        point1 = Point(0, 0)
        point2 = Point(3.0, 4.0)
        distance = point1.distance_to(point2)
        print(distance)
        self.assertTrue(isclose(distance, 5.0, rel_tol=1e-4))

    def test_point_distance2(self):
        point1 = Point(0, 0)
        point2 = Point(12.0000, 5.000001)
        distance = point1.distance_to(point2)
        print(distance)
        self.assertTrue(isclose(distance, 13.0, rel_tol=1e-6))

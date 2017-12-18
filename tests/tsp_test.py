from unittest import TestCase
import unittest
from tsp import generate_all_subsets, Point, extract_data, find_min_tour
from math import isclose


class TestTsp(TestCase):

    def test_generate_subset(self):
        subsets = generate_all_subsets(3, {1, 2, 3, 4}, 1)
        self.assertTrue(len(subsets), 2)
        self.assertTrue({1, 2, 3} in subsets)
        self.assertTrue({1, 3, 4} in subsets)

    def test_generate_subset_larger(self):
        subsets = generate_all_subsets(3, {1, 2, 3, 4, 5}, 1)
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

    def test_data_extraction_point_set(self):
        data_points, points_to_coordinates, point_distances = TestTsp.extract_data_from_file("tests/test1.txt")
        self.assertEquals(len(data_points), 3)

    def test_data_extraction_points_to_coordinates(self):
        data_points, points_to_coordinates, point_distances = TestTsp.extract_data_from_file("tests/test1.txt")
        self.assertEquals(points_to_coordinates[1].x_cor, 0.000)
        self.assertEquals(points_to_coordinates[1].y_cor, 0.000)
        self.assertEquals(points_to_coordinates[2].x_cor, 3.000)
        self.assertEquals(points_to_coordinates[2].y_cor, 4.000)

    def test_data_extraction_point_distances(self):
        data_points, points_to_coordinates, point_distances = TestTsp.extract_data_from_file("tests/test1.txt")
        one_to_two = frozenset([1, 2])
        two_to_three = frozenset([2, 3])
        one_to_three = frozenset([1, 3])
        self.assertTrue(isclose(point_distances[one_to_two], 5.000, rel_tol=1e-3))
        self.assertTrue(isclose(point_distances[two_to_three], 9.0553, rel_tol=1e-4))
        self.assertTrue(isclose(point_distances[one_to_three], 13.000, rel_tol=1e-3))

    def test_min_tour_distance_three_points(self):
        data_points, points_to_coordinates, point_distances = TestTsp.extract_data_from_file("tests/test1.txt")
        self.assertTrue(isclose(find_min_tour(data_points, point_distances), 27.055, rel_tol=1e-3))

    def test_min_tour_distance_four_points(self):
        data_points, points_to_coordinates, point_distances = TestTsp.extract_data_from_file("tests/test2.txt")
        min_tour_dist = find_min_tour(data_points, point_distances)
        print(min_tour_dist)
        self.assertTrue(isclose(min_tour_dist, 31.783, rel_tol=1e-3))

    @staticmethod
    def extract_data_from_file(file):
        return extract_data(file)


if __name__ == '__main__':
    unittest.main()
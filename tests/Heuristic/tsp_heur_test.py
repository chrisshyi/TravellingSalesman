from unittest import TestCase
from math import isclose
from tsp_heuristic import extract_data, find_min_tour


class TspHeurTest(TestCase):

    def test_small_input(self):
        point_set, point_coordinates, x_coor_dict, first_point_indices = extract_data("test1.txt")
        self.assertTrue(isclose(30.0, find_min_tour(point_set, point_coordinates, x_coor_dict, first_point_indices)))

    def test_small_input2(self):
        point_set, point_coordinates, x_coor_dict, first_point_indices = extract_data("test2.txt")
        self.assertTrue(isclose(15.2361, find_min_tour(point_set, point_coordinates, x_coor_dict, first_point_indices), rel_tol=1e-4))

    def test_small_input3(self):
        point_set, point_coordinates, x_coor_dict, first_point_indices = extract_data("test4.txt")
        self.assertTrue(isclose(70.000, find_min_tour(point_set, point_coordinates, x_coor_dict, first_point_indices), rel_tol=1e-4))

    def test_x_coor_dict(self):
        point_set, point_coordinates, x_coor_dict, first_point_indices = extract_data("test3.txt")
        self.assertEqual(len(x_coor_dict[1]), 2)
        self.assertTrue(1 in x_coor_dict[1])
        self.assertTrue(2 in x_coor_dict[1])
        self.assertEqual(len(x_coor_dict[3]), 3)
        self.assertTrue(3 in x_coor_dict[3])
        self.assertTrue(4 in x_coor_dict[3])
        self.assertTrue(5 in x_coor_dict[3])
        self.assertEqual(len(x_coor_dict[6]), 1)
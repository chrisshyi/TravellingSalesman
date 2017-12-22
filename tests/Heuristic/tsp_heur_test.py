from unittest import TestCase
from math import isclose
from tsp_heuristic import extract_data, find_min_tour


class TspHeurTest(TestCase):

    def test_small_input(self):
        point_set, point_coordinates = extract_data("test1.txt")
        self.assertTrue(isclose(30.0, find_min_tour(point_set, point_coordinates)))
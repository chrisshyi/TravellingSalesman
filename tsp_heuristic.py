from tsp import Point
from heapq import heapify, heappop, heappush
from functools import total_ordering
from math import inf


def extract_data(data_file):
    """
        extract points from a data_file

        :param data_file: .txt file containing the point data, first line is the number of points
        :return (set of points, dictionary of points to coordinates, dictionary of point pairs to the distance between them)
        """

    data_points = set()
    points_to_coordinates = {}

    with open(data_file) as input_file:
        # consume the first line, it only tells us how many points there are
        input_file.readline()
        line_count = 0
        for line in input_file:
            line_count += 1
            line = line.strip('\n')
            split_line = line.split(" ")
            print(split_line)
            new_point = Point(float(split_line[1]), float(split_line[2]))
            points_to_coordinates[line_count] = new_point
            data_points.add(line_count)

    # Don't need to cache the distances between all point pairs

    # point_distances = {}
    # for point in data_points:
    #     for other_point in data_points:
    #         if point == other_point:
    #             pass
    #         point_distances[frozenset([point, other_point])] \
    #             = points_to_coordinates[point].distance_to(points_to_coordinates[other_point])
    return data_points, points_to_coordinates


# total_ordering decorator helps define the natural ordering of a class
@total_ordering
class HeapNode:
    """
    Represents a node in the min heap
    """
    def __init__(self, point, score):
        self.point = point
        self.score = score
        """
        indicates whether this node has been removed from the heap  
        used for custom remove operation
        """
        self.REMOVED = False

    def __lt__(self, other):
        return self.score < other.score

    def __eq__(self, other):
        return self.point == other.point


def remove_from_heap(heap, node, entry_dict):
    """

    :param heap: the heap from which the removal is to be done
    :param node: the node to be removed
    :param entry_dict: a dictionary mapping points(cities) to HeapNodes
    :return:
    """
    pass


def pop_from_heap():
    pass


def find_min_tour(point_set, point_coordinates):
    """

    :param point_set: set of points (integers)
    :param point_coordinates: dictionary mapping point numbers to Point objects
    :return: the length of the minimum tour, using a greedy heuristic
    """
    # using a list here since the order matters, if not then should use a set
    visited_cities = []
    # heap containing all the cities that have not yet been visited
    city_heap = []
    num_cities = len(point_set)
    min_tour_length = 0
    # closest_city = 1
    # closest_distance = inf
    #
    # while len(visited_cities) != num_cities:
    #     visited_cities.append(closest_city)
    #     for city in range(1, num_cities + 1):
    #         if city in visited_cities:
    #             continue

    # Heap implementation too slow...
    # initialize the heap
    for point in range(1, num_cities + 1):
        score = inf
        if point == 1:
            score = 0
        heappush(city_heap, HeapNode(point, score))

    while len(city_heap) != 0:
        print("{} cities left".format(str(len(city_heap))))
        closest_city = heappop(city_heap)
        min_tour_length += closest_city.score
        visited_cities.append(closest_city.point)
        closest_city_point = point_coordinates[closest_city.point]
        for city in range(1, num_cities + 1):
            if city == closest_city.point or city in visited_cities:
                continue
            city_point = point_coordinates[city]
            # need to recalculate the score for each city
            city_heap.remove(HeapNode(city, inf))
            new_node = HeapNode(city, closest_city_point.distance_to(city_point))
            city_heap.append(new_node)
        heapify(city_heap)

    last_city = visited_cities[len(visited_cities) - 1]
    min_tour_length += point_coordinates[last_city].distance_to(point_coordinates[1])
    print("Minimum tour length: " + str(min_tour_length))
    return min_tour_length


def main():
    point_set, point_coordinates = extract_data("large_dataset.txt")
    find_min_tour(point_set, point_coordinates)


if __name__ == "__main__":
    main()

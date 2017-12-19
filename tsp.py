""" import the matpltlib library for plotting """
import matplotlib.pyplot as plt
import math
import copy
import statistics


class Point:
    """
    Represents a point in 2D space
    """
    def __init__(self, x_coordinate, y_coordinate):
        self.x_cor = x_coordinate
        self.y_cor = y_coordinate

    def distance_to(self, point):
        """
        Calculate the Euclidean distance from this point to another

        :param point: another Point object
        """
        return math.sqrt((self.x_cor - point.x_cor)**2 + (self.y_cor - point.y_cor)**2)

    def __eq__(self, other):
        """
        Defines the comparison of one Point object to another
        :return: True if the other Point object is equivalent to this one
        """
        if not type(other) == Point:
            return False
        return self.x_cor == other.x_cor and self.y_cor == other.y_cor


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
            new_point = Point(float(split_line[0]), float(split_line[1]))
            points_to_coordinates[line_count] = new_point
            data_points.add(line_count)

    point_distances = {}
    for point in data_points:
        for other_point in data_points:
            if point == other_point:
                pass
            point_distances[frozenset([point, other_point])] \
                = points_to_coordinates[point].distance_to(points_to_coordinates[other_point])
    return data_points, points_to_coordinates, point_distances


def plot_points(points_map):
    """
    plot the points in tsp.txt using matplotlib

    :param points_map: a dictionary mapping points(int) to Point objects
    """
    # Extract x,y values into their own lists
    x_val = [point.x_cor for key, point in points_map.items()]
    print(x_val)
    y_val = [point.y_cor for key, point in points_map.items()]
    print(y_val)

    fig, ax = plt.subplots()

    ax.plot(x_val, y_val, 'ro')

    for x in range(1, len(x_val) + 1):
        # Annotate the points
        ax.annotate(str(x), (x_val[x - 1], y_val[x - 1]))

    plt.show()


def generate_all_subsets_with_source(size, parent_set, source):
    parent_set_copy = copy.deepcopy(parent_set)
    parent_set_copy.remove(source)
    subsets = generate_all_subsets(size - 1, parent_set_copy)
    for subset in subsets:
        subset.add(source)
    return subsets


def generate_all_subsets(size, parent_set):
    """
    generates all subsets of points with a given size for a parent set
    :param size: the size of subsets to generate
    :param parent_set: the parent point set
    :return: a list of all generated subsets
    """
    if size == len(parent_set):
        return [parent_set]
    if size == 0:
        return [set()]

    subsets = []
    # for every point that's not the source or the dest, generate subset of size (size - 1) / size
    # with or without that point
    print("Generating subsets for problem size " + str(size))
    point = parent_set.pop()
    parent_set.add(point)

    parent_set_copy = copy.deepcopy(parent_set)
    parent_set_copy.remove(point)
    if len(parent_set_copy) >= size - 1:
        with_point = generate_all_subsets(size - 1, parent_set_copy)
        print("Generated subset with point\n")
        print(with_point)
        print("\n")
        for subset in with_point:
            subset.add(point)
        subsets.extend(with_point)

    parent_set_copy2 = copy.deepcopy(parent_set)
    parent_set_copy2.remove(point)
    if len(parent_set_copy2) >= size:
        without_point = generate_all_subsets(size, parent_set_copy2)
        subsets.extend(without_point)

    return subsets


def find_min_tour(point_set, point_distances, source_point):
    """
    Computes the minimum tour for a point set using a dynamic programming algorithm

    :param source_point: the source point from which to begin the computation
    :param point_set: set of points forming a complete graph (set of integers)
    :param point_distances: dictionary of sets of points(integers) mapped to the distance between them
    :return: the length of the minimum tour using Euclidean distance between the points
    """
    num_vertices = len(point_set)
    '''
    maps (S, j) to their minimum tour length, where S is the set of vertices on the path,
    and j is the destination
    '''
    tour_map = {(frozenset([source_point]), source_point): 0}

    for problem_size in range(2, num_vertices + 1):
        if problem_size == 2:
            for vertex in range(source_point + 1, source_point + num_vertices):
                tour_map[frozenset([source_point, vertex]), vertex] = point_distances[frozenset([source_point, vertex])]
            continue
        for subset in generate_all_subsets_with_source(problem_size, point_set, source_point):
            for point in subset:
                print("Problem Size: " + str(problem_size) + " Point: " + str(point) + "\n")
                min_distance = math.inf
                if point == source_point:
                    continue
                # For every other point in the set beside the point under consideration
                for other_point in subset:
                    if other_point == point or other_point == source_point:
                        continue
                    # remove the point under consideration from the subset
                    exclude_point = copy.deepcopy(subset)
                    exclude_point.remove(point)
                    exclude_point = frozenset(exclude_point)
                    candidate_distance = tour_map[exclude_point, other_point] + point_distances[frozenset([point, other_point])]
                    if candidate_distance < min_distance:
                        min_distance = candidate_distance
                tour_map[frozenset(subset), point] = min_distance
    min_tour_distance = math.inf
    for vertex in range(source_point + 1, source_point + num_vertices):
        candidate_min_tour = tour_map[frozenset(point_set), vertex] + point_distances[frozenset([source_point, vertex])]
        if candidate_min_tour < min_tour_distance:
            min_tour_distance = candidate_min_tour
    return min_tour_distance


def main():
    """
    The main function for executing a dynamic programming solution to the
    traveling salesman problem.
    """

    data_points, points_to_coordinates, point_distances = extract_data('tsp.txt')
    plot_points(points_to_coordinates)

    first_cluster = set([x for x in range(1, 14)])
    second_cluster = set([x for x in range(12, 26)])

    print("Calculating first cluster\n")
    min_tour_first = find_min_tour(first_cluster, point_distances, 1)

    print("Calculating second cluster\n")
    min_tour_second = find_min_tour(second_cluster, point_distances, 12)
    print("min tour for first cluster: " + str(min_tour_first) + "\n")
    print("min tour for second cluster: " + str(min_tour_second) + "\n")

    point_12 = points_to_coordinates[12]
    point_13 = points_to_coordinates[13]

    common_edge = point_12.distance_to(point_13)

    final_tour_length = min_tour_first + min_tour_second - 2 * common_edge

    # final_tour_length = find_min_tour(data_points, point_distances, 1)

    print("minimum tour is: " + str(final_tour_length))


if __name__ == "__main__":
    main()

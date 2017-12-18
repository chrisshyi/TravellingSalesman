""" import the matpltlib library for plotting """
import matplotlib.pyplot as plt
import math
import copy


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


def plot_points(points_list):
    """
    plot the points in tsp.txt using matplotlib

    :param points_list: a list of Point objects
    """
    # Extract x,y values into their own lists
    x_val = [point.x_cor for point in points_list]
    print(x_val)
    y_val = [point.y_cor for point in points_list]
    print(y_val)

    fig, ax = plt.subplots()

    ax.plot(x_val, y_val, 'ro')

    for x in range(1, 26):
        # Annotate the points from 1 - 25
        ax.annotate(str(x), (x_val[x - 1], y_val[x - 1]))

    plt.show()


def generate_all_subsets(size, parent_set, source):
    """
    generates all subsets of points with a given size for a parent set
    :param size: the size of subsets to generate
    :param parent_set: the parent point set
    :param source: the source point
    :return: a list of all generated subsets
    """
    if size == len(parent_set):
        return [parent_set]
    subsets = []
    # for every point that's not the source or the dest, generate subset of size (size - 1) / size
    # with or without that point
    for point in parent_set:
        if point == source:
            continue
        parent_set_copy = copy.deepcopy(parent_set)
        parent_set_copy.remove(point)
        if len(parent_set_copy) >= size:
            with_point = generate_all_subsets(size - 1, parent_set_copy, source)
            for subset in with_point:
                if not len(subset) == 0:
                    subset.add(point)
            subsets.extend(with_point)

        parent_set_copy2 = copy.deepcopy(parent_set)
        parent_set_copy2.remove(point)
        if len(parent_set_copy2) >= size:
            without_point = generate_all_subsets(size, parent_set_copy2, source)
            subsets.extend(without_point)
    return subsets


def find_min_tour(point_set, point_distances):
    """
    Computes the minimum tour for a point set using a dynamic programming algorithm

    :param point_set: set of points forming a complete graph (set of integers)
    :param point_distances: dictionary of sets of points(integers) mapped to the distance between them
    :return: the length of the minimum tour using Euclidean distance between the points
    """
    num_vertices = len(point_set)
    source_point = 1
    '''
    maps (S, j) to their minimum tour length, where S is the set of vertices on the path,
    and j is the destination
    '''
    tour_map = {(frozenset([1]), 1): 0}

    for problem_size in range(2, num_vertices + 1):
        if problem_size == 2:
            for vertex in range(2, num_vertices + 1):
                tour_map[frozenset([1, vertex]), vertex] = point_distances[frozenset([1, vertex])]
            continue
        for subset in generate_all_subsets(problem_size, point_set, source_point):
            for point in subset:
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
    for vertex in range(2, num_vertices + 1):
        candidate_min_tour = tour_map[frozenset(point_set), vertex] + point_distances[frozenset([1, vertex])]
        if candidate_min_tour < min_tour_distance:
            min_tour_distance = candidate_min_tour
    return min_tour_distance


def main():
    """
    The main function for executing a dynamic programming solution to the
    traveling salesman problem.
    """
    points_list = extract_data('tsp.txt')
    plot_points(points_list)


if __name__ == "__main__":
    main()

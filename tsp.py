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
    :return: a list of Point objects
    """

    data_points = []

    with open(data_file) as input_file:
        # consume the first line, it only tells us how many points there are
        input_file.readline()
        for line in input_file:
            line = line.strip('\n')
            split_line = line.split(" ")
            print(split_line)
            new_point = Point(float(split_line[0]), float(split_line[1]))
            data_points.append(new_point)

    return data_points


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


def generate_all_subsets(size, parent_set, source, dest):
    """
    generates all subsets of points with a given size for a parent set
    :param size: the size of subsets to generate
    :param parent_set: the parent point set
    :param source: the source point
    :param dest: the destination point
    :return: a list of all generated subsets
    """
    if size == len(parent_set):
        return [parent_set]
    if size > len(parent_set):
        return []
    subsets = []
    # for every point that's not the source or the dest, generate subset of size (size - 1) / size
    # with or without that point
    for point in parent_set:
        if point == source or point == dest:
            continue
        parent_set_copy = copy.deepcopy(parent_set)
        parent_set_copy.remove(point)
        with_point = generate_all_subsets(size - 1, parent_set_copy, source, dest)
        for subset in with_point:
            if not len(subset) == 0:
                subset.add(point)
        subsets.extend(with_point)

        parent_set_copy2 = copy.deepcopy(parent_set)
        parent_set_copy2.remove(point)
        without_point = generate_all_subsets(size, parent_set_copy2, source, dest)
        subsets.extend(without_point)
    return subsets


def find_min_tour(point_set):
    """
    Computes the minimum tour for a point set using a dynamic programming algorithm
    :param point_set: set of points forming a complete graph
    :return: the length of the minimum tour using Euclidean distance between the points
    """
    pass


def main():
    """
    The main function for executing a dynamic programming solution to the
    traveling salesman problem.
    """
    points_list = extract_data('tsp.txt')
    plot_points(points_list)


if __name__ == "__main__":
    main()

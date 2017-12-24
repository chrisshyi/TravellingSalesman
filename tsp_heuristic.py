from tsp import Point
from math import inf


def extract_data(data_file):
    """
        extract points from a data_file

        :param data_file: .txt file containing the point data, first line is the number of points
        :return (set of points, dictionary of points to coordinates, dictionary mapping the first point with a
        given x coordinate to a list of points with the same x coordinate, list of first point indices)
        """

    data_points = set()
    points_to_coordinates = {}
    x_coor_dict = {}
    # need this since we need to iterate through the first point indices in a fixed order
    first_point_indices = []

    with open(data_file) as input_file:
        # consume the first line, it only tells us how many points there are
        input_file.readline()
        point_number = 0
        current_x_coor = inf
        # point that's used as the indexing point for a list of points with the same x coordinates
        first_point_index = 1

        for line in input_file:
            point_number += 1
            line = line.strip('\n')
            split_line = line.split(" ")
            print(split_line)
            x_coor = float(split_line[1])
            # if we're seeing this x coordinate for the first time
            if current_x_coor != x_coor:
                first_point_index = point_number
                first_point_indices.append(first_point_index)
                x_coor_dict[first_point_index] = []
                current_x_coor = x_coor
            x_coor_dict[first_point_index].append(point_number)
            new_point = Point(x_coor, float(split_line[2]))
            points_to_coordinates[point_number] = new_point
            data_points.add(point_number)

    return data_points, points_to_coordinates, x_coor_dict, first_point_indices


def find_min_tour(point_set, point_coordinates, x_coor_dict, first_point_indices):
    """
    Finds the minimum tour for a given set of points. Assumes that the point data in its original format
    is sorted by x-coordinates and by y-coordinates for points with the same x-coordinate

    :param point_set: set of points (integers)
    :param point_coordinates: dictionary mapping point numbers to Point objects
    :param x_coor_dict: dictionary mapping the first point with a
    given x coordinate to a list of points with the same x coordinate
    :param first_point_indices: list of first point indices used in the x_coor_dict as keys
    :return: the length of the minimum tour, using a greedy heuristic
    """
    # using a list here since the order matters, if not then should use a set
    visited_cities = [1, ]  # start at city 1
    visited_cities_set = set()
    visited_cities_set.add(1)
    num_cities = len(point_set)
    min_tour_length = 0.00000

    current_city = 1
    closest_point = 1
    closest_dist = inf

    while len(visited_cities_set) != num_cities:
        cities_left = num_cities - len(visited_cities)
        print("{} cities left".format(str(cities_left)))

        # iterating through all the points this way since there might be a way to
        # optimize the algorithm by taking advantage of the fact that the points
        # are sorted (by x first and then by y)
        for first_point_index in first_point_indices:
            for point in x_coor_dict[first_point_index]:
                # checking whether the point is visited already must be done using a set
                # using a list would involve linear search and slows the program down
                # as the visited cities grow in number
                if point == current_city or point in visited_cities_set:
                    continue
                current_city_point = point_coordinates[current_city]
                other_city_point = point_coordinates[point]

                distance = current_city_point.distance_to(other_city_point)
                if distance < closest_dist:
                    closest_dist = distance
                    closest_point = point
        visited_cities.append(closest_point)
        visited_cities_set.add(closest_point)
        current_city = closest_point
        min_tour_length += closest_dist
        closest_dist = inf

    # calculate the distance from the last city to the first to complete the tour
    last_city = visited_cities[len(visited_cities) - 1]
    last_city_point = point_coordinates[last_city]
    first_city_point = point_coordinates[1]
    min_tour_length += first_city_point.distance_to(last_city_point)

    print("Minimum tour length: " + str(min_tour_length))
    return min_tour_length


def main():
    point_set, point_coordinates, x_coor_dict, first_point_indices = extract_data("large_dataset.txt")
    find_min_tour(point_set, point_coordinates, x_coor_dict, first_point_indices)


if __name__ == "__main__":
    main()

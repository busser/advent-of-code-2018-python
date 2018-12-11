"""Solution de day 06 of the Advent of Code.

Reading input:
    The input provides coordinates as comma-separated strings. We can extract
    the two integers we want with regular expressions or with Python's
    string.split function. Coordinates are stored as tuples (and not NamedTuples
    which are much slower). See _read_coordinates function.

Normalizing coordinates:
    To make our work easier, we are going to normalize our coordinates. This
    means that the coordinates will be shifted so that they have the smallest
    possible positive values while keeping their relative positions. See
    _normalize_coordinates function.

Building a matrix:
    We can build our matrix in memory as a list of lists. See _build_matrix
    function.

Manhattan distance:
    The Manhattan distance is a very simple computation that relies on Python's
    abs function to compute absolute values. See _manhattan_distance function.

Areas of influence:
    We need to map each cell of our matrix to the closest coordinate. We can
    find the distance from the cell to each coordinate and assign the cell to
    the closest coordinate. In case of tie, no coordinate is assigned. See
    _fill_matrix function.

Area sizes:
    Measuring the size of all areas is only a question of counting how many
    cells were assigned to each coordinate in the previous step. See
    _get_area_sizes function.

Infinite areas:
    Areas that are adjacent to the side of our matrix are infinite. We can use
    this to identifiy infinite areas. See _get_infinite_area_points function.

Part 1:
    We can build and fill a matrix based on the normalised coordinates, get the
    size of each area, discard areas that are infinite, and find the largest
    finite area. See get_largest_finite_area function.

Sum of distances:
    Since we already know how to compute the distance between a cell of the
    matrix and any coordinate, we can easily compute the sum of all distances
    (one for each coordinate). See _get_total_distance function.

Part 2:
    We can build a matrix based on the normalised coordinates and count how
    many cells have a total distance from all coordinates that is below a
    certain threshold. See get_safe_area function.
"""

import re
from typing import Dict, List, Set, Tuple

import utils

Point = Tuple[int, int]


def _read_coordinates(input_string: str) -> List[Point]:
    """Reads coordinates from a given input string.

    Args:
        input_string: A string containing the day's input.

    Returns:
        A list of coordinates.
    """
    return [
        tuple(int(n)
              for n in re.findall('[0-9]+', line))
        for line in input_string.split('\n')
    ]


def _normalize_coordinates(coordinates: List[Point]) -> List[Point]:
    """Normalizes a list of coordinates.

    Makes all coordinates have the smallest possible positive values.

    Args:
        coordinates: A list of coordinates to normalize.

    Returns:
        A list of normalized coordinates.
    """
    min_x = min([coordinate[0] for coordinate in coordinates])
    min_y = min([coordinate[1] for coordinate in coordinates])
    return [(c[0] - min_x, c[1] - min_y) for c in coordinates]


def _build_matrix(width: int, height: int,
                  content: Point = None) -> List[List[str]]:
    """Builds a matrix of strings with given width and height.

    Args:
        width: Desired width of the matrix.
        height: Desired height of the matrix.
        content: The value to fill the cells of the matrix with.

    Returns:
        A width x height matrix where each cell contains content.
    """
    return [[content for x in range(width)] for y in range(height)]


def _manhattan_distance(point_1: Point, point_2: Point) -> int:
    """Returns the Manhattan dictance between two points.

    Args:
        point_1: The first point.
        point_2: The second point.

    Returns:
        The Manhattan distance between point_1 and point_2.
    """
    return abs(point_1[0] - point_2[0]) + abs(point_1[1] - point_2[1])


def _fill_matrix(matrix: List[List[Point]], coordinates: List[Point]) -> None:
    """Fills a given matrix with the given coordinates' areas of influence.

    Args:
        matrix: The matrix to fill.
        coordinates: A list of points to fill the matrix with.

    Returns:
        Nothing. The matrix is modified in-place.
    """
    for row, _ in enumerate(matrix):
        for col, _ in enumerate(matrix[row]):
            distances = {
                coordinate: _manhattan_distance(coordinate, (col, row))
                for coordinate in coordinates
            }
            min_distance = min(distances.values())
            closest_points = [
                point for point, distance in distances.items()
                if distance == min_distance
            ]
            if len(closest_points) == 1:
                matrix[row][col] = closest_points[0]
            else:
                matrix[row][col] = None


def _get_area_sizes(matrix: List[List[Point]]) -> Dict[Point, int]:
    """Counts the number of cells belonging to each area.

    Args:
        matrix: A 2D matrix of points where areas are defined by different cells
            containing the same value.

    Returns:
        A dictionary with as keys the different cell values in the matrix and as
            values the number of cells containing the corresponding value.
    """
    value_to_count = {}
    for row in matrix:
        for value in row:
            if value not in value_to_count.keys():
                value_to_count[value] = 0
            value_to_count[value] += 1
    return value_to_count


def _get_infinite_area_points(matrix: List[List[Point]]) -> Set[Point]:
    """Finds which points have infinite areas.

    Args:
        matrix: A 2D matrix of points where areas are defined by different cells
            containing the same instance of Point.

    Returns:
        A set of points whose areas touch the side of the matrix.
    """
    infinite_area_points = set()
    for row, _ in enumerate(matrix):
        infinite_area_points.add(matrix[row][0])
        infinite_area_points.add(matrix[row][-1])
    for col, _ in enumerate(matrix[0]):
        infinite_area_points.add(matrix[0][col])
        infinite_area_points.add(matrix[-1][col])
    return infinite_area_points - {None}


def _get_total_distance(point: Point, coordinates: List[Point]) -> int:
    """Computes the sum of the distances from a point to a list of coordinates.

    Args:
        point: The point to measure the distances from.
        coordinates: The coordinates to measure the distances to.

    Returns:
        The sum of the Manhattan distances between point and each coordinate.
    """
    return sum(
        [_manhattan_distance(point, coordinate) for coordinate in coordinates])


def get_largest_finite_area(input_string: str) -> int:
    """Finds the size of the largest finite area.

    Args:
        input_string: The puzzle input.

    Returns:
        An integer representing the size of the largest finite area.
    """
    coordinates = _read_coordinates(input_string)
    coordinates = _normalize_coordinates(coordinates)
    matrix = _build_matrix(
        max([c[0] for c in coordinates]) + 1,
        max([c[1] for c in coordinates]) + 1)
    _fill_matrix(matrix, coordinates)
    area_sizes = _get_area_sizes(matrix)
    infinite_area_points = _get_infinite_area_points(matrix)
    return max([
        area for point, area in area_sizes.items()
        if point not in infinite_area_points
    ])


def get_safe_area(input_string: str, max_distance: int = 10000) -> int:
    """Finds the size of the safe area.

    Args:
        input_string: The puzzle input.

    Returns:
        An integer representing the size of the area containing all locations
            which have a total distance to all coordinates of less than
            max_distance.
    """
    coordinates = _read_coordinates(input_string)
    coordinates = _normalize_coordinates(coordinates)
    matrix = _build_matrix(
        max([c[0] for c in coordinates]) + 1,
        max([c[1] for c in coordinates]) + 1)
    safe_area_size = 0
    for row, _ in enumerate(matrix):
        for col, _ in enumerate(matrix[row]):
            if _get_total_distance((col, row), coordinates) < max_distance:
                safe_area_size += 1
    return safe_area_size


def _run_tests() -> None:
    """Tests solution."""
    assert get_largest_finite_area('1, 1\n1, 6\n8, 3\n3, 4\n5, 5\n8, 9') == 17
    assert get_safe_area('1, 1\n1, 6\n8, 3\n3, 4\n5, 5\n8, 9', 32) == 16


def _print_answers(largest_finite_area: int = None, safe_area: int = None) -> None:
    """Prints answers.

    Args:
        largest_finite_area: The largest finite area.
    """
    print('Answers for day 06:')
    print(f'  Largest finite area: {largest_finite_area}')
    print(f'  Safe area: {safe_area}')


def main() -> None:
    """Runs tests and prints answers to day's puzzle."""
    _run_tests()
    input_string = utils.read_input(6)
    largest_finite_area = get_largest_finite_area(input_string)
    safe_area = get_safe_area(input_string)
    _print_answers(largest_finite_area, safe_area)


if __name__ == '__main__':
    main()

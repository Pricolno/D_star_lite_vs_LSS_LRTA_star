import math
from typing import List


def heuristic_8N(p: (int, int), q: (int, int)) -> float:
    """
    Helper function to compute distance between two points.
    :param p: (x,y)
    :param q: (x,y)
    :return: manhattan distance
    """
    return math.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2)


def heuristic_4N(p: (int, int), q: (int, int)) -> float:
    """
    Helper function to compute distance between two points.
    :param p: (x,y)
    :param q: (x,y)
    :return: manhattan distance
    """
    return abs(p[0] - q[0]) + abs(p[1] - q[1])


def get_movements_4n(y: int, x: int) -> List:
    """
    get all possible 4-connectivity movements.
    :return: list of movements with cost [(dx, dy, movement_cost)]
    """
    return [(y + 1, x + 0),
            (y + 0, x + 1),
            (y - 1, x + 0),
            (y + 0, x - 1)]


def get_movements_8n(x: int, y: int) -> List:
    """
    get all possible 8-connectivity movements.
    :return: list of movements with cost [(dx, dy, movement_cost)]
    """
    return [(y + 1, x + 0),
            (y + 0, x + 1),
            (y - 1, x + 0),
            (y + 0, x - 1),
            (y + 1, x + 1),
            (y - 1, x + 1),
            (y - 1, x - 1),
            (y + 1, x - 1)]


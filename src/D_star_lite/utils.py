import math
from typing import List


class Vertex:
    def __init__(self, pos: (int, int)):
        self.pos = pos
        self.edges_and_costs = {}

    def add_edge_with_cost(self, succ: (int, int), cost: float):
        if succ != self.pos:
            self.edges_and_costs[succ] = cost

    @property
    def edges_and_c_old(self):
        return self.edges_and_costs

    def __str__(self):
        return f"Vertex={self.pos}"

    def __le__(self, other):
        return self.pos <= other.pos

    def __lt__(self, other):
        return self.pos < other.pos


class Vertices:
    def __init__(self):
        self.list = []

    def add_vertex(self, v: Vertex):
        self.list.append(v)

    @property
    def vertices(self):
        return self.list

    def __len__(self):
        return len(self.list)


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


def get_movements_4n(x: int, y: int) -> List:
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

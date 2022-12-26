from heapq import heappop, heappush, heapify

import numpy as np


class Node:
    """
    Node class represents a search node

    - i, j: coordinates of corresponding grid element
    - g: g-value of the node
    - h: h-value of the node
    - f: f-value of the node
    - parent: pointer to the parent-node
    - g_is_true_cost: flag that shows whether the g-value wath precisely computed or just estimated

    You might want to add other fields, methods for Node, depending on how you prefer to implement OPEN/CLOSED further on
    """

    def __init__(self, i, j, g=0, h=0, f=None, parent=None):
        self.i = i
        self.j = j
        self.g = g
        self.h = h
        if f is None:
            self.f = self.g + h
        else:
            self.f = f
        self.parent = parent

    def __eq__(self, other):
        """
        Estimating where the two search nodes are the same,
        which is needed to detect dublicates in the search tree.
        """
        return (self.i == other.i) and (self.j == other.j)

    def __hash__(self):
        """
        To implement CLOSED as set of nodes we need Node to be hashable.
        """
        ij = self.i, self.j
        return hash(ij)

    def __lt__(self, other) -> object:
        """
        Comparison between self and other. Returns is self < other (self has higher priority).
        """
        return self.f < other.f or ((self.f == other.f) and (self.h < other.h))
        # TODO: try different tie-breaks: h-max and h-min

    def __str__(self):
        return f'[({self.i}, {self.j}):g={self.g}, h={self.h}, f={self.f}]'


class SearchTreePQS:  # SearchTree which uses PriorityQueue for OPEN and set for CLOSED
    def __init__(self):
        self._open = []  # heapq for the OPEN nodes
        self._closed = {}  # dict for the expanded nodes = CLOSED
        self._enc_open_dublicates = 0
        self._edges = dict()

    def __len__(self):
        return len(self._open) + len(self._closed)

    def open_is_empty(self):
        return len(self._open) == 0

    def add_to_open(self, item):
        heappush(self._open, item)
        return

    def get_best_node_from_open(self):
        best = None
        while self._open and ((not best) or best in self._closed):
            best = heappop(self._open)
        return best

    def choose_best_h_node_from_open_with(self, cur_node=None):
        if not cur_node:
            cur_node = Node(-1, -1, h=np.inf)
        for node in self._open:
            if node.h < cur_node.h:
                cur_node = node
        return cur_node

    def add_to_closed(self, item):
        self._closed[item] = item

    def was_expanded(self, item):
        return item in self._closed

    @property
    def OPEN(self):
        return self._open

    @property
    def CLOSED(self):
        return self._closed

    @property
    def EDGES(self):
        return self._edges

    @property
    def number_of_open_dublicates(self):
        return self._enc_open_dublicates

    @property
    def expansions(self):
        return len(self._closed)

    @property
    def transitions_computed(self):
        return len(self._edges)


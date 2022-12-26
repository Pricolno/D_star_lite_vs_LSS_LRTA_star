import numpy as np
from sortedcontainers import SortedDict

EPS = 1e-15


class Priority:
    """
    handle lexicographic order of keys
    """

    def __init__(self, k1, k2):
        """
        :param k1: key value
        :param k2: key value
        """
        self.k1 = k1
        self.k2 = k2

    def __str__(self):
        str_priority = f"""Pr(k1={self.k1}, k2={self.k2})"""
        return str_priority

    def __eq__(self, other):
        if not ((self.k1 == np.inf and other.k1 == np.inf) or (abs(self.k1 - other.k1) < EPS)):
            return False

        if not ((self.k2 == np.inf and other.k2 == np.inf) or (abs(self.k2 - other.k2) < EPS)):
            return False

        return True

    def __hash__(self):
        return hash((self.k1, self.k2))

    def __lt__(self, other):
        """
        lexicographic 'lower than'
        :param other: comparable keys
        :return: lexicographic order
        """
        return self.k1 < other.k1 or (self.k1 == other.k1 and self.k2 < other.k2)

    def __le__(self, other):
        """
        lexicographic 'lower than or equal'
        :param other: comparable keys
        :return: lexicographic order
        """
        return self.k1 < other.k1 or (self.k1 == other.k1 and self.k2 <= other.k2)


class PriorityNode:
    """
    handle lexicographic order of vertices
    """

    def __init__(self, priority, pos):
        """
        :param priority: the priority of a
        :param vertex:
        """
        self.priority = priority
        self.pos = pos

    def __eq__(self, other):
        return self.priority == other.priority and self.pos == other.pos

    def __le__(self, other):
        """
        :param other: comparable node
        :return: lexicographic order
        """

        if not (self.priority == other.priority):
            return self.priority < other.priority

        return self.pos <= other.pos

    def __lt__(self, other):
        """
        :param other: comparable node
        :return: lexicographic order
        """
        if not (self.priority == other.priority):
            return self.priority < other.priority

        return self.pos < other.pos

    def __hash__(self):
        return hash((self.priority, self.pos))

    def __repr__(self):
        return f"PriorityNode=[{self.priority}, {self.pos}]"

    def __str__(self):
        return self.__repr__()


class OrderedDictWithRemove:
    def __init__(self):

        self._ordered_dict = SortedDict()
        # for fast finding in ordered_dict by key
        self._map_vertex_to_key = SortedDict()

    def top(self):
        return self._ordered_dict.peekitem(index=0)[1]

    def top_key(self):
        if len(self._ordered_dict) == 0:
            return Priority(float('inf'), float('inf'))
        return self._ordered_dict.peekitem(index=0)[0].priority

    """
    def pop(self):
        key, value = self._ordered_dict.popitem(index=0)
        self._map_vertex_to_key.pop(value)
        return key """

    def insert(self, pos: (int, int), priority):
        # print(f"Insert pos={pos}")
        if pos in self._map_vertex_to_key:
            # print(f"Insert | vertex in self._map_vertex_to_key")
            key_node_del = self._map_vertex_to_key[pos]
            self._ordered_dict.pop(key_node_del)

        key_node = PriorityNode(priority, pos)
        # print(f"Debug {self.}")
        self._map_vertex_to_key[pos] = key_node
        self._ordered_dict[key_node] = pos

    def remove(self, pos: (int, int)):
        # print(f"Remove pos={pos}")
        # like pop
        if pos in self._map_vertex_to_key:
            key_node = self._map_vertex_to_key.pop(pos)
            # print(key_node.__dict__)
            # print(key_node.priority)
            # print(f"{key_node in self._ordered_dict} | key_node={key_node} | \n _ordered_dict={self._ordered_dict} ")

            # print(f"self._ordered_dict[{key_node}]={self._ordered_dict[key_node]}")
            # del self._ordered_dict[key_node]
            # self._ordered_dict.__delitem__(key_node)

            # print(self._ordered_dict)
            del self._ordered_dict[key_node]

            # self._ordered_dict.pop(key_node)

    def update(self, pos: (int, int), priority):
        # print(pos)
        self.remove(pos)
        self.insert(pos, priority)

    def __str__(self):
        str_res = f"{str(self._ordered_dict)}"
        return str_res

    def __contains__(self, pos):
        return pos in self._map_vertex_to_key

    def __len__(self):
        return self._ordered_dict.__len__()

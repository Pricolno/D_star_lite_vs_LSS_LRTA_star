import copy
import numpy as np
import pandas as pd

from search import Node
from src.LSS_LRTA_star.grid_map import Map
from src.data.run_tests import SampleTest
from src.statistics_tools.statistics_methods import Statistic


def manhattan_distance(i1, j1, i2, j2):
    return abs(i1 - i2) + abs(j1 - j2)


def compute_cost(i1, j1, i2, j2):
    """
    Computes cost of simple moves between cells
    """
    d = abs(i1 - i2) + abs(j1 - j2)
    if d == 1:  # cardinal move
        return 1
    else:
        raise Exception('Trying to compute the cost of non-supported move!')


def make_path(goal):
    """
    Creates a path by tracing parent pointers from the goal node to the start node
    It also returns path's length.
    """
    length = goal.g
    current = goal
    path = []
    while current.parent:
        path.append(current)
        current = current.parent
    path.append(current)
    return path[::-1], length


def astar(grid_map_ptr, start_i, start_j, goal_i, goal_j, heuristic_func=None, search_tree=None, lookahead=0):
    grid_map = grid_map_ptr[0]
    if not lookahead:
        lookahead = np.inf

    ast = search_tree()
    steps = 0
    last_node = None
    path_flag = False

    start = Node(start_i, start_j, g=0, h=heuristic_func(start_i, start_j, goal_i, goal_j))
    ast.add_to_open(start)

    while ast.OPEN:
        steps += 1
        cur = ast.get_best_node_from_open()
        if not cur:
            break

        if (cur.i, cur.j) == (goal_i, goal_j) or ast.expansions >= lookahead:
            last_node = cur
            path_flag = True
            ast.add_to_open(cur)
            break

        ast.add_to_closed(cur)

        for i, j in grid_map.get_neighbors(cur.i, cur.j):
            if (i, j) in grid_map._upgraded_h:
                h_value = grid_map._upgraded_h[(i, j)]
            else:
                h_value = heuristic_func(i, j, goal_i, goal_j)
            new_node = Node(i, j,
                            g=cur.g + compute_cost(cur.i, cur.j, i, j),
                            h=h_value,
                            parent=cur)
            if not ast.was_expanded(new_node):
                ast.EDGES[(cur.i, cur.j, i, j)] = True
                ast.add_to_open(new_node)

    return path_flag, last_node, ast


def dijkstra(grid_map_ptr, dijkstra_start, a_closed, search_tree=None):
    grid_map = grid_map_ptr[0]
    dst = search_tree()  # Dijkstra's search tree
    start = Node(dijkstra_start.i, dijkstra_start.j, g=dijkstra_start.h)
    dst.add_to_open(start)
    steps = 0
    while a_closed and dst.OPEN:
        steps += 1
        cur = dst.get_best_node_from_open()
        if not cur:
            break
        if cur in a_closed:
            del a_closed[cur]
        dst.add_to_closed(cur)

        for i, j in grid_map.get_neighbors(cur.i, cur.j):
            new_node = Node(i, j, g=cur.g + compute_cost(cur.i, cur.j, i, j))
            if not dst.was_expanded(new_node) and new_node in a_closed:
                # new_node.parent = cur
                dst.add_to_open(new_node)

    for node in dst.CLOSED:
        grid_map._upgraded_h[(node.i, node.j)] = node.g
    return


def lss_lrta_star(grid_map_ptr, start_i, start_j, goal_i, goal_j, heuristic_func=None, search_tree=None,
                  lookahead=0):
    results = []
    init_obst = grid_map_ptr[0].set_local_observations(start_i, start_j)

    while (start_i, start_j) != (goal_i, goal_j):
        path_flag, last_node, search_tree_log = astar(
            grid_map_ptr,
            start_i, start_j,
            goal_i, goal_j,
            heuristic_func,
            search_tree,
            lookahead
        )
        # set viewed obstacles and find real last node
        viewed_obstacles = []
        real_last_node = last_node
        if not results:
            viewed_obstacles += init_obst
        path, _ = make_path(last_node)
        for node in path:
            if grid_map_ptr[0].traversable(node.i, node.j):
                real_last_node = node
                viewed_obstacles += grid_map_ptr[0].set_local_observations(node.i, node.j)
            else:
                break
        start_i, start_j = real_last_node.i, real_last_node.j
        # get statistic
        stat_values = (search_tree_log.expansions,
                       len(search_tree_log))
        stat_objects = (search_tree_log.OPEN,
                        search_tree_log.CLOSED,
                        search_tree_log.EDGES,
                        viewed_obstacles)
        # dijkstra procedure
        a_closed = copy.copy(search_tree_log.CLOSED)
        if search_tree_log.open_is_empty():
            return results
        dijkstra_start = search_tree_log.choose_best_h_node_from_open_with(cur_node=last_node)
        dijkstra(grid_map_ptr, dijkstra_start, a_closed, search_tree)
        '''
        print('h-hash_map: ', grid_map_ptr[0]._upgraded_h)
        print('last_node: ', last_node)
        print('dijkstra: ', dijkstra_start)
        print('open: ', *search_tree_log.OPEN)
        print('closed: ', *search_tree_log.CLOSED)
        '''
        # add new results
        results.append((path_flag, (real_last_node, last_node), dijkstra_start, stat_values, stat_objects))

    return results





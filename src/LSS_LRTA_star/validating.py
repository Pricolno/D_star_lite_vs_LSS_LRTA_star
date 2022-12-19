from random import randint

import numpy as np
import pandas as pd

from src.LSS_LRTA_star.drawing import draw_dynamic
from src.LSS_LRTA_star.grid_map import Map
from src.LSS_LRTA_star.search import Node
from src.LSS_LRTA_star.lss_lrta import lss_lrta_star, make_path
from src.data.run_tests import SampleTest
from src.statistics_tools.statistics_methods import Statistic


def simple_test(search_func, task, *args):
    height = 15
    width = 30
    map_str = '''
. . . # # . . . . . . . . # # . . . # . . # # . . . . . . .  
. . . # # # # # . . # . . # # . . . . . . # # . . . . . . . 
. . . . . . . # . . # . . # # . . . # . . # # . . . . . . . 
. . . # # . . # . . # . . # # . . . # . . # # . . . . . . . 
. . . # # . . # . . # . . # # . . . # . . # # . . . . . . . 
. . . # # . . # . . # . . # # . . . # . . # # # # # . . . . 
. . . # # . . # . . # . . # # . . . # . . # # # # # . . . . 
. . . . . . . # . . # . . # # . . . # . . # . . . . . . . . 
. . . # # . . # . . # . . # # . . . # . . # . . . . . . . . 
. . . # # . . # . . # . . # # . . . # . . # . . . . . . . . 
. . . # # . . . . . # . . . . . . . # . . . . . . . . . . . 
. . . # # # # # # # # # # # # # . # # . # # # # # # # . # # 
. . . # # . . . . . . . . # # . . . . . . . . . . . . . . . 
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
. . . # # . . . . . . . . # # . . . . . . . . . . . . . . .
'''

    task_map = Map(2)
    task_map.read_from_string(map_str, width, height)

    starts = [(1, 28), (2, 29), (3, 20), (3, 20), (0, 0)]
    goals = [(0, 1), (6, 2), (5, 6), (13, 0), (4, 23)]

    # lengths = [54, 47, 48, 38, 56]

    if (task is None) or not (0 <= task < 5):
        task = randint(0, 4)

    start = Node(*starts[task])
    goal = Node(*goals[task])
    # length = lengths[task]
    try:
        results = search_func([task_map], start.i, start.j, goal.i, goal.j, *args)
        draw_dynamic(task_map, start, goal, results)
        return results

    except Exception as e:
        print("Execution error")
        print(e)


def hard_test(search_func, task, *args):
    height = 15
    width = 30
    map_str = '''
. . . # # . . . . . . . . # # . . . # . . # # . . . . . . .  
. . . # # # # # . . # . . # # . . . . . . # # . . . . . . . 
. . . # . . . # . . # . . # # . . . # . . # # . . . . . . . 
. . . # # . . # . . # . . # # . . . # . . # # . . . . . . . 
. . . # # . . # . . # . . # # . . . # . . # # . . . . . . . 
. . . # # . . # . . # . . # # . . . # . . # # # # # . . . . 
. . . # # . . # . . # . . # # . . . # . . # # # # # . . . . 
. . . # . . . # . . # . . # # . . . # . . # . . . . . . . . 
. . . # # . . # . . # . . # # . . . # . . # . . . . . . . . 
. . . # # . . # . . # . . # # . . . # . . # . . . . . . . . 
. . . # # . . . . . # . . . . . . . # . . . . . . . . . . . 
. . . # # # # # # # # # # # # # . # # . # # # # # # # . # # 
. . . # # . . . . . . . . # # . . . . . . . . . . . . . . . 
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
. . . # # . . . . . . . . # # . . . . . . . . . . . . . . .
'''

    task_map = Map(view_range=1)
    task_map.read_from_string(map_str, width, height)

    starts = [(1, 28), (2, 29), (3, 20), (3, 20), (0, 0)]
    goals = [(0, 1), (6, 2), (5, 6), (13, 0), (4, 23)]

    lengths = [54, 47, 48, 38, 56]

    if (task is None) or not (0 <= task < 5):
        task = randint(0, 4)

    start = Node(*starts[task])
    goal = Node(*goals[task])
    length = lengths[task]
    try:
        results = search_func([task_map], start.i, start.j, goal.i, goal.j, *args)
        draw_dynamic(task_map, start, goal, results)
        return results

    except Exception as e:
        print("Execution error")
        print(e)


def toy_test(search_func, task, *args):
    # map_str = ...
    height = 167
    width = 247
    starts = [(24, 10)]
    # goals = [(105, 11)]
    goals = [(102, 100)]  # 178 #100
    task_map = Map(3)
    task_map.read_from_file('den011d.map', width, height)
    start = Node(*starts[task])
    goal = Node(*goals[task])
    try:
        results = search_func([task_map], start.i, start.j, goal.i, goal.j, *args)
        draw_dynamic(task_map, start, goal, results)
        return results
    except Exception as e:
        print("Execution error (draw?)")
        print(e)


def base_test(search_func, task, *args):
    height = 3
    width = 6
    map_strs = ['''
. . . . # .
. # # # # .
. . . . . .
''',
                '''
. . # # # .
. . . . # .
# # # . . .
'''
                ]
    starts = [(0, 2), (0, 0)]
    goals = [(0, 5), (0, 5)]
    map_str = map_strs[task]

    task_map = Map(0)
    task_map.read_from_string(map_str, width, height)

    if (task is None) or not (0 <= task < 2):
        task = randint(0, 2)

    start = Node(*starts[task])
    goal = Node(*goals[task])
    try:
        results = search_func([task_map], start.i, start.j, goal.i, goal.j, *args)
        draw_dynamic(task_map, start, goal, results)
        return results

    except Exception as e:
        print("Execution error")
        print(e)


def super_test(search_func, sample_test, *args):
    start = sample_test.start
    goal = sample_test.goal
    task_map = Map(3)
    task_map.read_from_cells(sample_test.cells)
    start = Node(*start)
    goal = Node(*goal)
    try:
        results = search_func([task_map], start.i, start.j, goal.i, goal.j, *args)
        draw_dynamic(task_map, start, goal, results)
        return results
    except Exception as e:
        print("Execution error (draw?)")
        print(e)


class TestLSSLRTAstar:
    def __init__(self, heuristic_func, search_tree, lookahead=None, view_range=None):
        self.heuristic_func = heuristic_func
        self.search_tree = search_tree
        self.lookahead = lookahead
        self.view_range = view_range

    def get_procedure(self, in_frame=True):
        def test_lss_lrta_star(sample_test: SampleTest) -> pd.DataFrame:
            start = sample_test.start
            goal = sample_test.goal
            task_map = Map(view_range=self.view_range)
            task_map.read_from_cells(sample_test.cells)
            start = Node(*start)
            goal = Node(*goal)
            results = []
            try:
                results = lss_lrta_star([task_map], start.i, start.j, goal.i, goal.j,
                                        self.heuristic_func, self.search_tree, self.lookahead)
            except Exception as e:
                print("Run test error for LSS-LRTA*")
                print(e)

            result_frame = pd.DataFrame(np.array(
                [[*last_node_tuple, *stat_values]
                 for path_flag, last_node_tuple, start_dijkstra, stat_values, stat_objects in results]),
                columns=['Actual goal', 'Dummy goal', 'Expansions', 'Created'])

            searches, _ = result_frame.shape
            assert result_frame['Actual goal'][searches - 1] == goal

            result_frame['Actual pathlen'] = result_frame['Actual goal'].apply(
                lambda node: make_path(node)[1])

            return result_frame

        def get_statistic(sample_test: SampleTest) -> Statistic:
            result_frame = test_lss_lrta_star(sample_test)
            return Statistic(Cell_expansions=result_frame['Expansions'].sum(),
                             Searchesc=result_frame.shape[0],
                             Trajectory_length=result_frame['Actual pathlen'].sum(),
                             Trajectory_length_per_search=result_frame['Actual pathlen'].mean())

        if in_frame:
            return test_lss_lrta_star
        else:
            return get_statistic

    def get_vectorized_procedure(self):
        test_lss_lrta_star = self.get_procedure()

        def multiple_test_lss_lrta_star(sample_tests: [SampleTest]):
            searches = 0
            cell_expansions = 0
            trajectory_length = 0
            trajectory_length_per_search = 0
            for sample_test in sample_tests:
                result_frame = test_lss_lrta_star(sample_test)
                searches += result_frame.shape[0]
                cell_expansions += result_frame['Expansions'].sum()
                trajectory_length += result_frame['Actual pathlen'].sum()
                # trajectory_length_per_search += result_frame['Actual pathlen'].mean()
            size = len(sample_tests)
            return Statistic(Cell_expansions=cell_expansions / size,
                             Searchesc=searches / size,
                             Trajectory_length=trajectory_length / size,
                             #Trajectory_length_per_search=trajectory_length_per_search / size)
                             Trajectory_length_per_search=trajectory_length / searches)
        return multiple_test_lss_lrta_star

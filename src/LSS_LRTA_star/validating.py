from random import randint
from drawing import draw_dynamic
from grid_map import Map
from search import Node


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

    #lengths = [54, 47, 48, 38, 56]

    if (task is None) or not (0 <= task < 5):
        task = randint(0, 4)

    start = Node(*starts[task])
    goal = Node(*goals[task])
    #length = lengths[task]
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
    #goals = [(105, 11)]
    goals = [(102, 100)] #178 #100
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
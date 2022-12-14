import numpy as np
from IPython.display import HTML

from random import randint
from PIL import Image, ImageDraw, ImageOps
from IPython.display import Image as Img
from IPython.display import display
from matplotlib import pyplot as plt, animation

from lss_lrta import make_path
from search import Node


def draw_dynamic(grid_map, start, goal, search_logs, output_filename='animated_trajectories'):
    """
    Auxiliary function that visualizes the environment.

    The function assumes that nodes_opened/nodes_expanded
    are iterable collestions of search nodes
    """

    k = 30  # k = 30, 5
    quality = 6
    height, width = grid_map.get_size()
    h_im = height * k
    w_im = width * k

    images = []
    agent_color = randint(0, 255), randint(0, 255), randint(0, 255)
    nodes_expanded_prev = []
    viewed_obstacles_prev = []
    abs_length, abs_nodes_created, abs_expansions, abs_transitions_computed = 0, 0, 0, 0
    real_last_node = None

    for path_flag, last_node_tuple, start_dijkstra, stat_values, stat_objects in search_logs:
        real_last_node, last_node = last_node_tuple
        expansions, transitions_computed, nodes_created = stat_values
        nodes_opened, nodes_expanded, edges_evaluated, new_viewed_obstacles = stat_objects

        # viewed_obstacles += new_viewed_obstacles
        if path_flag:
            path_ = make_path(last_node)
            real_path_ = make_path(real_last_node)
            abs_length += real_path_[1]
            abs_nodes_created += nodes_created
            abs_expansions += expansions
            abs_transitions_computed += transitions_computed
            message = 'Success'
            if last_node != real_last_node:
                message = 'Obstacle'
            print(
                f"{message}! Length: {round(real_path_[1], 3)}."
                f" Nodes created: {nodes_created}."
                f" Number of expansions: {expansions}."
                f" Transitions computed: {transitions_computed}.")
        else:
            print("Path not found!")
            return

        path = path_[0]
        pathlen = len(path)
        real_path = real_path_[0]
        real_pathlen = len(real_path)

        step_number = 0
        while step_number < real_pathlen:
            for n in range(0, quality):
                im = Image.new('RGB', (w_im, h_im), color='white')
                draw = ImageDraw.Draw(im)

                # draw upgraded h_values
                for (i, j) in grid_map._upgraded_h:
                    h = grid_map._upgraded_h[(i, j)]
                    if Node(i, j) in nodes_expanded_prev:
                        draw.rectangle((j * k, i * k, (j + 1) * k - 1, (i + 1) * k - 1),
                                       fill=(255, 255, (-int(256 * (h / (height + width)))) % 256), width=0)
                # draw opened nodes
                if nodes_opened is not None:
                    for node in nodes_opened:
                        draw.rectangle((node.j * k, node.i * k, (node.j + 1) * k - 1, (node.i + 1) * k - 1),
                                       fill=(213, 219, 219), width=0)
                # draw expanded nodes
                if nodes_expanded is not None:
                    for node in nodes_expanded:
                        draw.rectangle((node.j * k, node.i * k, (node.j + 1) * k - 1, (node.i + 1) * k - 1),
                                       fill=(131, 145, 146), width=0)
                # draw static obstacles
                for i in range(height):
                    for j in range(width):
                        if not grid_map.traversable(i, j, by_origin=True):
                            draw.rectangle((j * k, i * k, (j + 1) * k - 1, (i + 1) * k - 1), fill=(70, 80, 80))
                            # (70, 80, 80)
                # draw path
                if path is not None:
                    for step in path:
                        if step is not None:
                            if grid_map.traversable(step.i, step.j):
                                draw.rectangle((step.j * k, step.i * k, (step.j + 1) * k - 1, (step.i + 1) * k - 1),
                                               fill=(52, 152, 219), width=0)
                            else:
                                draw.rectangle((step.j * k, step.i * k, (step.j + 1) * k - 1, (step.i + 1) * k - 1),
                                               fill=(230, 126, 34), width=0)
                    # color boundaries of path
                    step = path[-1]
                    if step and (step != goal):
                        draw.rectangle((step.j * k, step.i * k, (step.j + 1) * k - 1, (step.i + 1) * k - 1),
                                       fill=(255, 20, 147), width=0)
                    step = path[0]
                    if step and (step != start):
                        draw.rectangle((step.j * k, step.i * k, (step.j + 1) * k - 1, (step.i + 1) * k - 1),
                                       fill=(107, 142, 35), width=0)
                # draw start
                if (start is not None) and (grid_map.traversable(start.i, start.j)):
                    draw.rectangle((start.j * k, start.i * k, (start.j + 1) * k - 1, (start.i + 1) * k - 1),
                                   fill=(40, 180, 99), width=0)
                # draw goal
                if (goal is not None) and (grid_map.traversable(goal.i, goal.j)):
                    draw.rectangle((goal.j * k, goal.i * k, (goal.j + 1) * k - 1, (goal.i + 1) * k - 1),
                                   fill=(231, 76, 60), width=0)
                '''
                # draw dijkstra start
                if (start_dijkstra is not None) and (grid_map.traversable(start_dijkstra.i, start_dijkstra.j)) and (start_dijkstra != goal):
                    draw.rectangle((start_dijkstra.j * k, start_dijkstra.i * k, (start_dijkstra.j + 1) * k - 1,
                                    (start_dijkstra.i + 1) * k - 1), fill=(139, 69, 19), width=0)
                '''
                '''
                # draw evaluated edges
                if edges_evaluated is not None:
                    for edge in edges_evaluated.keys():
                        draw.line(((edge[1] + 0.5) * k, (edge[0] + 0.5) * k, (edge[3] + 0.5) * k, (edge[2] + 0.5) * k),
                                  fill=((0, 0, 0) if edges_evaluated[edge] else (200, 200, 200)), width=2)
                '''
                # draw agent
                curr_node = real_path[step_number]
                next_node = real_path[min(real_pathlen - 1, step_number + min(n, 1))]
                di = n * (next_node.i - curr_node.i) / quality
                dj = n * (next_node.j - curr_node.j) / quality
                draw.ellipse((float(curr_node.j + dj + 0.2) * k,
                              float(curr_node.i + di + 0.2) * k,
                              float(curr_node.j + dj + 0.8) * k - 1,
                              float(curr_node.i + di + 0.8) * k - 1),
                             fill=agent_color, width=0)
                # draw viewed obstacles
                if grid_map._view_range:
                    for i, j in viewed_obstacles_prev:
                        draw.rectangle((j * k, i * k, (j + 1) * k - 1, (i + 1) * k - 1), fill=(0, 0, 0))

                im = ImageOps.expand(im, border=2, fill='black')
                images.append(im)

            step_number += 1
        nodes_expanded_prev += nodes_expanded.keys()
        viewed_obstacles_prev += new_viewed_obstacles
    print('-----------------Absolute---------------------')
    if real_last_node == goal:
        print(
            f"Path found! Length: {abs_length}."
            f" Nodes created: {abs_nodes_created}. "
            f"Number of expansions: {abs_expansions}. "
            f"Transitions computed: {abs_transitions_computed}.")
    else:
        print("Path not found!")

    #images[0].save('./' + output_filename + '.png', save_all=True, append_images=images[1:], optimize=False,
    #               duration=300 / quality, loop=0)
    #display(Img(filename='./' + output_filename + '.png'))
    images[0].save('./' + output_filename + '.gif', save_all=True, append_images=images[1:], optimize=True,
                   duration=600 / quality, loop=0)
    # 120







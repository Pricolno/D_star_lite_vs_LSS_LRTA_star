import random

from config import N, M, COUNT_OF_SCENE, PATH_TO_SCENE
from src.Dijkstra.run_dijkstra import RunDijkstra
from src.data.scene import Scene


# def check

def generate_random_pos(map01):
    n = len(map01)
    m = len(map01[0])
    return random.randint(0, n - 1), random.randint(0, m - 1)


def is_obstacle(pos, map):
    return map[pos[0]][pos[1]] == 1


def is_exist_path(s_start, s_goal, map):
    run_dj = RunDijkstra()

    run_dj.load_map_cells(map)
    run_dj.load_map_start_goal(s_start, s_goal)

    length = run_dj.run_dijkstra()

    # return length is not None
    return length


def create_list_random_scene(map01):
    list_scenes = []
    count_ready_scenes = 0
    while count_ready_scenes < COUNT_OF_SCENE:

        s_start = generate_random_pos(map01)
        s_goal = generate_random_pos(map01)

        print(f"created scene: {s_start}, {s_goal} | ", end="")
        if is_obstacle(s_start, map01) or is_obstacle(s_goal, map01):
            print("Fail, is_obstacle")
            continue

        optimal_length = is_exist_path(s_start, s_goal, map01)
        if optimal_length is None:
            print("Fail, not found path")
            continue

        scene_now = Scene(hard_lvl=-1,
                          height=len(map01),
                          width=len(map01[0]),
                          start_i=s_start[0],
                          start_j=s_start[1],
                          goal_i=s_goal[0],
                          goal_j=s_goal[1],
                          optimal_length=optimal_length)
        list_scenes.append(scene_now)
        print("Succesefull, path is found")
        count_ready_scenes += 1
    return list_scenes


def save_scenes_for_all_maps(list_random_maps, list_names_of_maps):
    for map, name_of_maps in zip(list_random_maps, list_names_of_maps):
        list_scenes = create_list_random_scene(map01=map)

        save_list_of_scenes_to_movingAi(list_scenes=list_scenes,
                                        name_file_scenes=name_of_maps)




def save_list_of_scenes_to_movingAi(list_scenes, name_file_scenes):
    str_version = "version__0\n"
    list_str_scenes = []
    for num_scenes, scene in enumerate(list_scenes):
        str_scene = scene.str_movingAi()
        str_scene += "\n"
        list_str_scenes.append(str_scene)

    str_res = ''.join([str_version, *list_str_scenes])

    full_path_to_file = PATH_TO_SCENE + '/' + name_file_scenes + '.scene'


    with open(full_path_to_file, "a") as file_scenes:
        file_scenes.write(str_res)

    return full_path_to_file


if __name__ == "__main__":
    map01 = [[0, 1],
             [0, 0]]

    list_scenes = create_list_random_scene(map01)
    save_list_of_scenes_to_movingAi(list_scenes, name_file_scenes="random0")
    #print(list_scenes[1])

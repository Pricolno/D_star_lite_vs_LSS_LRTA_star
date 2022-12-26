import random
import pickle
from pprint import pprint
import os

from config import N, M, COUNT_OF_MAPS, PATH_TO_MAP, NAME_FILE

#N, M = 512, 512
#COUNT_OF_MAPS = 1
#PATH_TO_FILE = "../our_data/random_obstacles.map"
#NAME_FILE = "random_map"


def create_list_random_maps():
    list_random_maps = []
    for num_test in range(COUNT_OF_MAPS):
        random_map = [
            [1 if random.randint(0, 3) == 0 else 0
             for j in range(M)]
            for i in range(N)
        ]

        list_random_maps.append(random_map)
    return list_random_maps


def save_list_random_maps_by_pickle(list_random_maps):
    path_to_maps = f"{PATH_TO_MAP}"
    list_names_maps = os.listdir(path_to_maps)
    offset = len(list_names_maps)

    for num_test, random_map in enumerate(list_random_maps):
        name_file = NAME_FILE + f"_{str(num_test + offset)}"
        full_path_to_file = PATH_TO_MAP + '/' + name_file + '.pickle'
        pickle.dump(random_map, file=open(full_path_to_file, "wb"))


def map01_to_movingAi(map01):
    str_type = "type ___\n"
    str_height = f"height {N}\n"
    str_weight = f"weight {M}\n"
    str_name_map = f"__random_map__\n"

    str_map = ""
    for i in range(N):
        for j in range(M):
            if map01[i][j] == 0:
                str_map += "."
            else:
                str_map += "@"
        str_map += "\n"

    str_res = ''.join([str_type, str_height, str_weight, str_name_map, str_map])
    return str_res


def save_list_random_maps_by_movingAi(list_random_maps):
    path_to_maps = f"{PATH_TO_MAP}"
    list_names_maps = os.listdir(path_to_maps)
    offset = len(list_names_maps)

    list_names_of_maps = []
    for num_test, random_map in enumerate(list_random_maps):
        name_file = NAME_FILE + f"_{str(num_test + offset)}"
        full_path_to_file = PATH_TO_MAP + '/' + name_file + '.map'
        list_names_of_maps.append(name_file)
        str_map = map01_to_movingAi(random_map)

        with open(full_path_to_file, "a") as file_map:
            file_map.write(str_map)
    return list_names_of_maps

if __name__ == "__main__":
    list_random_maps = create_list_random_maps()

    save_list_random_maps_by_movingAi(list_random_maps)










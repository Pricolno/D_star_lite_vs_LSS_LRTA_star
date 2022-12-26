import generate_random_map as grm
import generator_scene as gs
import config
import os


def generate_maps(verbose=False):
    list_random_maps = grm.create_list_random_maps()
    if verbose:
        print(f"Создано {len(list_random_maps)} карт")
    list_names_of_maps = grm.save_list_random_maps_by_movingAi(list_random_maps)
    if verbose:
        print(f"Сохранено {len(list_random_maps)} карт в path={config.PATH_TO_MAP}")
    return list_random_maps, list_names_of_maps


def generate_scenes(list_random_maps=None, list_names_of_maps=None, verbose=False):
    gs.save_scenes_for_all_maps(list_random_maps=list_random_maps,
                                list_names_of_maps=list_names_of_maps)

    if verbose:
        print(f"Scenes loaded in {list_names_of_maps[0]}. Count equal {len(list_random_maps)}")


def generate_data(verbose=False):
    list_random_maps, list_names_of_maps = generate_maps(verbose=verbose)
    generate_scenes(list_random_maps,
                    list_names_of_maps,
                    verbose=verbose)
    return


def clear_random_maps():
    path_to_maps = f"{config.PATH_TO_MAP}"
    list_names_maps = os.listdir(path_to_maps)
    # print(list_names_maps)
    for name_map in list_names_maps:
        full_path_to_maps = f"{config.PATH_TO_MAP}/{name_map}"
        os.remove(f"{full_path_to_maps}")


def clear_random_scenes():
    path_to_maps = f"{config.PATH_TO_SCENE}"
    list_names_scenes = os.listdir(path_to_maps)
    # print(list_names_scenes)
    for name_map in list_names_scenes:
        full_path_to_scenes = f"{config.PATH_TO_SCENE}/{name_map}"
        os.remove(f"{full_path_to_scenes}")


def clear_all():
    clear_random_maps()
    clear_random_scenes()


if __name__ == "__main__":
    generate_data(verbose=True)

    # clear_all()

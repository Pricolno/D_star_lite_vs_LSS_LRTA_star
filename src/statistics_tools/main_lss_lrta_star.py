from pprint import pprint

from src.LSS_LRTA_star.lss_lrta import manhattan_distance
from src.LSS_LRTA_star.search import SearchTreePQS

from src.statistics_tools.quick_test_run import QuickTestRun

# FILE
LIST_PATH_TO_FILE_MAPS = ["../data/movingai_data/maze-map/maze512-1-0.map",
                          "../data/our_data/random_obstacles.map/random_obstacles_0.map",
                          "../data/movingai_data/den011d.map/den011d.map",
                          "../data/movingai_data/street-map/Berlin_0_256.map"
                          ]

LIST_PATH_TO_FILE_SCENES = ["../data/movingai_data/maze-scen/maze512-1-0.map.scen",
                            "../data/our_data/random_obstacles.map-scen/random_obstacles_0.scen",
                            "../data/movingai_data/den011d.map-scen/den011d.map.scen",
                            "../data/movingai_data/street-scen/Berlin_0_256.map.scen"
                            ]
# DIR
LIST_PATH_TO_DIR_MAPS = ["../data/movingai_data/maze-map",
                         "../data/our_data/random_obstacles.map",
                         "../data/movingai_data/den011d.map",
                         "../data/movingai_data/street-map"
                         ]

LIST_PATH_TO_DIR_SCENES = ["../data/movingai_data/maze-scen",
                           "../data/our_data/random_obstacles.map-scen",
                           "../data/movingai_data/den011d.map-scen",
                           "../data/movingai_data/street-scen"
                           ]


def launch_number1():
    Quick_Test_Run = QuickTestRun()
    Quick_Test_Run.load_lss_lrta_star(
        heuristic_func=manhattan_distance,
        search_tree=SearchTreePQS,
        lookahead=0,
        view_range=10)
    path_to_dir_maps = LIST_PATH_TO_DIR_MAPS[1]
    path_to_dir_scenes = LIST_PATH_TO_DIR_SCENES[1]

    factor_stats = Quick_Test_Run.run_all_test_for_all_maps(path_to_dir_maps=path_to_dir_maps,
                                                            path_to_dir_scenes=path_to_dir_scenes)

    factor_stats.save_stats(name_file=f'LSS_LRTA_star_launch_number1_', verbose=True)

    return factor_stats

def launch_number_old():
    Quick_Test_Run = QuickTestRun()

    Quick_Test_Run.run_all_test_for_all_maps()

    Quick_Test_Run.read_data_from_files(
        path_to_file_map=LIST_PATH_TO_FILE_MAPS[1],
        path_to_file_scenes=LIST_PATH_TO_FILE_SCENES[1])

    Quick_Test_Run.load_lss_lrta_star(
        heuristic_func=manhattan_distance,
        search_tree=SearchTreePQS,
        lookahead=0,
        view_range=10)

    Quick_Test_Run.select_tests_random(count_of_tests=2,
                                       prob_l=0.5, prob_r=0.6,
                                       seed=1332)
    factor_stats = Quick_Test_Run.run_all_test()
    pprint(factor_stats.get_stats())

    factor_stats.save_stats(name_file='LSS_LRTA_star_random', verbose=True)
    # factor_stats = FactoryStatistics.load_stats(name_file="LSS_LRTA_star_random", verbose=True)
    # pprint(factor_stats.get_DataFrame())

    return factor_stats


if __name__ == '__main__':
    print("START MAIN LSS_LRTA_STAR")
    factor_stats = launch_number1()
    pprint(factor_stats.get_stats())
    exit()


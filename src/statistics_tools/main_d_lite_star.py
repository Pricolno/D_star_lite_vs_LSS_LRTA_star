from pprint import pprint

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


def launch_test_Dlite(name_saved_file=None, view_range=1, max_count_map=250 // 5):
    name_saved_file = f'random_obstacles/D_Lite_star_random_obstacles_view_range_{view_range}_max_count_{max_count_map}'
    path_to_dir_maps = LIST_PATH_TO_DIR_MAPS[1]
    path_to_dir_scenes = LIST_PATH_TO_DIR_SCENES[1]

    #max_count_map = 3

    Quick_Test_Run = QuickTestRun()

    factor_stats = Quick_Test_Run.run_Dlite_all_test_for_all_maps(path_to_dir_maps=path_to_dir_maps,
                                                                  path_to_dir_scenes=path_to_dir_scenes,
                                                                  max_count_map=max_count_map,
                                                                  restart=True,
                                                                  name_saved_file=name_saved_file)
    # pprint(factor_stats.get_stats())
    return factor_stats


def launch_old_Dlite():
    Quick_Test_Run = QuickTestRun()

    Quick_Test_Run.read_data_from_files(path_to_file_map=LIST_PATH_TO_FILE_MAPS[0],
                                        path_to_file_scenes=LIST_PATH_TO_FILE_SCENES[0])

    Quick_Test_Run.load_d_star_lite(gui=False,
                                    view_range=10)
    Quick_Test_Run.select_tests_random(count_of_tests=10,
                                       prob_l=0.1, prob_r=0.2,
                                       seed=1332)
    factor_stats = Quick_Test_Run.run_all_test()

    pprint(factor_stats.get_stats())


if __name__ == "__main__":
    launch_test_Dlite()

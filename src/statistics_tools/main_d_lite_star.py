from pprint import pprint

from src.statistics_tools.quick_test_run import QuickTestRun

LIST_PATH_TO_FILE_MAP = ["maze-map/maze512-1-0.map",
                         "random512-10-0.map/random512-10-0.map",
                         "den011d.map/den011d.map",
                         "street-map/Berlin_0_256.map"]

LIST_PATH_TO_FILE_SCENES = ["maze-scen/maze512-1-0.map.scen",
                            "random512-10-0.map-scen/random512-10-0.map.scen",
                            "den011d.map-scen/den011d.map.scen",
                            "street-scen/Berlin_0_256.map.scen"
                            ]


if __name__ == "__main__":
    print("START")

    Quick_Test_Run = QuickTestRun()

    Quick_Test_Run.read_data_from_files(path_to_file_map=LIST_PATH_TO_FILE_MAP[0],
                                        path_to_file_scenes=LIST_PATH_TO_FILE_SCENES[0])

    Quick_Test_Run.load_d_star_lite(gui=False,
                                    view_range=10)
    Quick_Test_Run.select_tests_random(count_of_tests=10,
                                       prob_l=0.1, prob_r=0.2,
                                       seed=1332)
    factor_stats = Quick_Test_Run.run_all_test()

    pprint(factor_stats.get_stats())

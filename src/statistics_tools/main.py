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

    Quick_Test_Run.read_data_from_files(path_to_file_map=LIST_PATH_TO_FILE_MAP[1],
                                        path_to_file_scenes=LIST_PATH_TO_FILE_SCENES[1])

    Quick_Test_Run.load_d_star_lite()
    Quick_Test_Run.select_tests_random(count_of_tests=2,
                                       prob_l=0.6, prob_r=0.9)
    factor_stats = Quick_Test_Run.run_all_test()

    pprint(factor_stats.get_stats())
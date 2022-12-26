import pprint

# reading maps and scenes
from src.data.read_maps_info import ReadMapsInfo

# struct for general test
from src.data.run_tests import SampleTest, RunTests

# Dlite
from src.D_start_lite.run_d_star_lite import RunDStarLite
from src.D_start_lite.utils import heuristic_4N, heuristic_8N


LIST_PATH_TO_FILE_MAP = ["../data/movingai_data/maze-map/maze512-1-0.map",
                         "../data/our_data/random_obstacles.map/random_obstacles_0.map",
                         "../data/movingai_data/den011d.map/den011d.map",
                         "../data/movingai_data/street-map/Berlin_0_256.map"
                         ]

LIST_PATH_TO_FILE_SCENES = ["../data/movingai_data/maze-scen/maze512-1-0.map.scen",
                            "../data/our_data/random_obstacles.map-scen/random_obstacles_0.scen",
                            "../data/movingai_data/den011d.map-scen/den011d.map.scen",
                            "../data/movingai_data/street-scen/Berlin_0_256.map.scen"
                            ]

if "__main__" == __name__:
    read_maps_info = ReadMapsInfo()
    run_tests = RunTests()

    cur_cells = read_maps_info.read_map_from_file(full_path_to_file_map=LIST_PATH_TO_FILE_MAP[1])

    list_scenes = read_maps_info.read_scenes_from_file(full_path_to_file_scenes=LIST_PATH_TO_FILE_SCENES[1])

    list_all_tests = SampleTest.map_list_scenes_to_list_tests(cells=cur_cells,
                                                              list_scenes=list_scenes,
                                                              label='Name_of_group_test')
    # load set of tests
    run_tests.load_sample_tests(list_all_tests)

    # create launching DSTARLite structure
    run_d_star_lite = RunDStarLite()

    run_d_star_lite.load_map_cells(cur_cells)

    # create search_func:Dstar_lite (soon will be LSS_LRTA_star)
    search_func = run_d_star_lite.create_search_func(gui=True,
                                                     delay_for_every_step=10,
                                                     #exploration_setting='4N',
                                                     # view_range=4,
                                                     view_range=7,
                                                     dist_func=heuristic_4N,
                                                     #heuristic=heuristic_8N,
                                                     heuristic=heuristic_4N
                                                     )


    run_tests.load_search_func(search_func)

    # select specific data from all data
    select_small_data = run_tests.select_tests_in_bounds(prob_l=0.1, prob_r=0.2,
                                                         count_of_tests=2,
                                                         offset=10,
                                                         )

    # launch testing and get stats by factor_stats
    factor_stats = run_tests.run_all_test(list_sample_tests=select_small_data)

    pprint.pprint(factor_stats.get_stats())

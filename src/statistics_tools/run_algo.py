import pprint

# reading maps and scenes
from D_star_lite_vs_LSS_LRTA_star.src.data.read_maps_info import ReadMapsInfo

# struct for general test
from D_star_lite_vs_LSS_LRTA_star.src.data.run_tests import SampleTest, RunTests

# Dlite
from D_star_lite_vs_LSS_LRTA_star.src.D_start_lite.run_d_star_lite import RunDStarLite

LIST_PATH_TO_FILE_MAP = ["den011d.map/den011d.map",
                         "street-map/Berlin_0_256.map",
                         ReadMapsInfo.PATH_TO_FILE_MAP]

LIST_PATH_TO_FILE_SCENES = ["den011d.map-scen/den011d.map.scen",
                            "street-scen/Berlin_0_256.map.scen",
                            ReadMapsInfo.PATH_TO_FILE_SCENES]

if "__main__" == __name__:
    read_maps_info = ReadMapsInfo()
    run_tests = RunTests()

    cur_cells = read_maps_info.read_map_from_file(path_to_file_map=LIST_PATH_TO_FILE_MAP[0])

    list_scenes = read_maps_info.read_scenes_from_file(path_to_file_scenes=LIST_PATH_TO_FILE_SCENES[0])

    list_all_tests = SampleTest.map_list_scenes_to_list_tests(cells=cur_cells,
                                                              list_scenes=list_scenes,
                                                              label='Name_of_group_test')
    # load set of tests
    run_tests.load_sample_tests(list_all_tests)

    # create launching DSTARLite structure
    run_d_star_lite = RunDStarLite()

    run_d_star_lite.load_map_cells(cur_cells)

    # create search_func:Dstar_lite (soon will be LSS_LRTA_star)
    search_func = run_d_star_lite.create_search_func(gui=False,
                                                     delay_for_every_step=10,
                                                     exploration_setting='8N',
                                                     # view_range=4,
                                                     view_range=7,
                                                     )

    run_tests.load_search_func(search_func)

    # select specific data from all data
    select_small_data = run_tests.select_tests_in_bounds(prob_l=0.7, prob_r=0.8,
                                                         count_of_tests=10,
                                                         offset=2,
                                                         )

    # launch testing and get stats by factor_stats
    factor_stats = run_tests.run_all_test(list_sample_tests=select_small_data)

    pprint.pprint(factor_stats.get_stats())

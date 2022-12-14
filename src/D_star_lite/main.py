from run_d_star_lite import RunDStarLite
from src.data.read_maps_info import ReadMapsInfo
from src.data.run_tests import SampleTest, RunTests
from pprint import pprint

if __name__ == '__main__':
    read_maps_info = ReadMapsInfo()
    run_d_star_lite = RunDStarLite()
    run_tests = RunTests()

    path_to_file_map = "den011d.map/den011d.map"
    # path_to_file_map = "street-map/Berlin_0_256.map"
    # path_to_file_map = ReadMapsInfo.PATH_TO_FILE_MAP

    path_to_file_scenes = "den011d.map-scen/den011d.map.scen"
    # path_to_file_scenes = "street-scen/Berlin_0_256.map.scen"
    # path_to_file_scenes = ReadMapsInfo.PATH_TO_FILE_SCENES

    cur_cells = read_maps_info.read_map_from_file(path_to_file_map=path_to_file_map)
    # cur_cells = read_maps_info.get_simple_map()
    list_scenes = read_maps_info.read_scenes_from_file(path_to_file_scenes=path_to_file_scenes)
    # list_scenes = read_maps_info.get_simple_scene(is_list=True)

    run_d_star_lite.load_map_cells(cur_cells)

    list_all_tests = SampleTest.map_list_scenes_to_list_tests(cells=cur_cells,
                                                              list_scenes=list_scenes,
                                                              label='Labirint')

    run_tests.load_sample_tests(list_all_tests)

    search_func = run_d_star_lite.create_search_func(gui=False,
                                                     delay_for_every_step=10,
                                                     exploration_setting='8N',
                                                     # view_range=4,
                                                     view_range=7,
                                                     )

    run_tests.load_search_func(search_func)

    select_small_data = run_tests.select_tests_in_bounds(prob_l=0.7, prob_r=0.8,
                                                         count_of_tests=10,
                                                         offset=2,
                                                         )

    # print(select_small_data)
    factor_stats = run_tests.run_all_test(list_sample_tests=select_small_data)

    pprint(factor_stats.get_stats())

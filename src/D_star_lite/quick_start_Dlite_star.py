from src.D_star_lite.run_d_star_lite import RunDStarLite
from src.data.read_maps_info import ReadMapsInfo
from src.data.run_tests import SampleTest, RunTests
from pprint import pprint

if __name__ == '__main__':
    read_maps_info = ReadMapsInfo()
    run_d_star_lite = RunDStarLite()
    run_tests = RunTests()

    cur_cells = read_maps_info.get_simple_map()
    list_scenes = read_maps_info.get_simple_scene(is_list=True, num_scene=2)

    run_d_star_lite.load_map_cells(cur_cells)

    list_all_tests = SampleTest.map_list_scenes_to_list_tests(cells=cur_cells,
                                                              list_scenes=list_scenes,
                                                              label='Labirint')

    run_tests.load_sample_tests(list_all_tests)

    search_func = run_d_star_lite.create_search_func(gui=True,
                                                     delay_for_every_step=10,
                                                     exploration_setting='8N',
                                                     view_range=2,
                                                     )

    run_tests.load_search_func(search_func)

    factor_stats = run_tests.run_all_test()

    # pprint(factor_stats.get_stats())

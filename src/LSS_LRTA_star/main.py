from lss_lrta import lss_lrta_star, manhattan_distance
from search import SearchTreePQS
from src.data.read_maps_info import ReadMapsInfo
from src.data.run_tests import SampleTest, RunTests
from validating import simple_test, hard_test, toy_test, base_test, super_test, TestLSSLRTAstar

LIST_PATH_TO_FILE_MAP = ["den011d.map/den011d.map",
                         "street-map/Berlin_0_256.map",
                         ReadMapsInfo.PATH_TO_FILE_MAP]

LIST_PATH_TO_FILE_SCENES = ["den011d.map-scen/den011d.map.scen",
                            "street-scen/Berlin_0_256.map.scen",
                            ReadMapsInfo.PATH_TO_FILE_SCENES]


if __name__ == '__main__':
    # res = simple_test(lss_lrta_star, 1, manhattan_distance, SearchTreePQS, 10)
    # res = hard_test(lss_lrta_star, 1, manhattan_distance, SearchTreePQS, 20)
    # res = toy_test(lss_lrta_star, 0, manhattan_distance, SearchTreePQS, 100)
    # res = base_test(lss_lrta_star, 0, manhattan_distance, SearchTreePQS, 3)
    #res = simple_test(lss_lrta_star, 1, manhattan_distance, SearchTreePQS, 10)

    read_maps_info = ReadMapsInfo()
    cur_cells = read_maps_info.read_map_from_file(
        path_to_file_map=LIST_PATH_TO_FILE_MAP[0])
    list_scenes = read_maps_info.read_scenes_from_file(
        path_to_file_scenes=LIST_PATH_TO_FILE_SCENES[0])
    list_all_tests = SampleTest.map_list_scenes_to_list_tests(
        cells=cur_cells,
        list_scenes=list_scenes,
        label='Name_of_group_test')

    #sample_test = list_all_tests[3]
    #res_ = super_test(lss_lrta_star, sample_test, manhattan_distance, SearchTreePQS, 10)

    '''
    run_tests_lss_lrta_star = TestLSSLRTAstar(
        manhattan_distance, SearchTreePQS, lookahead=10, view_range=3
        ).get_vectorized_procedure()
    res = run_tests_lss_lrta_star(list_all_tests[0:100])
    print(res)
    '''

    ################################################
    run_test_lss_lrta_star = TestLSSLRTAstar(
        manhattan_distance, SearchTreePQS, lookahead=10, view_range=3
        ).get_procedure(in_frame=False)

    # initialize test runner
    run_tests = RunTests()
    run_tests.load_sample_tests(list_all_tests)
    run_tests.load_search_func(run_test_lss_lrta_star)
    # crop tests
    selected_tests = run_tests.select_tests_in_bounds(
        prob_l=0.7, prob_r=0.8,
        count_of_tests=20,
        offset=0)

    # launch testing and get stats by factor_stats
    factor_stats = run_tests.run_all_test(
        list_sample_tests=selected_tests)

    print(factor_stats.get_stats())


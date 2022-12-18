# reading maps and scenes
from src.data.read_maps_info import ReadMapsInfo

# struct for general test
from src.data.run_tests import SampleTest, RunTests

# Dlite
from src.D_start_lite.run_d_star_lite import RunDStarLite


class QuickTestRun:

    def __init__(self):
        self.select_small_data = None
        self.list_all_tests = None
        self.cells = None
        self.list_scenes = None

        self.read_maps_info = ReadMapsInfo()
        self.run_tests = RunTests()
        self.run_d_star_lite = RunDStarLite()

    def read_data_from_files(self, path_to_file_map=None,
                             path_to_file_scenes=None):
        self.cells = self.read_maps_info.read_map_from_file(path_to_file_map=path_to_file_map)
        self.list_scenes = self.read_maps_info.read_scenes_from_file(path_to_file_scenes=path_to_file_scenes)

        self.list_all_tests = SampleTest.map_list_scenes_to_list_tests(cells=self.cells,
                                                                       list_scenes=self.list_scenes,
                                                                       label='Name_of_group_test')
        # load set of tests
        self.run_tests.load_sample_tests(self.list_all_tests)

    def load_d_star_lite(self, gui=False,
                         delay_for_every_step=10,
                         exploration_setting='4N',
                         view_range=7, **kwargs):
        self.run_d_star_lite.load_map_cells(self.cells)

        search_func = self.run_d_star_lite.create_search_func(gui=gui,
                                                              delay_for_every_step=delay_for_every_step,
                                                              exploration_setting=exploration_setting,
                                                              view_range=view_range,
                                                              **kwargs
                                                              )

        self.run_tests.load_search_func(search_func)

    def select_tests_random(self,
                            count_of_tests=2,
                            seed=2312,
                            prob_l: float = 0.0, prob_r: float = 1.0,
                            offset: int = 0
                            ):
        self.select_small_data = self.run_tests.select_tests_by_random(count_of_tests=count_of_tests,
                                                                       seed=seed,
                                                                       prob_l=prob_l,
                                                                       prob_r=prob_r,
                                                                       offset=offset)

    def select_tests_in_bounds(self,
                               prob_l=0.7, prob_r=0.8,
                               count_of_tests=2,
                               offset=0):
        self.select_small_data = self.run_tests.select_tests_in_bounds(prob_l=prob_l,
                                                                       prob_r=prob_r,
                                                                       count_of_tests=count_of_tests,
                                                                       offset=offset)

    def run_all_test(self):
        factor_stats = self.run_tests.run_all_test(list_sample_tests=self.select_small_data)

        return factor_stats

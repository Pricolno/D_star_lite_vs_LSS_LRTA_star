from typing import List, Callable
from statistics_methods import Statistic, FactoryStatistics
from math import ceil, floor
from scene import Scene


class SampleTest:
    def __init__(self, cells: List[List[int]],
                 start: (int, int),
                 goal: (int, int),
                 label=None,
                 scene: Scene = None):
        self.start = start
        self.goal = goal
        self.cells = cells

        # need to understand is same two cells without explicit check
        self.label = label

        self.scene = scene

    def get_shape(self):
        return len(self.cells), len(self.cells[0])

    @classmethod
    def map_scene_to_test(cls, cells: List[List[int]],
                          scene: Scene,
                          label=None) -> "SampleTest":
        sample_test = SampleTest(cells=cells,
                                 start=scene.start, goal=scene.goal,
                                 label=label,
                                 scene=scene)

        return sample_test

    @classmethod
    def map_list_scenes_to_list_tests(cls, cells: List[List[int]],
                                      list_scenes: Scene,
                                      label=None) -> List['SampleTest']:
        list_tests = []
        for scene in list_scenes:
            list_tests.append(cls.map_scene_to_test(cells, scene, label))
        return list_tests

    def __str__(self):
        str_sampe_test = f"""SampleTest:start={self.start}, goal={self.goal}, shapes={self.get_shape()}"""
        return str_sampe_test


class RunTests:
    def __init__(self):
        self.search_func = None
        self.list_sample_tests = None

    def load_search_func(self, search_func: Callable[[SampleTest], None]):
        self.search_func = search_func

    def load_sample_tests(self, list_sample_tests: List[SampleTest]):
        self.list_sample_tests = list_sample_tests

    def run_test(self, sample_test: SampleTest) -> Statistic | None:
        stat = self.search_func(sample_test)
        print(f"stat={stat}")
        return stat

    def run_all_test(self, list_sample_tests: List[SampleTest] = None,
                     factory_statistics: FactoryStatistics = None) -> FactoryStatistics:
        if factory_statistics is None:
            factory_statistics = FactoryStatistics()

        if list_sample_tests is None:
            list_sample_tests = self.list_sample_tests

        # print(f"RunTests.run_all_test: len(list_sample_tests)={len(list_sample_tests)} {len(list_sample_tests[0])}")
        for number, sample_test in enumerate(list_sample_tests):
            print(f"Start run test №{number}")
            stat = self.run_test(sample_test)
            factory_statistics.add_stat(stat)

        return factory_statistics

    def select_tests_in_bounds(self, list_of_all_tests: List[SampleTest] = None,
                               prob_l: float = 0.0, prob_r: float = 1.0,
                               count_of_tests: int = 5,
                               offset: int = 0) -> List[SampleTest]:
        assert (0.0 <= prob_l < prob_r < 1.0)
        if list_of_all_tests is None:
            list_of_all_tests = self.list_sample_tests

        list_tests = []
        n = len(list_of_all_tests)
        min_ind = floor(n * prob_l) + offset

        max_ind = floor(n * prob_r)
        assert (0 <= min_ind <= max_ind < n)


        while count_of_tests > len(list_tests):
            for cur_ind in range(min_ind, max_ind + 1):
                list_tests.append(list_of_all_tests[cur_ind])

                if len(list_tests) == count_of_tests:
                    break

        return list_tests





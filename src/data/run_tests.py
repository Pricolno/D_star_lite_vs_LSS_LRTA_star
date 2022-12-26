import random
from math import floor
from typing import List, Callable
import numpy as np

from src.statistics_tools.statistics_methods import Statistic, FactoryStatistics
from src.Dijkstra.run_dijkstra import RunDijkstra
from src.data.sample_test import SampleTest


# sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
# from statistics_tools.statistics_methods import Statistic, FactoryStatistics


class RunTests:
    def __init__(self):
        self.count_of_maps = None
        self.all_count_of_tests = None
        self.search_func = None
        self.list_sample_tests = None

    def load_search_func(self, search_func: Callable[[SampleTest], Statistic]):
        self.search_func = search_func

    def load_sample_tests(self, list_sample_tests: List[SampleTest]):
        self.list_sample_tests = list_sample_tests

    def run_test(self, sample_test: SampleTest) -> Statistic:
        run_dij = RunDijkstra()
        optimal_length = run_dij.run_dijkstra_on_test(sample_test)
        # print(f"run_test| sample_test={sample_test} | optimal_length={optimal_length}")
        # print(sample_test.cells[0])
        if optimal_length is None:
            print(f"No exists path sample_test={sample_test}")
        else:
            print(f"Exists path sample_test={sample_test}")

        stat = self.search_func(sample_test)
        stat.Optimal_length = optimal_length
        # print(f"stat={stat}")
        return stat

    def run_all_test(self, list_sample_tests: List[SampleTest] = None,
                     factory_statistics: FactoryStatistics = None) -> FactoryStatistics:
        if factory_statistics is None:
            factory_statistics = FactoryStatistics()

        if list_sample_tests is None:
            list_sample_tests = self.list_sample_tests

        # print(f"RunTests.run_all_test: len(list_sample_tests)={len(list_sample_tests)} {len(list_sample_tests[0])}")
        for number, sample_test in enumerate(list_sample_tests):
            print(f"Start run test №{number}  |  all_count_of_tests={self.all_count_of_tests} | count_of_maps={self.count_of_maps}")
            self.all_count_of_tests += 1

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
        min_ind = floor((n - 1) * prob_l)
        max_ind = floor((n - 1) * prob_r)

        # print(f"min_ind={min_ind} max_ind={max_ind}")
        assert (0 <= min_ind <= max_ind < n)

        is_first_loop = True
        while count_of_tests > len(list_tests):
            cur_min_ind = min_ind
            if not is_first_loop:
                cur_min_ind = min_ind
            if is_first_loop:
                cur_min_ind = min_ind + offset
                is_first_loop = False

            for cur_ind in range(cur_min_ind, max_ind + 1):
                list_tests.append(list_of_all_tests[cur_ind])

                if len(list_tests) == count_of_tests:
                    break



        return list_tests

    def select_tests_by_random(self, list_of_all_tests: List[SampleTest] = None,
                               count_of_tests: int = 5,
                               seed: int = 1378,
                               prob_l: float = 0.0, prob_r: float = 1.0,
                               offset: int = 0) -> List[SampleTest]:
        if list_of_all_tests is None:
            list_of_all_tests = self.list_sample_tests
        random.seed(seed)
        n = len(list_of_all_tests)
        min_ind = floor((n - 1) * prob_l) + offset
        max_ind = floor((n - 1) * prob_r)
        assert (0 <= min_ind <= max_ind < n)

        inds = np.random.randint(min_ind, max_ind, size=count_of_tests)

        list_tests = []
        for ind in inds:
            list_tests.append(list_of_all_tests[ind])

        return list_tests

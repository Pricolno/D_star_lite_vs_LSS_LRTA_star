import os

import pandas as pd
import pickle


class Statistic:
    name_of_statistics = [
        "Cell_expansions",
        "Searchesc",
        "Trajectory_length",
        "Trajectory_length_per_search",
        "Search_time",
        "Search_time_per_search",
        "Search_time_per_action",
        "Optimal_length"
    ]

    def __init__(self, Cell_expansions=0,
                 Searchesc=0,
                 Trajectory_length=0,
                 Trajectory_length_per_search=0,
                 Search_time=0,
                 Search_time_per_search=None,
                 Search_time_per_action=None,
                 Optimal_length=0):

        self.Cell_expansions = Cell_expansions
        self.Searchesc = Searchesc
        self.Trajectory_length = Trajectory_length
        self.Trajectory_length_per_search = Trajectory_length_per_search
        self.Search_time = Search_time
        self.Search_time_per_search = Search_time_per_search
        self.Search_time_per_action = Search_time_per_action
        self.Optimal_length = Optimal_length

        self.distribution_Trajectory_length_per_search = None
        self.distribution_Search_time_per_search = None

    @classmethod
    def get_name_of_statistics(cls):
        return cls.name_of_statistics

    def gen_stats(self):
        for str_stat in Statistic.name_of_statistics:
            stat = self.__getattribute__(str_stat)
            yield str_stat, stat

    def __str__(self):
        res_str_stat = """"""
        for str_stat, stat in self.gen_stats():
            if stat is not None:
                res_str_stat += f"""{str_stat}={stat}|"""
        return res_str_stat


class FactoryStatistics:
    def __init__(self):
        for statistic in Statistic.name_of_statistics:
            self.__setattr__(statistic, statistic)

        self.stats = {name_of_statistic: [] for name_of_statistic in Statistic.name_of_statistics}
        self.count_of_maps = 0

    def clear_stats(self):
        self.stats = {name_of_statistic: [] for name_of_statistic in Statistic.name_of_statistics}

    def add_stat(self, statistic: Statistic):
        if statistic is None:
            statistic = Statistic()

        for str_stat, stat in statistic.gen_stats():
            self.stats[str_stat].append(stat)

    def append_factory_stats(self, factory_stats: 'FactoryStatistics'):
        for stat in factory_stats.get_stats():
            self.stats[stat].extend(factory_stats.get_stats()[stat])

    def get_stats(self):
        return self.stats

    def get_DataFrame(self) -> pd.DataFrame:
        df = pd.DataFrame.from_dict(self.get_stats())
        return df

    def save_stats(self, name_file='saved_stats', path_to_file='calcutated_stats', verbose=False):
        full_path_to_file = path_to_file + '/' + name_file + '.pickle'
        pickle.dump(self, file=open(full_path_to_file, "wb"))
        if verbose:
            print(f"Statistics is saved in {full_path_to_file} | count_of_maps={self.count_of_maps}")

    @classmethod
    def load_stats(cls, name_file='saved_stats', path_to_file='calcutated_stats', verbose=False):
        full_path_to_file = path_to_file + '/' + name_file + '.pickle'
        factor_stats = pickle.load(open(full_path_to_file, "rb"))
        if verbose:
            print(f"Statistics is loaded from {full_path_to_file}")
        return factor_stats

    @classmethod
    def is_exist_file(cls, name_file='saved_stats',
                      path_to_file='calcutated_stats'):
        full_path_to_file = path_to_file + '/' + name_file + '.pickle'
        return os.path.exists(full_path_to_file)

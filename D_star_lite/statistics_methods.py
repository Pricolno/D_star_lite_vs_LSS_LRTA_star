class Statistic:
    name_of_statistics = [
        "Cell_expansions",
        "Searchesc",
        "Trajectory_length",
        "Trajectory_length_per_search",
        "Search_time",
        "Search_time_per_search",
        "Search_time_per_action"
    ]

    def __init__(self, Cell_expansions=None,
                 Searchesc=None,
                 Trajectory_length=None,
                 Trajectory_length_per_search=None,
                 Search_time=None,
                 Search_time_per_search=None,
                 Search_time_per_action=None):

        self.Cell_expansions = Cell_expansions
        self.Searchesc = Searchesc
        self.Trajectory_length = Trajectory_length
        self.Trajectory_length_per_search = Trajectory_length_per_search
        self.Search_time = Search_time
        self.Search_time_per_search = Search_time_per_search
        self.Search_time_per_action = Search_time_per_action

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

    def clear_stats(self):
        self.stats = {name_of_statistic: [] for name_of_statistic in Statistic.name_of_statistics}

    def add_stat(self, statistic: Statistic):
        for str_stat, stat in statistic.gen_stats():
            self.stats[str_stat].append(stat)

    def get_stats(self):
        return self.stats

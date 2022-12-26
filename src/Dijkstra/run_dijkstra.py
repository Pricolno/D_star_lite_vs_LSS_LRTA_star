from typing import List
from src.Dijkstra.dijkstra import Dijkstra
from src.data.sample_test import SampleTest


class RunDijkstra:

    def __init__(self):
        self.cells = None
        self.start = None
        self.goal = None

    def load_map_cells(self, cells: List[List[int]]):
        self.cells = cells

    def load_map_start_goal(self, start: (int, int), goal: (int, int)):
        self.start = start
        self.goal = goal

    def load_test(self, sample_test: SampleTest):
        self.load_map_cells(sample_test.cells)
        self.load_map_start_goal(sample_test.start, sample_test.goal)

    def run_dijkstra(self):
        dijkstra = Dijkstra()
        dijkstra.load_map_cells(self.cells)
        dijkstra.load_map_start_goal(self.start, self.goal)
        path, length = dijkstra.run_dijkstra()
        # print(f"run_dijkstra| length={length}, path={path}")
        return path, length

    def run_dijkstra_on_test(self, sample_test: SampleTest):
        self.load_test(sample_test)
        path, length = self.run_dijkstra()

        return path, length

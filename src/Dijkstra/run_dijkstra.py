from typing import List
from src.Dijkstra.dijkstra import Dijkstra


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

    def get_path(self):
        dijkstra = Dijkstra()
        dijkstra.load_map_cells(self.cells)
        dijkstra.load_map_start_goal(self.start, self.goal)
        path, length = dijkstra.run_dijkstra()

        return length












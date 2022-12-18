from typing import List, Dict
import heapq as hq
import numpy as np
from src.Dijkstra.utils import get_movements_4n, heuristic_4N


class Dijkstra:
    def __init__(self, get_movements: str = '4N'):
        self.cells = None
        self.start = None
        self.goal = None

        if get_movements == '4N':
            self.get_movements = get_movements_4n
            self.heuristic = heuristic_4N

    def load_map_cells(self, cells: List[List[int]]):
        self.cells = cells

    def load_map_start_goal(self, start: (int, int), goal: (int, int)):
        self.start = start
        self.goal = goal

    def is_can_go(self, pos: tuple[int, int]):
        n, m = len(self.cells), len(self.cells[0])
        return 0 <= pos[0] < n and 0 <= pos[1] < m

    def is_empty_pos(self, pos: tuple[int, int]):
        return not self.cells[pos[0]][pos[1]]

    def get_path(self, pred: Dict[tuple[int, int], tuple[int, int]]):
        if pred[self.goal] is None:
            return None, None

        path = [self.goal]
        cur_u = self.goal
        full_cost = 0

        while not (cur_u == self.start):
            full_cost += self.heuristic(cur_u, pred[cur_u])
            #print(full_cost)

            cur_u = pred[cur_u]
            path.append(cur_u)
        path = list(reversed(path))

        return path, full_cost

    def run_dijkstra(self):
        n, m = len(self.cells), len(self.cells[0])

        visited = dict()
        for i in range(n):
            for j in range(m):
                visited[(i, j)] = False

        dist = dict()
        for i in range(n):
            for j in range(m):
                dist[(i, j)] = np.inf

        pred = dict()
        for i in range(n):
            for j in range(m):
                pred[(i, j)] = None

        queue = []
        dist[self.start] = 0

        hq.heappush(queue, (0, self.start))

        while len(queue) > 0:
            g, u = hq.heappop(queue)
            visited[u] = True

            for u_next in self.get_movements(*u):
                if not self.is_can_go(u_next):
                    continue

                if not self.is_empty_pos(u_next):
                    continue

                if visited[u_next]:
                    continue

                cost = self.heuristic(u, u_next)
                g_next = g + cost

                if dist[u_next] > g_next:
                    #print(f"{u} {u_next}")
                    dist[u_next] = g_next
                    pred[u_next] = u
                    hq.heappush(queue, (g_next, u_next))

        path = self.get_path(pred)

        return path

import time
from typing import List
import numpy as np

from src.D_star_lite.ordered_dict import OrderedDictWithRemove, Priority
from src.D_star_lite.grid import OccupancyGridMap
from src.D_star_lite.utils import heuristic_4N, heuristic_8N, Vertices

OBSTACLE = 255
UNOCCUPIED = 0


class DStarLite:
    # BUG_OF_LOOPING = 1000
    WORK_IS_OVER = 1
    TIME_LIMIT = 400
    NOT_FIND_PATH = 500

    LAST_SET_TIMER = None
    TIME_LIMIT_FOR_FIND_MOVE = 30.  # in second

    def __init__(self, map: OccupancyGridMap = None,
                 s_start: (int, int) = None, s_goal: (int, int) = None,
                 restart=False,
                 **kwargs):
        """
        :param map: the ground truth map of the environment provided by gui
        :param s_start: start location
        :param s_goal: end location
        """
        self.dist_func = heuristic_4N
        self.heuristic = heuristic_4N
        if "exploration_setting" in kwargs:
            if kwargs['exploration_setting'] == '4N':
                self.heuristic = heuristic_4N
            elif kwargs['exploration_setting'] == '8N':
                self.heuristic = heuristic_8N

        if "heuristic" in kwargs:
            self.heuristic = kwargs['heuristic']

        if 'dist_func' in kwargs:
            self.dist_func = kwargs['dist_func']
            # print(f"DStarLite | dist_func= (_-_-_)")

        # for calc stats
        self.Cell_expansions = None

        self.new_edges_and_old_costs = None

        # algorithm start
        assert ('s_start' in self.__dict__ or (s_start is not None))
        if s_start is not None:
            self.s_start = s_start
        assert ('s_goal' in self.__dict__ or (s_goal is not None))
        if s_goal is not None:
            self.s_goal = s_goal
        assert ('map' in self.__dict__ or (map is not None))
        if map is not None:
            self.map = map

        self.s_last = s_start
        self.k_m = 0  # accumulation
        # OPEN : sorted struct
        self.U = OrderedDictWithRemove()

        # print(self.map)

        self.rhs = np.ones((self.map.y_size, self.map.x_size)) * np.inf
        self.g = self.rhs.copy()

        if True or not restart:
            # print(f"DStarLite.init: kwargs={kwargs}")
            self.sensed_map = OccupancyGridMap(y_size=self.map.y_size,
                                               x_size=self.map.x_size,
                                               # exploration_setting='8N',
                                               **kwargs)

        self.rhs[self.s_goal] = 0
        self.U.insert(self.s_goal, Priority(self.heuristic(self.s_start, self.s_goal), 0))

    def calculate_key(self, s: (int, int)):
        """
        param s: the vertex we want to calculate key
        :return: Priority class of the two keys
        """
        k1 = min(self.g[s], self.rhs[s]) + self.heuristic(self.s_start, s) + self.k_m
        k2 = min(self.g[s], self.rhs[s])
        return Priority(k1, k2)

    def c(self, u: (int, int), v: (int, int)) -> float:
        """
        calcuclate the cost between nodes
        :param u: from vertex
        :param v: to vertex
        :return: euclidean distance to traverse. inf if obstacle in path
        """
        if not self.sensed_map.is_unoccupied(u) or not self.sensed_map.is_unoccupied(v):
            return float('inf')
        else:
            return self.dist_func(u, v)

    def contain(self, u: (int, int)) -> (int, int):
        # return u in self.U.vertices_in_heap
        return u in self.U

    def update_vertex(self, u: (int, int)):
        if self.g[u] != self.rhs[u] and self.contain(u):
            self.U.update(u, self.calculate_key(u))
        elif self.g[u] != self.rhs[u] and not self.contain(u):
            self.U.insert(u, self.calculate_key(u))
        elif self.g[u] == self.rhs[u] and self.contain(u):
            self.U.remove(u)

    def compute_shortest_path(self):
        # print(f"len(compute_shortest_path)={len(self.U)} | U.top_key()={self.U.top_key()} calculate_key(self.s_start)={self.s_start}")

        while self.U.top_key() < self.calculate_key(self.s_start) or self.rhs[self.s_start] > self.g[self.s_start]:
            # calc stat.Cell_expansions
            self.Cell_expansions += 1

            u = self.U.top()
            k_old = self.U.top_key()
            k_new = self.calculate_key(u)
            # print(f"D_star_lite.compute_shortest_path u={u} k_old={k_old} k_new={k_new}")

            if k_old < k_new:
                # print(f"COMPUTE_S_P |    K_OLD: {k_old}, K_NEW: {k_new}")
                self.U.update(u, k_new)
            elif self.g[u] > self.rhs[u]:
                # print(f"COMPUTE_S_P |    g: {self.g[u]}, rhs: {self.rhs[u]}")
                self.g[u] = self.rhs[u]
                self.U.remove(u)
                pred = self.sensed_map.succ(vertex=u)
                for s in pred:
                    if s != self.s_goal:
                        # print(f"COMPUTE_S_P |        rhs: {self.rhs[s]}, new rhs: {min(self.rhs[s], self.c(s, u) + self.g[u])}")
                        self.rhs[s] = min(self.rhs[s], self.c(s, u) + self.g[u])
                    self.update_vertex(s)
            else:
                # print(f"COMPUTE_S_P |    g: inf")
                self.g_old = self.g[u]
                self.g[u] = float('inf')
                pred = self.sensed_map.succ(vertex=u)
                pred.append(u)
                for s in pred:
                    if self.rhs[s] == self.c(s, u) + self.g_old:
                        if s != self.s_goal:
                            min_s = float('inf')
                            succ = self.sensed_map.succ(vertex=s)
                            for s_ in succ:
                                temp = self.c(s, s_) + self.g[s_]
                                if min_s > temp:
                                    min_s = temp
                            self.rhs[s] = min_s
                    # self.update_vertex(u)
                    self.update_vertex(s)

    def rescan(self) -> Vertices:

        new_edges_and_old_costs = self.new_edges_and_old_costs
        self.new_edges_and_old_costs = None
        return new_edges_and_old_costs

    @classmethod
    def check_bug_of_looping(cls, path: List[tuple[int, int]]):
        # s t s t s  (s, t - any position, mean bad loop)
        # if len(path) >= 4:

        if len(path) >= 8:
            if path[-1] == path[-3] == path[-5] == path[-7] \
                    and path[-8] == path[-6] == path[-2] == path[-4]:
                return True
        return False

    def set_timer(self):
        """in seconds"""
        self.LAST_SET_TIMER = time.time()

    def get_time_from_timer(self):
        """in seconds"""
        assert self.LAST_SET_TIMER is not None
        return time.time() - self.LAST_SET_TIMER

    def move_and_replan(self, robot_position: (int, int)) -> tuple['Flag_running', 'path', 'g', 'rhs']:
        path = [robot_position]
        self.s_start = robot_position
        self.s_last = self.s_start
        # print(f"DStarLite.move_and_replan start robot_position={robot_position}")
        self.compute_shortest_path()
        # print(f"DStarLite.move_and_replan finish firsh compute_shortest_path")

        self.set_timer()

        while self.s_start != self.s_goal:
            if self.get_time_from_timer() > self.TIME_LIMIT_FOR_FIND_MOVE:
                return self.TIME_LIMIT, path, self.g, self.rhs

            # assert (self.rhs[self.s_start] != float('inf')), "There is no known path!"
            if self.rhs[self.s_start] == float('inf'):
                return self.NOT_FIND_PATH, None, None, None

            succ = self.sensed_map.succ(self.s_start, avoid_obstacles=True)

            min_s = float('inf')
            arg_min = None
            # print(f"move_and_replan | succ={succ}")
            for s_ in succ:
                temp = self.c(self.s_start, s_) + self.g[s_]
                if temp < min_s:
                    min_s = temp
                    arg_min = s_

            # print(f"move_and_replan | arg_min ={arg_min} min_s={min_s} cur={self.s_start} | DEBUG")

            ### algorithm sometimes gets stuck here for some reason !!! FIX
            self.s_start = arg_min
            path.append(self.s_start)

            # scan graph for changed costs
            changed_edges_with_old_cost = self.rescan()

            # print(f"move_and_replan | changed_edges_with_old_cost={changed_edges_with_old_cost} | DEBUG")
            # if any edge costs changed
            if changed_edges_with_old_cost:

                # print(f"self.s_last={self.s_last} self.s_start={self.s_start}")

                self.k_m += self.heuristic(self.s_last, self.s_start)
                self.s_last = self.s_start

                # for all directed edges (u,v) with changed edge costs
                vertices = changed_edges_with_old_cost.vertices
                for vertex in vertices:
                    v = vertex.pos
                    succ_v = vertex.edges_and_c_old
                    for u, c_old in succ_v.items():
                        c_new = self.c(u, v)
                        # Update the edge cost c(u, v) (?)

                        if c_old > c_new:
                            if u != self.s_goal:
                                self.rhs[u] = min(self.rhs[u], self.c(u, v) + self.g[v])
                        elif self.rhs[u] == c_old + self.g[v]:
                            if u != self.s_goal:
                                min_s = float('inf')
                                succ_u = self.sensed_map.succ(vertex=u)
                                for s_ in succ_u:
                                    temp = self.c(u, s_) + self.g[s_]
                                    if min_s > temp:
                                        min_s = temp
                                self.rhs[u] = min_s

                        self.update_vertex(u)
                        # self.update_vertex(u)

                # self.compute_shortest_path()
            self.compute_shortest_path()

            # DEBUG
            '''
            
            if self.s_start == (98, 83):
                succ = self.sensed_map.succ(self.s_start, avoid_obstacles=True)
                min_s = float('inf')
                arg_min = None
                print(f"move_and_replan | succ={succ}")
                for s_ in succ:
                    temp = self.c(self.s_start, s_) + self.g[s_]
                    if temp < min_s:
                        min_s = temp
                        arg_min = s_

                assert(1 == 0), f"move_and_replan | arg_min ={arg_min} min_s={min_s} cur={self.s_start}"
                
            '''
            # DEBUG

        # print("path found!")
        return self.WORK_IS_OVER, path, self.g, self.rhs

    def restart_d_star(self, **kwargs):
        self = self.__init__(restart=True, **kwargs)
        return self

    def __str__(self):
        str_dstar = f"""DStarLite:start={self.s_start}, goal={self.s_goal}, shape_map={self.map.map_extents}"""
        return str_dstar

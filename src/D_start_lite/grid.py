import numpy as np
from typing import Dict, List

from D_star_lite_vs_LSS_LRTA_star.src.D_start_lite.utils import get_movements_4n, get_movements_8n, heuristic, Vertices, Vertex


OBSTACLE = 255
UNOCCUPIED = 0


class OccupancyGridMap:
    def __init__(self, y_size, x_size, exploration_setting='8N',
                 **kwargs):
        """
        set initial values for the map occupancy grid
        """
        #print(f"OccupancyGridMap.__init__: exploration_setting={exploration_setting}")
        self.y_size = y_size
        self.x_size = x_size

        # the map extents in units [m]
        self.map_extents = (y_size, x_size)

        # the obstacle map
        self.occupancy_grid_map = np.full(self.map_extents,
                                          UNOCCUPIED, dtype=np.uint8)
        # there are found info
        self.visited = np.full(self.map_extents, False, dtype=np.bool)

        # obstacles
        self.exploration_setting = exploration_setting

    def clear_visited(self):
        # there are found info
        self.visited = np.full(self.map_extents, False, dtype=np.bool)

    def clear_occupancy(self, **kwargs):

        # the obstacle map
        self.occupancy_grid_map = np.full(self.map_extents,
                                          UNOCCUPIED, dtype=np.uint8)

    @classmethod
    def read_from_string(cls, cell_str, y_size, x_size, exploration_setting='8N'):
        """
        Converting a string (with '#' representing obstacles and '.' representing free cells) to a grid

        Parameters
        ----------
        cell_str : str
            String which contains map data
        y_size : int
            Number of grid columns
        x_size : int
            Number of grid rows
        """

        ogrid = cls(y_size, x_size, exploration_setting)

        cell_lines = cell_str.split("\n")
        # print(cell_lines)
        i = 0
        j = 0
        for l in cell_lines:
            if len(l) != 0:
                j = 0
                # print(f"len(l)={len(l)} | l={l}")
                for c in l:
                    # print(f"i={i}, j={j}")

                    if c == '.':
                        ogrid.occupancy_grid_map[i][j] = UNOCCUPIED
                    elif c == '#' or c == 'T' or c == '@':
                        ogrid.occupancy_grid_map[i][j] = OBSTACLE
                    else:
                        continue
                    # print(f"ogrid.occupancy_grid_map[{i}][{j}]=", ogrid.occupancy_grid_map[i][j])

                    j += 1
                if j != ogrid.x_size:
                    raise Exception("Size Error. Map width = ", j, ", but must be", ogrid.x_size)

                # print(f"ogrid.occupancy_grid_map[{i}]=", ogrid.occupancy_grid_map[i])
                i += 1

        if i != ogrid.y_size:
            raise Exception("Size Error. Map height = ", i, ", but must be", ogrid.y_size)

        return ogrid

    def get_size(self):
        return self.map_extents

    def get_map(self):
        """
        :return: return the current occupancy grid map
        """
        return self.occupancy_grid_map

    def set_map(self, new_ogrid):
        """
        :param new_ogrid:
        :return: None
        """
        self.occupancy_grid_map = new_ogrid

    def is_unoccupied(self, pos: (int, int)) -> bool:
        """
        :param pos: cell position we wish to check
        :return: True if cell is occupied with obstacle, False else
        """
        (y, x) = (round(pos[0]), round(pos[1]))  # make sure pos is int
        (row, col) = (y, x)

        # if not self.in_bounds(cell=(x, y)):
        #    raise IndexError("Map index out of bounds")

        return self.occupancy_grid_map[row][col] == UNOCCUPIED

    def in_bounds(self, cell: (int, int)) -> bool:
        """
        Checks if the provided coordinates are within
        the bounds of the grid map
        :param cell: cell position (x,y)
        :return: True if within bounds, False else
        """
        (y, x) = cell
        return 0 <= y < self.y_size and 0 <= x < self.x_size

    def filter(self, neighbors: List, avoid_obstacles: bool):
        """
        :param neighbors: list of potential neighbors before filtering
        :param avoid_obstacles: if True, filter out obstacle cells in the list
        :return:
        """
        if avoid_obstacles:
            return [node for node in neighbors if self.in_bounds(node) and self.is_unoccupied(node)]
        return [node for node in neighbors if self.in_bounds(node)]

    def succ(self, vertex: (int, int), avoid_obstacles: bool = False) -> list:
        """
        :param avoid_obstacles:
        :param vertex: vertex you want to find direct successors from
        :return:
        """
        (y, x) = vertex
        #print(f"OccupancyGridMap.succ: exploration_setting={self.exploration_setting}")
        if self.exploration_setting == '4N':  # change this
            movements = get_movements_4n(y=y, x=x)
        else:
            movements = get_movements_8n(y=y, x=x)

        # not needed. Just makes aesthetics to the path
        if (x + y) % 2 == 0: movements.reverse()

        filtered_movements = self.filter(neighbors=movements, avoid_obstacles=avoid_obstacles)
        return list(filtered_movements)

    def set_obstacle(self, pos: (int, int)):
        """
        :param pos: cell position we wish to set obstacle
        :return: None
        """
        (y, x) = (round(pos[0]), round(pos[1]))  # make sure pos is int
        (row, col) = (y, x)
        self.occupancy_grid_map[row, col] = OBSTACLE

    def remove_obstacle(self, pos: (int, int)):
        """
        :param pos: position of obstacle
        :return: None
        """
        (y, x) = (round(pos[0]), round(pos[1]))  # make sure pos is int
        (row, col) = (y, x)
        self.occupancy_grid_map[row, col] = UNOCCUPIED

    def local_observation(self, global_position: (int, int), view_range: int = 2) -> Dict:
        """
        :param global_position: position of robot in the global map frame
        :param view_range: how far ahead we should look
        :return: dictionary of new observations
        """
        (py, px) = global_position
        nodes = [(y, x) for y in range(py - view_range, py + view_range + 1)
                 for x in range(px - view_range, px + view_range + 1)
                 if self.in_bounds((y, x))]
        #print(f"OccupancyGridMap.local_observation view_range={view_range}  len(nodes)={len(nodes)} nodes={nodes}")
        for y, x in nodes:
            self.visited[y][x] = True

        return {node: UNOCCUPIED if self.is_unoccupied(pos=node) else OBSTACLE for node in nodes}

    @staticmethod
    def covert_list2d_to_ogrid(cells: List[List[int]],
                               exploration_setting='8N',
                               **kwargs) -> "OccupancyGridMap":
        #print(f"covert_list2d_to_ogrid:cells={cells}")
        # need assert for dim 2
        y_size = len(cells)
        x_size = len(cells[0])

        #print(f"OccupancyGridMap.covert_list2d_to_ogrid: kwargs={kwargs}")
        ogrid = OccupancyGridMap(y_size=y_size,
                                 x_size=x_size,
                                 exploration_setting=exploration_setting)
        for row in range(len(cells)):
            for col in range(len(cells[0])):
                if cells[row][col] == 1:
                    ogrid.set_obstacle((row, col))

        return ogrid


class SLAM:
    def __init__(self, map: OccupancyGridMap,
                 view_range: int):
        self.ground_truth_map = map
        self.slam_map = OccupancyGridMap(y_size=map.y_size,
                                         x_size=map.x_size,
                                         exploration_setting=map.exploration_setting)
        self.view_range = view_range

    def restart_slam(self, **kwargs):
        # change 8N -> 4N
        self.slam_map.clear_occupancy()
        self.slam_map.clear_visited()

    def set_ground_truth_map(self, gt_map: OccupancyGridMap):
        self.ground_truth_map = gt_map

    def c(self, u: (int, int), v: (int, int)) -> float:
        """
        calcuclate the cost between nodes
        :param u: from vertex
        :param v: to vertex
        :return: euclidean distance to traverse. inf if obstacle in path
        """
        if not self.slam_map.is_unoccupied(u) or not self.slam_map.is_unoccupied(v):
            return float('inf')
        else:
            return heuristic(u, v)

    def rescan(self, global_position: (int, int)):
        #print(f"SLAM.rescan start global_position={global_position}")
        # rescan local area
        local_observation = self.ground_truth_map.local_observation(global_position=global_position,
                                                                    view_range=self.view_range)

        #print(f"SLAM.rescan finish find len(local_observation) = {len((local_observation))}, local_observation={local_observation}")
        vertices = self.update_changed_edge_costs(local_grid=local_observation)

        return vertices, self.slam_map

    def update_changed_edge_costs(self, local_grid: Dict) -> Vertices:
        #print(f"SLAM.update_changed_edge_costs start  local_grid={local_grid}")
        vertices = Vertices()
        for node, value in local_grid.items():
            # if obstacle
            if value == OBSTACLE:
                if self.slam_map.is_unoccupied(node):
                    v = Vertex(pos=node)
                    succ = self.slam_map.succ(node)
                    for u in succ:
                        v.add_edge_with_cost(succ=u, cost=self.c(u, v.pos))
                    vertices.add_vertex(v)
                    self.slam_map.set_obstacle(node)
            else:
                # if white cell
                if not self.slam_map.is_unoccupied(node):
                    v = Vertex(pos=node)
                    succ = self.slam_map.succ(node)
                    for u in succ:
                        v.add_edge_with_cost(succ=u, cost=self.c(u, v.pos))
                    vertices.add_vertex(v)
                    self.slam_map.remove_obstacle(node)
        return vertices

    def __str__(self):
        str_slam = f"""SLAM: view_range={self.view_range} """
        return str_slam



from typing import List
from D_star_lite_vs_LSS_RTA_star.src.data.py_data.simple_maps import SIMPLE_MAPS
from D_star_lite_vs_LSS_RTA_star.src.data.py_data.simple_scenes import SIMPLE_SCENES
from D_star_lite_vs_LSS_RTA_star.src.data.scene import Scene


class ReadMapsInfo:
    SCENES_FILE = "maze512-1-0.map.scen"
    MAP_FILE = "maze512-1-0.map"
    DIR_MAP_FILE = "maze-map"
    DIR_SCENES_FILE = "maze-scen"

    PATH_TO_FILE_MAP = "maze-map\maze512-1-0.map"
    PATH_TO_FILE_SCENES = "maze-scen\maze512-1-0.map.scen"

    path_to_dir_data = "../data/movingai_data"

    def __init__(self, path_to_file_map=None,
                 path_to_file_scenes=None):
        if path_to_file_map is None:
            path_to_file_map = self.PATH_TO_FILE_MAP
        if path_to_file_scenes is None:
            path_to_file_scenes = self.PATH_TO_FILE_SCENES

        self.path_to_file_map = path_to_file_map
        self.path_to_file_scenes = path_to_file_scenes

        # print(f"Init ReadMapsInfo")

    def set_path_to_file_map(self, path_to_file_map):
        self.path_to_file_map = path_to_file_map

    def set_path_to_file_scene(self, path_to_file_scenes):
        self.path_to_file_scenes = path_to_file_scenes

    def get_path_to_file_map(self):
        return self.path_to_file_map

    def get_path_path_to_file_scene(self):
        return self.path_to_file_scenes

    def get_full_path_to_file_map(self, path_to_file_map=None):
        if path_to_file_map is None:
            path_to_file_map = self.path_to_file_map
        return self.path_to_dir_data + '\\' + path_to_file_map

    def get_full_path_to_file_scenes(self, path_to_file_scenes=None):
        if path_to_file_scenes is None:
            path_to_file_scenes = self.path_to_file_scenes
        return self.path_to_dir_data + '\\' + path_to_file_scenes

    def read_map_from_file(self, path_to_file_map: str = None) -> List[List[int]]:
        """
        Reads map.
        """

        if not self.path_to_file_map == path_to_file_map:
            #print("self.path_to_file_map != path_to_file_map")
            pass
        if path_to_file_map is None:
            path_to_file_map = self.path_to_file_map
        full_path_to_file_map = self.get_full_path_to_file_map(path_to_file_map=path_to_file_map)

        map_file = open(full_path_to_file_map)
        # unless
        map_type = map_file.readline()

        height = int(map_file.readline().strip().split()[1])
        width = int(map_file.readline().strip().split()[1])

        _ = map_file.readline()

        cells = [[0 for _ in range(width)] for _ in range(height)]
        i = 0
        j = 0

        for l in map_file:
            l = l.strip()
            j = 0
            for c in l:
                if c == '.':
                    cells[i][j] = 0
                else:
                    cells[i][j] = 1
                j += 1

            if j != width:
                raise Exception("Size Error. Map width = ", j, ", but must be",
                                width, "(map line: ", i, ")")

            i += 1
            if i == height:
                break
        print(f"Read map from file={full_path_to_file_map}")

        return cells

    @staticmethod
    def read_map_from_string(cell_str: str,
                             height: int, width: int) -> List[List[int]]:
        """
        Reads map.
        """
        cells = [[0 for _ in range(width)] for _ in range(height)]

        cell_lines = cell_str.split("\n")
        i = 0
        j = 0
        for l in cell_lines:
            if len(l) != 0:
                j = 0
                for c in l:
                    if c == '.':
                        cells[i][j] = 0
                    elif c == '#' or c == 'T' or c == '@':
                        cells[i][j] = 1
                    else:
                        continue

                    j += 1
                if j != width:
                    raise Exception("Size Error. Map width = ", j, ", but must be", width)

                # print(f"ogrid.occupancy_grid_map[{i}]=", ogrid.occupancy_grid_map[i])
                i += 1

        if i != height:
            raise Exception("Size Error. Map height = ", i, ", but must be", height)

        return cells

    def read_scenes_from_file(self, path_to_file_scenes: str = None) -> List[Scene]:
        """
        return: hard_lvl, map_file, height, width, start_i, start_j, goal_i, goal_j, optimal_length
        """

        if not self.path_to_file_scenes == path_to_file_scenes:
            #print("self.path_to_file_scenes != path_to_file_scenes")
            pass
        if path_to_file_scenes is None:
            path_to_file_scenes = self.path_to_file_scenes
        full_path_to_file_scenes = self.get_full_path_to_file_scenes(path_to_file_scenes=path_to_file_scenes)

        scenes_file = open(full_path_to_file_scenes)
        version = scenes_file.readline()
        scenes_list = []
        for scene in scenes_file:
            scene_info = scene.strip().split()
            # print(scen_info)

            hard_lvl = int(scene_info[0])
            # map_file = scene_info[1]

            width = int(scene_info[2])
            height = int(scene_info[3])

            start_j = int(scene_info[4])
            start_i = int(scene_info[5])

            goal_j = int(scene_info[6])
            goal_i = int(scene_info[7])

            optimal_length = float(scene_info[8])

            struct_scene = Scene(hard_lvl,
                                 height, width,
                                 start_i, start_j,
                                 goal_i, goal_j,
                                 optimal_length)

            scenes_list.append(struct_scene)
        # print(f"Read scene from file={full_path_to_file_scenes}")
        # hard_lvl, height, width, start_j, start_i, goal_j, goal_i, optimal_length
        return scenes_list

    @classmethod
    def get_simple_map(cls, num_map=0):
        cells = ReadMapsInfo.read_map_from_string(*SIMPLE_MAPS[num_map])
        return cells

    @classmethod
    def get_simple_scene(cls, num_scene=1, is_list=False):
        scene = SIMPLE_SCENES[num_scene]
        if is_list:
            scene = [scene]
        return scene

    """@classmethod
    def get_simple_test(cls, num_scene=0, num_map=0):
        cells = cls.get_simple_map(num_map=num_map)
        scene = cls.get_simple_scene(num_scene=num_scene)
        sample_test = SampleTest(cells, scene.start, scene.goal)
        return sample_test"""

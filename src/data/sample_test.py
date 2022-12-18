from typing import List

from src.data.scene import Scene


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
        self.Optimal_length = None
        if scene is not None:
            self.Optimal_length = scene.optimal_length

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
                                      list_scenes: List[Scene],
                                      label=None) -> List['SampleTest']:
        list_tests = []
        for scene in list_scenes:
            list_tests.append(cls.map_scene_to_test(cells, scene, label))
        return list_tests

    def __str__(self):
        str_sampe_test = f"""SampleTest:start={self.start}, goal={self.goal}, shapes={self.get_shape()}"""
        return str_sampe_test
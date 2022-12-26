import time
from typing import Callable, List
import pygame
import numpy as np
from PIL import Image
import os

from src.D_star_lite.gui import Animation
from src.D_star_lite.d_star_lite import DStarLite
from src.D_star_lite.grid import OccupancyGridMap, SLAM
from src.data.run_tests import SampleTest
from src.data.read_maps_info import ReadMapsInfo
from src.data.py_data.simple_maps import SIMPLE_MAPS
from src.data.py_data.simple_scenes import SIMPLE_SCENES
from src.statistics_tools.statistics_methods import Statistic


class RunDStarLite:
    def __init__(self):
        self.number_image_for_gif = None
        self.dist_func = None
        self.heuristic = None

        self.last_time_set_timer = None
        self.ogrid = None
        self.is_current_ogrid_correct_in_dstar = False
        self.label_map = None

        # (y, x):(int, int)
        self.s_start = None
        self.s_goal = None

        self.dstar = None

        self.view_range = 3
        self.slam = None

        self.gui = None

        self.last_position = None
        self.new_position = None
        self.new_map = None

    def load_str_map(self, cell_str: str, y_size: int, x_size: int,
                     exploration_setting: str = '4N', label=None):
        self.ogrid = OccupancyGridMap.read_from_string(cell_str, y_size, x_size, exploration_setting)
        self.is_current_ogrid_correct_in_dstar = False
        self.label_map = label

    def load_map_ogrid(self, ogrid: OccupancyGridMap, label=None):
        self.ogrid = ogrid
        self.is_current_ogrid_correct_in_dstar = False
        self.label_map = label

    def load_map_cells(self, cells: List[List[int]], label=None):
        self.ogrid = OccupancyGridMap.covert_list2d_to_ogrid(cells)
        self.is_current_ogrid_correct_in_dstar = False
        self.label_map = label

    def load_start_goal(self, s_start: (int, int), s_goal: (int, int)):
        self.s_start = s_start
        self.s_goal = s_goal

    def load_view_range(self, view_range: int):
        self.view_range = view_range

    def load_heuristic(self, heuristic: Callable):
        self.heuristic = heuristic

    def load_dist_func(self, dist_func: Callable):
        self.dist_func = dist_func

    # def load_exploration_setting(self, exploration_setting: str):
    #    self.exploration_setting = exploration_setting

    def create_slam(self):
        self.slam = SLAM(map=self.ogrid,
                         view_range=self.view_range)

    def create_dstar(self):
        assert (self.ogrid is not None and self.s_start is not None and self.s_goal is not None)

        if not self.is_current_ogrid_correct_in_dstar:
            self.dstar = DStarLite(map=self.ogrid,
                                   s_start=self.s_start,
                                   s_goal=self.s_goal)
            self.is_current_ogrid_correct_in_dstar = True
            self.create_slam()

        else:
            self.dstar = DStarLite(map=self.ogrid,
                                   s_start=self.s_start,
                                   s_goal=self.s_goal,
                                   heuristic=self.heuristic,
                                   dist_func=self.dist_func)
            self.is_current_ogrid_correct_in_dstar = True

            self.create_slam()

    def create_gui(self, delay_for_every_step=50):
        self.gui = Animation(title="D* Lite Path Planning",
                             ogdrid=self.ogrid,
                             viewing_range=self.view_range,
                             start=self.s_start,
                             goal=self.s_goal,
                             delay_for_every_step=delay_for_every_step)

    def restart_all(self, launch_gui=False,
                    delay_for_every_step=50,
                    **kwargs):

        self.dstar.restart_d_star(**kwargs)
        self.slam.restart_slam(**kwargs)

        if launch_gui:
            self.create_gui(delay_for_every_step=delay_for_every_step)

        if self.gui is not None:
            self.gui.restart_gui()
            self.gui.restart = False
            self.new_map = self.gui.world

        self.new_position = self.dstar.s_start
        self.last_position = None

    def show_finaly_algo(self, during=5, path=None,
                         brightness=True, is_viewing_range=True, **kwargs):
        self.create_gui()
        self.gui.display_all_map(path=path,
                                 brightness=brightness,
                                 is_viewing_range=is_viewing_range)
        pygame.display.flip()
        time.sleep(during)
        # pygame.quit()

    def save_image(self, name_file="d_lite_star", full_path_to_file=None):
        if full_path_to_file is not None:
            pygame.image.save(self.gui.screen, f"{full_path_to_file}.jpeg")

        else:
            pygame.image.save(self.gui.screen, f"images/{name_file}.jpeg")

    @classmethod
    def clear_dir(cls, full_path_to_file):
        for name_file in os.listdir(full_path_to_file):
            full_path_to_maps = f"{full_path_to_file}/{name_file}"
            os.remove(f"{full_path_to_maps}")

    def save_image_for_gif(self, full_path_to_file,
                           name_saved_photo):
        if self.number_image_for_gif is None or self.number_image_for_gif == 0:
            self.number_image_for_gif = 0
            # clear all image
            self.clear_dir(full_path_to_file=full_path_to_file)

        cur_name_file = full_path_to_file + '/' + f'{name_saved_photo}_{self.number_image_for_gif}'
        self.save_image(full_path_to_file=cur_name_file)
        self.number_image_for_gif += 1

    def save_gif(self, full_path_to_file,
                 name_saved_photo):
        frames = []

        # print(os.listdir(full_path_to_file))
        for num_frame in range(self.number_image_for_gif):
            cur_full_path_to_file = full_path_to_file + '/' + f'{name_saved_photo}_{num_frame}.jpeg'
            frame = Image.open(cur_full_path_to_file)
            frames.append(frame)

        frames[0].save(
            f"{full_path_to_file}/../{name_saved_photo}.gif",
            save_all=True,
            append_images=frames[1:],  # Срез который игнорирует первый кадр.
            optimize=True,
            duration=200,
            loop=0
        )

        self.clear_dir(full_path_to_file=full_path_to_file)

    def stop_show(self):
        pygame.quit()

    def quick_save_image(self, **kwargs):
        self.show_finaly_algo(**kwargs)
        self.save_image(**kwargs)
        self.stop_show()

    def get_distance_to_goal(self):
        return ((self.s_goal[0] - self.new_position[0]) ** 2 + (self.s_goal[1] - self.new_position[1]) ** 2) ** 0.5

    def set_timer(self):
        """in second"""
        self.last_time_set_timer = time.time()

    def get_timer(self, reloud=False):
        """return: in milliseconds"""
        time_sec = time.time() - self.last_time_set_timer
        if reloud:
            self.set_timer()
        return time_sec * 1000

    def run_with_gui(self, delay_for_every_step=50,
                     **kwargs):
        is_doing_gif = False
        if "path_saved_photo" in kwargs:
            is_doing_gif = True
            self.number_image_for_gif = 0

        self.restart_all(launch_gui=True,
                         delay_for_every_step=delay_for_every_step,
                         **kwargs)
        stat = Statistic()
        stat.Trajectory_length = 0
        #
        stat.distribution_Trajectory_length_per_search = []
        stat.Trajectory_length_per_search = None
        last_time_saw_new_obstacle = 0
        #
        stat.Searchesc = 0
        #
        stat.Cell_expansions = 0
        self.dstar.Cell_expansions = 0

        #
        stat.Search_time = 0
        stat.Search_time_per_search = None
        stat.distribution_Search_time_per_search = []

        while not self.gui.done:
            if self.gui.restart:
                self.restart_all()
                self.dstar.Cell_expansions = 0
                print("Restart map")

            self.new_position = self.gui.current

            new_observation = self.gui.observation
            self.new_map = self.gui.world

            if new_observation is not None:
                # old_map = self.new_map
                self.slam.set_ground_truth_map(gt_map=self.new_map)

            if self.gui.stop and \
                    self.last_position is None or \
                    self.new_position != self.last_position:
                self.last_position = self.new_position

                # slam
                new_edges_and_old_costs, slam_map = self.slam.rescan(global_position=self.new_position)

                self.dstar.new_edges_and_old_costs = new_edges_and_old_costs
                self.dstar.sensed_map = slam_map

                # move and compute path
                RUNNING_FLAG, path, g, rhs = self.dstar.move_and_replan(robot_position=self.new_position)
                # if RUNNING_FLAG == self.dstar.BUG_OF_LOOPING:
                #    print(f"RUNNING_FLAG={RUNNING_FLAG}")
                #    return None
                if RUNNING_FLAG == self.dstar.TIME_LIMIT:
                    print(f"RUNNING_FLAG={RUNNING_FLAG}")

                print(f"RUNNING_FLAG={RUNNING_FLAG}")

            # update the map
            # print(path)
            # drive gui
            self.gui.run_game(path=path, auto_play=True)

            if is_doing_gif:
                self.save_image_for_gif(full_path_to_file=kwargs["path_saved_photo"],
                                        name_saved_photo=kwargs["name_saved_photo"])

        if is_doing_gif:
            self.save_gif(full_path_to_file=kwargs["path_saved_photo"],
                          name_saved_photo=kwargs["name_saved_photo"])

    def run_without_gui(self) -> Statistic:
        self.restart_all()

        stat = Statistic()
        stat.Trajectory_length = 0
        #
        stat.distribution_Trajectory_length_per_search = []
        stat.Trajectory_length_per_search = None
        last_time_saw_new_obstacle = 0
        #
        stat.Searchesc = 0
        #
        stat.Cell_expansions = 0
        self.dstar.Cell_expansions = 0
        #
        stat.Search_time = 0
        stat.Search_time_per_search = None
        stat.distribution_Search_time_per_search = []
        self.set_timer()

        final_path = [self.new_position]
        if self.new_position == self.s_goal:
            print(f"Walking is finished in s_goal!")
            return stat

        while True:
            stat.Trajectory_length += 1

            # print(f"Do step №{stat.Trajectory_length}  (Trajectory_length={stat.Trajectory_length}) | Rest of way={self.get_distance_to_goal()}")

            # slam
            new_edges_and_old_costs, slam_map = self.slam.rescan(global_position=self.new_position)
            # score stats: distribution_Trajectory_length_per_search
            last_time_saw_new_obstacle += 1
            if len(new_edges_and_old_costs) > 0:
                stat.distribution_Trajectory_length_per_search.append(last_time_saw_new_obstacle)
                last_time_saw_new_obstacle = 0

                stat.Searchesc += 1

                stat.distribution_Search_time_per_search.append(self.get_timer(reloud=True))

            self.dstar.new_edges_and_old_costs = new_edges_and_old_costs
            self.dstar.sensed_map = slam_map
            # move and compute path
            RUNNING_FLAG, cur_path, g, rhs = self.dstar.move_and_replan(robot_position=self.new_position)
            if RUNNING_FLAG == self.dstar.TIME_LIMIT:
                # (22, 8), (23, 8), (22, 8), (23, 8) - path |  stay at couple poses
                # prob_l=0.7, prob=0.8, count_of_tests=10, offset=2 | 6 Test (0 .. 6, 7 .. 9)
                # (prob_l=0.7, prob=0.8, count_of_tests=10, offset=8)
                print(f"Walking is failed by TIME_LIMIT!")

                # print(f"RUNNING_FLAG={RUNNING_FLAG} | path={cur_path}")
                return Statistic()
            if RUNNING_FLAG == self.dstar.NOT_FIND_PATH:
                print(f"Walking is failed by NOT_FIND_PATH!")
                return Statistic()

            # print(f"Find len path = {len(cur_path)}. path[1]={cur_path[1]}")

            self.new_position = cur_path[1]

            final_path.append(self.new_position)

            if self.new_position == self.s_goal:
                print(f"Walking is finished in s_goal!")
                break

        # self.quick_save_image(name_file='quick_save')
        # print(f"Final_path={final_path}")

        stat.distribution_Trajectory_length_per_search = np.array(stat.distribution_Trajectory_length_per_search)
        stat.Trajectory_length_per_search = stat.distribution_Trajectory_length_per_search.mean()
        stat.Cell_expansions = self.dstar.Cell_expansions

        stat.distribution_Search_time_per_search = np.array(stat.distribution_Search_time_per_search)
        stat.Search_time_per_search = stat.distribution_Search_time_per_search.mean()
        stat.Search_time = stat.distribution_Search_time_per_search.sum()

        return stat

    def run_test(self, sample_test: SampleTest,
                 gui: bool = False,
                 delay_for_every_step=50,
                 **kwargs) -> Statistic:
        self.load_start_goal(sample_test.start,
                             sample_test.goal)
        # maybe don`t need change ogrid
        if self.label_map is None or sample_test.label is None or \
                not self.label_map == sample_test.label:
            self.load_map_ogrid(OccupancyGridMap.covert_list2d_to_ogrid(sample_test.cells, **kwargs))
        if 'view_range' in kwargs:
            self.load_view_range(kwargs['view_range'])
        if 'exploration_setting' in kwargs:
            pass
        if 'dist_func' in kwargs:
            self.load_dist_func(dist_func=kwargs['dist_func'])
        if 'heuristic' in kwargs:
            self.load_heuristic(heuristic=kwargs['heuristic'])

        self.create_dstar()

        print(f"run_test: {self.dstar} | {self.slam}")

        if not gui:
            stat = self.run_without_gui()
            # get Optimal_length from movingAi otherwise None
            stat.Optimal_length = sample_test.Optimal_length

            return stat
        else:
            self.run_with_gui(delay_for_every_step=delay_for_every_step,
                              **kwargs)

            print("Finish work GUI")
            exit()

            return None

    @classmethod
    def get_simple_map(cls, num_map=0):
        cells = ReadMapsInfo.read_map_from_string(*SIMPLE_MAPS[num_map])
        return cells

    @classmethod
    def get_simple_scene(cls, num_scene=0):
        scene = SIMPLE_SCENES[num_scene]
        return scene

    @classmethod
    def get_simple_test(cls, num_scene=0, num_map=0):
        cells = cls.get_simple_map(num_map=num_map)
        scene = cls.get_simple_scene(num_scene=num_scene)
        sample_test = SampleTest(cells, scene.start, scene.goal)
        return sample_test

    def create_search_func(self, **kargs) -> Callable[[SampleTest], Statistic]:
        def search_func(sample_test: SampleTest) -> Statistic:
            stat = self.run_test(sample_test, **kargs)
            return stat

        return search_func

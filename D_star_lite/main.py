from gui import Animation
from d_star_lite import DStarLite
from grid import OccupancyGridMap, SLAM
from D_start_lite.data.py_data.simple_maps import SIMPLE_MAPS

OBSTACLE = 255
UNOCCUPIED = 0

if __name__ == '__main__':

    """
    set initial values for the map occupancy grid
    |----------> y, column
    |           (x=0,y=2)
    |
    V (x=2, y=0)
    x, row
    """
    y_size = 50
    x_size = 70

    #start = (10, 2)
    start = (8, 24)
    goal = (0, 1)
    view_range = 3

    """gui = Animation(title="D* Lite Path Planning",
                    width=10,
                    height=10,
                    margin=0,
                    y_size=y_size,
                    x_size=x_size,
                    start=start,
                    goal=goal,
                    viewing_range=view_range)"""


    ogdrid = OccupancyGridMap.read_from_string(*SIMPLE_MAPS[0])

    gui = Animation(title="D* Lite Path Planning",
                    ogdrid=ogdrid,
                    viewing_range=view_range,
                    start=start,
                    goal=goal)

    new_map = gui.world
    old_map = new_map



    # D* Lite (optimized)
    dstar = DStarLite(map=new_map,
                      s_start=gui.start,
                      s_goal=gui.goal)

    # SLAM to detect vertices
    slam = SLAM(map=new_map,
                view_range=view_range)

    new_position = gui.start
    last_position = None

    while not gui.done:
        if gui.restart:
            dstar.restart_d_star()
            slam.restart_slam()
            gui.restart_gui()

            new_position = gui.start
            last_position = None

            gui.restart = False

            print("Restart map")


        new_position = gui.current


        new_observation = gui.observation
        new_map = gui.world


        if new_observation is not None:
            old_map = new_map
            slam.set_ground_truth_map(gt_map=new_map)

        if gui.stop and \
                last_position is None or \
                new_position != last_position:

            last_position = new_position

            # slam
            new_edges_and_old_costs, slam_map = slam.rescan(global_position=new_position)

            dstar.new_edges_and_old_costs = new_edges_and_old_costs
            dstar.sensed_map = slam_map

            # move and compute path
            path, g, rhs = dstar.move_and_replan(robot_position=new_position)

        # update the map
        # print(path)
        # drive gui
        gui.run_game(path=path, auto_play=True)



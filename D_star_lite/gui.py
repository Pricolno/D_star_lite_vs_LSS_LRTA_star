import pygame
from grid import OccupancyGridMap
from grid_color import GridColor
from win32api import GetSystemMetrics

# Define some colors
BLACK = (0, 0, 0)  # BLACK
UNOCCUPIED = (255, 255, 255)  # WHITE
GOAL = (0, 255, 0)  # GREEN
START = (255, 0, 0)  # RED
GRAY1 = (145, 145, 102)  # GRAY1
OBSTACLE = (77, 77, 51)  # GRAY2
LOCAL_GRID = (0, 0, 80)  # BLUE

LOW_BRIGHT = -100

colors = {
    0: UNOCCUPIED,
    1: GOAL,
    255: OBSTACLE
}

class Animation:
    @classmethod
    def get_now_time(cls):
        return pygame.time.get_ticks()

    def __init__(self,
                 title="D* Lite Path Planning",
                 width=30,
                 height=30,
                 margin=0,
                 y_size=50,
                 x_size=100,
                 start=(10, 30),
                 goal=(40, 40),
                 viewing_range=3,
                 ogdrid=None,
                 delay_for_every_step=50
                 ):
        self.time_last_action = None
        # milliseconds
        # self.delay_for_every_step = 500
        self.delay_for_every_step = delay_for_every_step

        self.time_last_action = self.get_now_time()
        self.cont = None
        self.restart = False
        self.stop = False
        self.margin = margin

        if ogdrid is not None:
            self.y_size = ogdrid.y_size
            self.x_size = ogdrid.x_size
        else:
            self.y_size = y_size
            self.x_size = x_size

        self.start = start
        self.current = start

        self.observation = {"pos": None, "type": None}
        self.goal = goal

        self.viewing_range = viewing_range
        pygame.init()

        # Set the 'width' and 'height' of the screen
        self.max_height = GetSystemMetrics(1) - 100
        self.max_width = GetSystemMetrics(0) - 100
        self.width = width
        self.height = height

        window_size = []
        for (height_, width_) in [(self.height, self.width),
                                  (6, 6),
                                  (3, 3),
                                  (2, 2),
                                  (1, 1)]:
            self.width = width_
            self.height = height_

            window_size = [(self.width + self.margin) * self.x_size + self.margin,
                           (self.height + self.margin) * self.y_size + self.margin]

            #print(f"height={self.height} width={self.width} | window_size={window_size[1], window_size[0]}  max_height={self.max_height} max_width={self.max_width}")


            if window_size[0] < self.max_width and window_size[1] < self.max_height:
                break

        #print(f"height={self.height} width={self.width} | window_size={window_size[1], window_size[0]}")
        self.screen = pygame.display.set_mode(window_size)

        # create occupancy grid map
        if ogdrid is not None:
            self.world = ogdrid
        else:
            self.world = OccupancyGridMap(y_size=y_size,
                                          x_size=x_size,
                                          exploration_setting='8N')

        # Set title of screen
        pygame.display.set_caption(title)

        # set font
        pygame.font.SysFont('Comic Sans MS', 36)

        # Loop until the user clicks the close button
        self.done = False

        # used to manage how fast the screen updates
        self.clock = pygame.time.Clock()

    def restart_gui(self):
        self.world.clear_visited()
        self.current = self.start
        self.stop = False

    def get_position(self):
        return self.current

    def set_position(self, pos: (int, int)):
        self.current = pos

    def get_goal(self):
        return self.goal

    def set_goal(self, goal: (int, int)):
        self.goal = goal

    def set_start(self, start: (int, int)):
        self.start = start

    def window_to_grid(self, pixel: (int, int)) -> (int, int):
        (row, col) = pixel
        # change the x/y screen coordinates to grid coordinates
        y = row // (self.height + self.margin)
        x = col // (self.width + self.margin)
        return y, x

    def grid_to_window(self, grid_cell: (int, int), xy=False) -> (int, int):
        y, x = grid_cell
        pix_x = (self.margin + self.width) * x + self.margin
        pix_y = (self.margin + self.height) * y + self.margin
        if xy:
            return pix_x, pix_y
        else:
            return pix_y, pix_x

    def center_of_grid(self, row, col, xy=False):
        center_window = (round(row * (self.height + self.margin) + self.height / 2) + self.margin,
                         round(col * (self.width + self.margin) + self.width / 2) + self.margin)
        if xy:
            return center_window[1], center_window[0]
        else:
            return center_window

    def get_true_color(self, row, cow, color):
        new_color = color
        if self.world.visited[row][cow]:
            new_color = GridColor.fog_of_war(color)
        return new_color

    def draw_rect(self, row, col, color=None,
                  width_rec=None, height_rec=None,
                  brightness=True):
        if width_rec is None:
            width_rec = self.width
        if height_rec is None:
            height_rec = self.height
        if color is None:
            color = colors[self.world.occupancy_grid_map[row][col]]

        if brightness:
            color = self.get_true_color(row, col, color)

        pygame.draw.rect(self.screen, color,
                         [(self.margin + self.width) * col + self.margin,
                          (self.margin + self.height) * row + self.margin,
                          width_rec,
                          height_rec])

    def draw_viewing_range(self, row, col, color=None):
        if color is None:
            color = LOCAL_GRID

        robot_center = [*self.center_of_grid(row, col, xy=True)]
        pygame.draw.rect(self.screen, LOCAL_GRID,
                         [robot_center[0] - self.viewing_range * (self.height + self.margin),
                          robot_center[1] - self.viewing_range * (self.width + self.margin),
                          2 * self.viewing_range * (self.width + self.margin),
                          2 * self.viewing_range * (self.height + self.margin)], 2)

    def draw_circle(self, row, col, color=None, radius=None,
                    brightness=True):
        assert (color is not None)
        if brightness:
            color = self.get_true_color(row, col, color)

        if radius is None:
            radius = round(self.width / 2) - 2

        step_center = [*self.center_of_grid(row, col, xy=True)]

        pygame.draw.circle(self.screen, color, step_center, radius)

    def display_path(self, path=None, brightness=True):
        if path is not None:
            for step in path:
                # draw a moving robot, based on current coordinates
                radius = max((self.height - 10) // 2, 1)
                self.draw_circle(*step, START, brightness=brightness, radius=radius)

    def display_obs(self, observations=None):
        if observations is not None:
            for o in observations:
                self.draw_rect(*o)

    def display_all_map(self, path=None, brightness=True,
                        is_viewing_range=True):
        # set the screen background
        self.screen.fill(BLACK)

        # draw the grid
        for row in range(self.y_size):
            for column in range(self.x_size):
                # color the cells
                self.draw_rect(row, column, brightness=brightness)
        if path is not None:
            self.display_path(path=path, brightness=brightness)


        # fill in the goal cell with green
        self.draw_rect(*self.goal, color=GOAL, brightness=brightness)

        # draw a moving robot, based on current coordinates
        # draw robot position as red circle
        self.draw_circle(*self.current, color=START, brightness=brightness)

        if is_viewing_range:
            # draw robot local grid map (viewing range)
            self.draw_viewing_range(*self.current, color=LOCAL_GRID)


        # set game tick
        #self.clock.tick(20)
        self.clock.tick(5)

    def get_mouse_position_on_grid(self) -> (int, int):
        """
        return (y, x)
        """
        (col, row) = pygame.mouse.get_pos()
        y, x = self.window_to_grid((row, col))
        return y, x

    def assign_obstacle(self, grid_cell: (int, int)) -> bool:
        """
        return True if change (free -> closed)
        """
        if self.world.is_unoccupied(grid_cell):
            print(f"grid cell: {grid_cell}")
            self.world.set_obstacle(grid_cell)
            self.observation = {"pos": grid_cell, "type": UNOCCUPIED}
            return True
        return False

    def remove_obstacle(self, grid_cell: (int, int)) -> bool:
        """
        return True if change (closed -> free)
        """
        if not self.world.is_unoccupied(grid_cell):
            print(f"grid cell: {grid_cell}")
            self.world.remove_obstacle(grid_cell)
            self.observation = {"pos": grid_cell, "type": UNOCCUPIED}
            return True
        return False

    def update_time_last_walk(self):
        self.time_last_action = self.get_now_time()

    def is_time_for_walk(self):
        if self.get_now_time() - self.time_last_action >= self.delay_for_every_step:
            return True
        return False

    def is_finish(self, y, x):
        return (y, x) == self.goal

    def go_next_position_on_the_path(self, path):
        """
        return True if path if finded
        """
        if self.stop:
            return

        if path:

            (y, x) = path[1]
            self.set_position((y, x))
            self.update_time_last_walk()

            if self.is_finish(y, x):
                self.stop = True
                print(f"Walked in finish y={y}, x={x} and Stop")

            return True
        return False

    def run_game(self, path=None, auto_play=True):
        if self.cont is None:
            self.cont = auto_play

        if path is None:
            path = []

        # if self.restart:

        pygame_events = pygame.event.get()
        # print(f"pygame_events={pygame_events}")

        if len(pygame_events) > 0:
            for event in pygame_events:
                # print(f"DEBUG:pygame.event.get() {event}")
                if event.type == pygame.QUIT or \
                        (event.type == pygame.KEYDOWN and event.key == pygame.K_q):  # if user clicked close
                    print("quit")
                    self.done = True  # flag that we are done so we can exit loop

                elif event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE:
                    self.cont = not self.cont
                    if not self.cont:
                        print("Stop walking")
                    else:
                        print("Continue walking")

                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    # space bar pressed. call next action
                    self.go_next_position_on_the_path(path)
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    # Restart walking
                    self.restart = True
                # set obstacle by holding left-click
                elif pygame.mouse.get_pressed()[0]:
                    # set the location in the grid map
                    grid_cell = self.get_mouse_position_on_grid()
                    self.assign_obstacle(grid_cell)

                elif pygame.mouse.get_pressed()[2]:
                    # remove obstacle by holding right-click
                    grid_cell = self.get_mouse_position_on_grid()
                    self.remove_obstacle(grid_cell)
        else:
            if self.cont and self.is_time_for_walk():
                self.go_next_position_on_the_path(path)

        self.display_all_map(path=path)

        # go ahead and update screen with that we've drawn
        pygame.display.flip()

    # be 'idle' friendly. If you forget this, the program will hang on exit
    pygame.quit()

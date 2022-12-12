class Scene:
    def __init__(self, hard_lvl,
                 height, width,
                 start_j, start_i, goal_j, goal_i,
                 optimal_length):
        """
        scene help (dont work docstring :( )
        :param hard_lvl:
        :param height:
        :param width:
        :param start_j:
        :param start_i:
        :param goal_j:
        :param goal_i:
        :param optimal_length:
        :return: void
        """
        self.hard_lvl = hard_lvl
        self.height = height
        self.width = width
        self.start = start_j, start_i,
        self.goal = goal_j, goal_i,
        self.optimal_length = optimal_length

    def get_start_goal(self):
        return self.start, self.goal

    def get_height_widht(self):
        return self.height, self.width

    def __str__(self):
        str_scene = f"""Scene(start={self.start}, goal={self.goal})"""
        return str_scene

class GridColor:
    LOW_BRIGHT = -100

    @classmethod
    def set_brightnes1(cls, r: int, low_bright: int):
        r += low_bright
        if r < 0:
            r = 0
        if r > 255:
            r = 255
        return r

    @classmethod
    def set_brightness3(cls, color, brightness=None):
        if brightness is None:
            brightness = cls.LOW_BRIGHT
        new_color = [0, 0, 0]
        for i, cur_channel in enumerate(color):
            new_color[i] = GridColor.set_brightnes1(cur_channel, brightness)

        # print(f"new_color={new_color}")
        return new_color

    @classmethod
    def set_blueness3(cls, color, brightness=None):
        new_color = list(color)

        new_color[1] = max(new_color[1] - 150, 0)
        new_color[0] = max(new_color[0] - 200, 0)

        return new_color

    # change goal_func this place
    @classmethod
    def fog_of_war(cls, color):
        new_color = cls.set_brightness3(color)
        return new_color

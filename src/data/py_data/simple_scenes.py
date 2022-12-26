from src.data.scene import Scene

from src.data.py_data.simple_maps import height1, width1

scene_0 = Scene(
    hard_lvl=0,
    height=height1, width=width1,
    start_i=0, start_j=0,
    goal_i=2, goal_j=2,
    optimal_length=-1
)


scene1 = Scene(
    hard_lvl=1,
    height=height1, width=width1,
    start_i=0, start_j=0,
    #goal_i=width1 - 3, goal_j=height1 - 3,
    goal_i=height1 - 3, goal_j=width1 - 3,
    optimal_length=-1
)

scene2 = Scene(
    hard_lvl=1,
    height=height1, width=width1,
    start_i=2, start_j=29,
    goal_i=6, goal_j=2,
    optimal_length=-1
)


SIMPLE_SCENES = [scene_0, scene1, scene2]

if __name__ == "__main__":
    print(SIMPLE_SCENES[0])
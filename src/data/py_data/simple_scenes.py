from D_star_lite_vs_LSS_RTA_star.src.data.scene import Scene

from D_star_lite_vs_LSS_RTA_star.src.data.py_data.simple_maps import height1, width1

scene_0 = Scene(
    0,
    height1, width1,
    0, 0,
    2, 2,
    -1
)


scene1 = Scene(1,
               height1, width1,
               0, 0,
               height1 - 1, width1 - 1,
               -1
               )

SIMPLE_SCENES = [scene_0, scene1]

if __name__ == "__main__":
    print(SIMPLE_SCENES[0])
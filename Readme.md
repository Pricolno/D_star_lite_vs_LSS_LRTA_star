# D* lite vs LSS-LRTA*

## Incremental algorithm for path planning in a dynamic environment

### D* lite


The D* Lite algorithm was developed by Sven Koenig and Maxim Likhachev for a faster and easier alternative to the D* algorithm (developed by Anthony Stentz in 1995).  

Here is an implementation of D\*Lite as provided in the article in [Koenig, 2002](http://idm-lab.org/bib/abstracts/papers/aaai02b.pdf)


![](docs/D_star_lite_simple_deadlock.gif)

#### Main ideas
1. Сhange the direction of the search: now look for the path from goal to (current) start. If a change in edge cost is detected during traversal (around the current robot pose), only few nodes near the goal (=start) need to be updated.

2. Nodes that need to be updated, or the distance to them has changed, or was not calculated before. Then, it is clear that they must be updated in any case.  

3. Incremental heuristic search algorithms: able to focus and build upon previous solutions


#### Pseudo code, D* Lite optimized version
![](docs/pseudocode_DLite_star.png)


### LSS-LRTA*

The LSS-LRTA* is similar to the D*, but with a limitation to local processing (*lookahead*).
The current implementation was inspired as provided in the article in [S. Koenig, X. Sun, 2008](https://link.springer.com/content/pdf/10.1007/s10458-008-9061-x.pdf).

![](docs/LSS-LRTA_star_simple_deadlock.gif)

#### Main ideas
1. Use A* [13, 12] to search from the current state of agent toward the goal state until *lookahead* > 0 states have been  expanded or the goal state is about to be expanded. The states expanded by A* form the local search space.
2. Use Dijkstra's algorithm [8] to replace the h-values of all states in the local search space with the sum of the distance from the state to a state *s* and the *h-value* of state *s*, minimazed over all states *s* from *S* that border the local search space.
3. Move the agent along the path found by A* until it reaches the end of the path (and leaves the local search space) or action cost on the path increase.
4. If the current state of the agent is different from the goal state, then go to *Step 1*, oherwise terminate successfully.


#### Pseudo code, LSS-LRTA*

![](docs/pseudocode_LSS_LRTA.png)


### D* lite | implementation

#### Dependencies

* pygame
* numpy
* win32api
* sortedcontainers
* PIL

#### quick run (need file `D_star_lite_vs_LSS_LRTA_star/src/D_star_lite/quick_start_Dlite_star.py`)

```
cd D_star_lite_vs_LSS_LRTA_star/src/D_star_lite
python3 quick_start_Dlite_star.py

```

* change map:
`cur_cells = read_maps_info.get_simple_map()` <br>
`cur_cells : List[List[{0, 1}]]` - 1 obstacle, 0 empty cell

* change scen (start, goal)
example create be in `D_star_lite_vs_LSS_LRTA_star/src/data/simple_scenes.py` <br>
`class Scene` be in (`D_star_lite_vs_LSS_LRTA_star/src/data/scene.py`) <br>

example create Scene:
```
scene2 = Scene(
    hard_lvl=1,
    height=height_map, width=width_map,
    start_i=2, start_j=29,
    goal_i=6, goal_j=2,
    optimal_length=27
)
```

```list_scenes = read_maps_info.get_simple_scene(is_list=True, num_scene=2)```<br>
for custom scene need to set like this: <br>
```list_scenes = [scene_big, scene_medium, scene_small]```


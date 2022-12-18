from src.Dijkstra.run_dijkstra import RunDijkstra
from src.Dijkstra.dijkstra import Dijkstra


if __name__ == "__main__":
    cells = [[0, 0, 0],
             [0, 1, 0],
             [1, 0, 0]]

    start = (0, 0)
    goal = (2, 2)

    # dijkstra = Dijkstra()
    # dijkstra.load_map_cells(cells)
    # dijkstra.load_map_start_goal(start, goal)
    # path, length = dijkstra.run_dijkstra()
    # print(path, length)

    run_dj = RunDijkstra()
    run_dj.load_map_cells(cells)
    run_dj.load_map_start_goal(start, goal)

    length = run_dj.run_dijkstra()
    print(length)

class Map:
    def __init__(self, view_range=None):
        """
        Default constructor
        """
        self._view_range = view_range
        self._upgraded_h = dict()
        self._width = 0
        self._height = 0
        self._cells = []
        self._vcells = []

    def read_from_string(self, cell_str, width, height):
        """
        Converting a string (with '#' representing obstacles and '.' representing free cells) to a grid
        """
        self._width = width
        self._height = height
        self._cells = [[0 for _ in range(width)] for _ in range(height)]
        self._vcells = [[0 for _ in range(width)] for _ in range(height)]
        cell_lines = cell_str.split("\n")
        i = 0
        j = 0
        for l in cell_lines:
            if len(l) != 0:
                j = 0
                for c in l:
                    if c == '.':
                        self._cells[i][j] = 0
                    elif c == '#' or c == '@' or c == 'T':
                        self._cells[i][j] = 1
                    else:
                        continue
                    j += 1
                if j != width:
                    raise Exception("Size Error. Map width = ", j, ", but must be", width)

                i += 1

        if i != height:
            raise Exception("Size Error. Map height = ", i, ", but must be", height)

    def read_from_cells(self, cells):
        self._width, self._height = len(cells[0]), len(cells)
        self._cells = cells
        self._vcells = [[0 for _ in range(self._width)]
                        for _ in range(self._height)]

    def read_from_file(self, file_name, width, height):
        self._width = width
        self._height = height
        self._cells = [[0 for _ in range(width)] for _ in range(height)]
        self._vcells = [[0 for _ in range(width)] for _ in range(height)]
        with open(file_name, 'r') as file:
            i = 0
            j = 0
            for row in file.readlines():
                # data.append(list(map(int, row.strip().split())))
                # cell_lines = cell_str.split("\n")
                if len(row) != 0:
                    j = 0
                    for c in row:
                        if c == '.':
                            self._cells[i][j] = 0
                        elif c == '#' or c == '@':
                            self._cells[i][j] = 1
                        else:
                            continue
                        j += 1
                    # if j != width:
                    #    raise Exception("Size Error. Map width = ", j, ", but must be", width)

                    i += 1

            # if i != height:
            #    raise Exception("Size Error. Map height = ", i, ", but must be", height)

    def set_grid_cells(self, width, height, grid_cells):
        """
        Initialization of map by list of cells.
        """
        self._width = width
        self._height = height
        self._cells = grid_cells

    def in_bounds(self, i, j):
        """
        Check if the cell is on a grid.
        """
        return (0 <= j < self._width) and (0 <= i < self._height)

    def traversable(self, i, j, by_origin=False):
        """
        Check if the cell is not an obstacle.
        """
        if self._view_range and not by_origin:
            return not self._vcells[i][j]
        else:
            return not self._cells[i][j]

    def get_neighbors(self, i, j):
        """
        Get a list of neighbouring cells as (i,j) tuples.
        """
        neighbors = []
        delta = [[0, 1], [1, 0], [0, -1], [-1, 0]]

        for d in delta:
            if self.in_bounds(i + d[0], j + d[1]) and self.traversable(i + d[0], j + d[1]):
                neighbors.append((i + d[0], j + d[1]))

        return neighbors

    def get_size(self):
        return self._height, self._width

    def set_local_observations(self, pi, pj):
        new_obs = []
        if not self._view_range:
            return new_obs
        for i in range(pi - self._view_range, pi + self._view_range + 1):
            for j in range(pj - self._view_range, pj + self._view_range + 1):
                if self.in_bounds(i, j):
                    if self._vcells[i][j] != self._cells[i][j]:
                        new_obs.append((i, j))
                    self._vcells[i][j] = self._cells[i][j]
        return new_obs

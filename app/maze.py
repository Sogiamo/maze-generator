from collections import deque

import numpy as np

DIRECTIONS = ((-1, 0), (0, -1), (1, 0), (0, 1))

class Maze:
    def __init__(self, shape):
        self.grid = np.zeros(shape=shape)
        self.height, self.width = shape
        self.start = (0, 0)
        self.end = (self.height - 1, self.width - 1)

        if self.height < 3 or self.width < 3:
            raise ValueError(f"Invalid shape:{shape}, width and height have to be at least 3")
    def __str__(self):
        print()
        EMPTY = ' '
        WALL = chr(9608)
        MARK = '@'

        for y in range(self.height):
            print_str = ''
            for x in range(self.width):
                if self.start == (x, y) or self.end == (x, y):
                    print_str += MARK
                elif self.grid[y, x] == 0:
                    print_str += WALL
                else:
                    print_str += EMPTY
            print(print_str)

    def add_bounds(self):
        self.grid = np.pad(self.grid, 1)
        self.height += 2
        self.width += 2
        self.start = (self.start[0] + 1, self.start[1] + 1)
        self.end = (self.end[0] + 1, self.end[1] + 1)

    def in_bounds(self, cell):
        row, col = cell
        return 0 <= row < self.height and 0 <= col < self.width

    def get_all_neighbours(self, cell):
        row, col = cell

        neighbours = ((row + d_row, col + d_col) for d_row, d_col in DIRECTIONS)

        return [neighbour for neighbour in neighbours if self.in_bounds(neighbour)]

    def get_walkable_neighbours(self, cell):
        neighbours = self.get_all_neighbours(cell)

        return [neighbour for neighbour in neighbours if self.is_walkable(neighbour)]

    def get_expandable_neighbours(self, cell):
        all_neighbours = self.get_all_neighbours(cell)

        expandable_neighbours = []
        for neighbour in all_neighbours:
            walkable_neighbours = self.get_walkable_neighbours(neighbour)
            if len(walkable_neighbours) <= 1 and not self.is_walkable(neighbour):
                expandable_neighbours.append(neighbour)

        return expandable_neighbours

    def is_path(self):
        queue = deque()

        current = self.start
        visited = {current}
        queue.append(current)

        while len(queue) > 0:
            current = queue.popleft()
            if current == self.end:
                return True
            current_neighbours = self.get_walkable_neighbours(current)
            for neighbour in current_neighbours:
                if neighbour not in visited:
                    queue.append(neighbour)
                    visited.add(neighbour)

        return False

    def is_walkable(self, cell):
        return self.grid[cell] == 1

    def set_walkable(self, cell):
        self.grid[cell] = 1

    def set_wall(self, cell):
        self.grid[cell] = 0

    def set_start(self, cell):
        self.start = cell

    def set_end(self, cell):
        self.end = cell

    def get_start(self):
        return self.start

    def get_end(self):
        return self.end
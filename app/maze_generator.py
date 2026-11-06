import numpy as np

from maze import Maze

MAX_ATTEMPTS = 1000

class MazeGenerator:
    def __init__(self, shape, seed, max_attempts = MAX_ATTEMPTS):
        self.shape = shape
        self.seed = seed
        self.max_attempts = MAX_ATTEMPTS

    def set_seed(self, seed):
        self.seed = seed

    def generate_maze(self):
        # 0 - wall, 1 - walkable
        np.random.seed(self.seed)

        for _ in range(self.max_attempts):
            maze = Maze(self.shape)
            candidates = [maze.get_start()]
            while len(candidates) > 0:
                current = candidates[np.random.choice(len(candidates))]
                candidates.remove(current)
                if maze.is_walkable(current) or len(maze.get_walkable_neighbours(current)) > 1:
                    continue
                maze.set_walkable(current)
                all_expandable_neighbours = maze.get_expandable_neighbours(current)
                candidates.extend(all_expandable_neighbours)

            if maze.is_walkable(maze.get_end()):
                return maze

        raise RuntimeError(
            f"No maze of shape {self.shape} reached the end after "
            f"{self.max_attempts} attempts; try another seed or size"
        )











def main():
    mazeGenerator = MazeGenerator((120, 120), 42)
    maze = mazeGenerator.generate_maze()
    maze.add_bounds()
    maze.plot_maze((22, 20))
if __name__ == '__main__':
    main()






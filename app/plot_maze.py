from matplotlib.colors import ListedColormap, BoundaryNorm

def draw_maze(maze, ax, start_end_visible = True):
    maze_copy = maze.grid.copy()
    if start_end_visible:
        maze_copy[maze.start] = 2
        maze_copy[maze.end] = 3

    cmap = ListedColormap(["black", "grey", "green", "red"])
    norm = BoundaryNorm([-0.5, 0.5, 1.5, 2.5, 3.5], cmap.N)

    ax.imshow(maze_copy, cmap=cmap, norm=norm)
    ax.set_title("Maze")
    ax.axis("off")
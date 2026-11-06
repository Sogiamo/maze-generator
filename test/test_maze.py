import pytest

from app.maze import Maze

def test_maze_init():
    maze = Maze((5, 5))
    maze.print_maze()

    maze.set_start((2, 1))
    maze.set_end((4, 3))

    maze.print_maze()

def test_maze_get_neighbours():
    maze = Maze((5, 5))

    cell1 = (0, 0)
    neighbours = maze.get_all_neighbours(cell1)

    assert set(neighbours) == {(0, 1), (1, 0)}

    cell2 = (5, 5)
    neighbours = maze.get_all_neighbours(cell2)

    assert set(neighbours) == {(4, 5), (5, 4)}

    cell3 = (3, 3)
    neighbours = maze.get_all_neighbours(cell3)

    assert set(neighbours) == {(2, 3), (3, 2), (4, 3), (3, 4)}

def test_maze_get_walkable_neighbours():
    maze = Maze((5, 5))

    cell1 = (0, 0)
    neighbours = maze.get_walkable_neighbours(cell1)

    assert set(neighbours) == set()

    walkable = [(2, 3), (3, 2), (4, 3), (3, 4), (3, 3)]
    for cell in walkable:
        maze.set_walkable(cell)

    cell2 = (3, 3)
    neighbours = maze.get_walkable_neighbours(cell2)

    assert set(neighbours) == {(2, 3), (3, 2), (4, 3), (3, 4)}

    walkable = [(0, 0), (0, 2)]
    for cell in walkable:
        maze.set_walkable(cell)

    cell3 = (0, 1)
    neighbours = maze.get_walkable_neighbours(cell3)

    assert set(neighbours) == {(0, 0), (0, 2)}

def test_set_walkable():
    maze = Maze((5, 5))
    maze.set_walkable((0, 0))
    assert maze.maze[0, 0] == 1

def test_set_wall():
    maze = Maze((5, 5))
    cell = (0, 0)
    maze.set_walkable(cell)
    assert maze.maze[cell] == 1
    maze.set_wall(cell)
    assert maze.maze[cell] == 0


def test_maze_is_path_true():
    maze = Maze((3, 3))
    maze.set_start((0, 0))
    maze.set_end((2, 2))

    path = [(0, 0), (0, 1), (0, 2), (1, 2), (2, 2)]
    for cell in path:
        maze.set_walkable(cell)

    assert maze.is_path() == True


def test_maze_is_path_false():
    maze = Maze((3, 3))
    maze.set_start((0, 0))
    maze.set_end((2, 2))

    path = [(0, 0), (1, 1), (2, 2)]
    for cell in path:
        maze.set_walkable(cell)

    assert maze.is_path() == False



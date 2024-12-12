from enum import IntEnum


grid = None
num_rows = None
num_columns = None
current_position = None
current_heading = None

OBSTACLE = "#"
PATH = "X"

# this representation lets us turn to the right by adding 1 mod 4
class Heading(IntEnum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

def parse(lines):
    global num_rows, num_columns, grid, current_position, current_heading
    num_rows = len(lines)
    num_columns = len(lines[0].strip())
    grid = [[None for _ in range(num_columns)] for _ in range(num_rows)]

    for i in range(num_rows):
        for j in range(num_columns):
            char = lines[i][j]
            if char == OBSTACLE:
                grid[i][j] = OBSTACLE
            elif char == "^":
                current_position = (i, j)
                current_heading = Heading.NORTH
                grid[i][j] = PATH
            elif char == ">":
                current_position = (i, j)
                current_heading = Heading.EAST
                grid[i][j] = PATH
            elif char == "<":
                current_position = (i, j)
                current_heading = Heading.WEST
                grid[i][j] = PATH
            elif char == "v":
                current_position = (i, j)
                current_heading = Heading.SOUTH
                grid[i][j] = PATH

def in_grid():
    y = current_position[0]
    x = current_position[1]
    return y >= 0 and y < num_columns and x >= 0 and x < num_rows

def rotate():
    global current_heading
    current_heading = (current_heading + 1) % 4

def route():
    global grid, current_position, current_heading
    while in_grid():
        y = current_position[0]
        x = current_position[1]
        grid[y][x] = PATH
        match current_heading:
            case Heading.NORTH:
                if y > 0 and grid[y-1][x] == OBSTACLE:
                    rotate()
                else:
                    current_position = (y - 1, x)
            case Heading.EAST:
                if x < num_rows - 1 and grid[y][x+1] == OBSTACLE:
                    rotate()
                else:
                    current_position = (y, x + 1)
            case Heading.SOUTH:
                if y < num_columns - 1 and grid[y+1][x] == OBSTACLE:
                    rotate()
                else:
                    current_position = (y + 1, x)
            case Heading.WEST:
                if x > 0 and grid[y][x-1] == OBSTACLE:
                    rotate()
                else:
                    current_position = (y, x - 1)

def positions_in_path():
    return len([tile for row in grid for tile in row if tile == PATH])

with open("day6/input.txt", "r") as f:
    lines = f.readlines()
    parse(lines)
    route()
    print(positions_in_path())

import copy
from enum import IntEnum
import itertools


base_map = None
num_rows = None
num_columns = None
initial_position = None
initial_heading = None

OBSTACLE = "#"
PATH = "X"
NORTH = "N"
SOUTH = "S"
EAST = "E"
WEST = "W"

# this representation lets us turn to the right by adding 1 mod 4
class Heading(IntEnum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

def parse(lines):
    global num_rows, num_columns, base_map, initial_position, initial_heading
    num_rows = len(lines)
    num_columns = len(lines[0].strip())
    base_map = [["." for _ in range(num_columns)] for _ in range(num_rows)]

    for i in range(num_rows):
        for j in range(num_columns):
            char = lines[i][j]
            if char == OBSTACLE:
                base_map[i][j] = OBSTACLE
            elif char == "^":
                initial_position = (i, j)
                initial_heading = Heading.NORTH
                # base_map[i][j] = NORTH
            elif char == ">":
                initial_position = (i, j)
                initial_heading = Heading.EAST
                # base_map[i][j] = EAST
            elif char == "<":
                initial_position = (i, j)
                initial_heading = Heading.WEST
                # base_map[i][j] = WEST
            elif char == "v":
                initial_position = (i, j)
                initial_heading = Heading.SOUTH
                # base_map[i][j] = SOUTH

def in_grid(position):
    y = position[0]
    x = position[1]
    return y >= 0 and y < num_columns and x >= 0 and x < num_rows

def rotate(heading):
    return (heading + 1) % 4

# this could be optimized by immediately jumping ahead to the next obstacle
def has_loop(map):
    position = initial_position
    heading = initial_heading
    while in_grid(position):
        y = position[0]
        x = position[1]
        match heading:
            case Heading.NORTH:
                if map[y][x] == NORTH:
                    return True
                elif y > 0 and map[y-1][x] == OBSTACLE:
                    heading = rotate(heading)
                else:
                    map[y][x] = NORTH
                    position = (y - 1, x)
            case Heading.EAST:
                if map[y][x] == EAST:
                    return True
                elif x < num_rows - 1 and map[y][x+1] == OBSTACLE:
                    heading = rotate(heading)
                else:
                    map[y][x] = EAST
                    position = (y, x + 1)
            case Heading.SOUTH:
                if map[y][x] == SOUTH:
                    return True
                elif y < num_columns - 1 and map[y+1][x] == OBSTACLE:
                    heading = rotate(heading)
                else:
                    map[y][x] = SOUTH
                    position = (y + 1, x)
            case Heading.WEST:
                if map[y][x] == WEST:
                    return True
                elif x > 0 and map[y][x-1] == OBSTACLE:
                    heading = rotate(heading)
                else:
                    map[y][x] = WEST
                    position = (y, x - 1)
    return False

def map_with_obstacle_at(y, x):
    global base_map
    map = copy.deepcopy(base_map)
    map[y][x] = OBSTACLE
    return map

def num_positions():
    global base_map
    # we can optimize this a bit by only considering positions off by one from being in line with existing obstacles
    # currently this is very slow!
    # could also parallelize
    result = [(y, x) for y, x in itertools.product(range(num_rows), range(num_columns)) if has_loop(map_with_obstacle_at(y, x)) and base_map[y][x] not in [NORTH, SOUTH, EAST, WEST, OBSTACLE]]
    return len(result)

with open("day6/input.txt", "r") as f:
    lines = f.readlines()
    parse(lines)
    print(num_positions())

from scipy import stats
import numpy as np

XSIZE = 101
YSIZE = 103
NUM_ITERATIONS = 100

class Robot:
    def __init__(self, position, velocity):
        self.position = position
        self.velocity = velocity

class Floor:
    def __init__(self, robots, xsize, ysize):
        self.robots = robots
        self.xsize = xsize
        self.ysize = ysize

def x(tup):
    return tup[0]

def y(tup):
    return tup[1]

def parse(lines):
    robots = []
    for line in lines:
        p_v = line.split()
        position = list(map(int, p_v[0].strip("p=").split(",")))
        velocity = list(map(int, p_v[1].strip("v=").split(",")))
        robots.append(Robot((position[0], position[1]), (velocity[0], velocity[1])))
    return Floor(robots, XSIZE, YSIZE)

def move(floor):
    robots = floor.robots
    variances = set()
    for i in range(1, 10000):
        new_robots = []
        for robot in robots:
            new_x = (x(robot.position) + x(robot.velocity)) % floor.xsize
            new_y = (y(robot.position) + y(robot.velocity)) % floor.ysize
            new_robots.append(Robot((new_x, new_y), robot.velocity))
        robots = new_robots
        x_variance = np.var(list(map(lambda robot: x(robot.position), robots)))
        y_variance = np.var(list(map(lambda robot: y(robot.position), robots)))
        variance = x_variance * y_variance
        variances.add((i, variance))
        if i == 7603:
            visualize(Floor(robots, floor.xsize, floor.ysize))
    min_variance = min(variances, key=lambda x: x[1])
    return min_variance[0]

def visualize(floor):
    for i in range(floor.ysize):
        for j in range(floor.xsize):
            num = len(list(filter(lambda robot: x(robot.position) == j and y(robot.position) == i, floor.robots)))
            if num > 0:
                print(num, end="")
            else:
                print(".", end="")
        print()
    print()

with open("day14/input.txt", "r") as f:
    lines = f.readlines()
    floor = parse(lines)
    tree = move(floor)
    print(tree)

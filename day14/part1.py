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

def move(floor, num_iterations):
    robots = floor.robots
    new_robots = []
    for robot in robots:
        new_x = (x(robot.position) + num_iterations * x(robot.velocity)) % floor.xsize
        new_y = (y(robot.position) + num_iterations * y(robot.velocity)) % floor.ysize
        new_robots.append(Robot((new_x, new_y), robot.velocity))
    return Floor(new_robots, floor.xsize, floor.ysize)

def safety_factor(floor):
    xmiddle = floor.xsize // 2
    ymiddle = floor.ysize // 2
    top_left = len(list(filter(lambda robot: x(robot.position) < xmiddle and y(robot.position) < ymiddle, floor.robots)))
    top_right = len(list(filter(lambda robot: x(robot.position) > xmiddle and y(robot.position) < ymiddle, floor.robots)))
    bottom_left = len(list(filter(lambda robot: x(robot.position) < xmiddle and y(robot.position) > ymiddle, floor.robots)))
    bottom_right = len(list(filter(lambda robot: x(robot.position) > xmiddle and y(robot.position) > ymiddle, floor.robots)))
    return top_left * top_right * bottom_left * bottom_right

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
    after = move(floor, NUM_ITERATIONS)
    factor = safety_factor(after)
    print(factor)

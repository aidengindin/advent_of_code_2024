class Warehouse:
    def __init__(self, walls, boxes, robot_position, moves):
        self.walls = walls
        self.boxes = boxes
        self.robot_position = robot_position
        self.moves = moves

def parse(lines: list[str]) -> Warehouse:
    walls = set()
    boxes = set()
    robot_position = None
    map_lines = list(map(lambda line: line.strip(), filter(lambda line: line[0] == "#", lines)))
    move_lines = list(map(lambda line: line.strip(), filter(lambda line: line[0] in ["<", ">", "^", "v"], lines)))
    for i in range(len(map_lines)):
        for j in range(len(map_lines[0])):
            char = map_lines[i][j]
            position = (j * 2, i)
            next_position = (j * 2 + 1, i)
            if char == "#":
                walls.add(position)
                walls.add(next_position)
            elif char == "O":
                boxes.add((position, next_position))
            elif char == "@":
                robot_position = position
    moves = [char for line in move_lines for char in line]
    return Warehouse(walls, boxes, robot_position, moves)

def x(position: tuple[int, int]) -> int:
    return position[0]

def y(position: tuple[int, int]) -> int:
    return position[1]

# helper functions for getting the left or right tile of a box
# logically same as x/y but should have distinct names
left = x
right = y

def boxes_in_line(robot_position, direction, boxes):
    if direction == "<":
        return helper(x, y, -1, lambda x, y: x < y, lambda box: ((x(left(box)) - 1, y(left(box))), (x(right(box)) - 1, y(right(box)))), robot_position, boxes)
    elif direction == ">":
        return helper(x, y, 1, lambda x, y: x > y, lambda box: ((x(left(box)) + 1, y(left(box))), (x(right(box)) + 1, y(right(box)))), robot_position, boxes)
    elif direction == "^":
        return helper(y, x, -1, lambda x, y: x < y, lambda box: ((x(left(box)), y(left(box)) - 1), (x(right(box)), y(right(box)) - 1)), robot_position, boxes)
    elif direction == "v":
        return helper(y, x, 1, lambda x, y: x > y, lambda box: ((x(left(box)), y(left(box)) + 1), (x(right(box)), y(right(box)) + 1)), robot_position, boxes)

# this function could use some serious cleanup, not to mention some optimizations...
def helper(comparison_axis, same_axis, direction, comparison, next_position_mapper, robot_position, boxes):
    next_boxes = set(filter(lambda box: any(map(lambda tile: same_axis(tile) == same_axis(robot_position) and comparison_axis(tile) - comparison_axis(robot_position) == direction, [left(box), right(box)])), boxes))
    pushed_boxes = set()
    while len(next_boxes) > 0:
        current = next_boxes.pop()
        next_boxes.update(filter(lambda box: any(map(lambda tile: same_axis(tile) in map(same_axis, current) and any([comparison_axis(tile) - comparison_axis(current_tile) == direction for current_tile in [left(current), right(current)]]), [left(box), right(box)])) and box not in pushed_boxes, boxes))
        pushed_boxes.add(current)
    return {(box, next_position_mapper(box)) for box in pushed_boxes}

def move(warehouse: Warehouse) -> Warehouse:
    walls = warehouse.walls
    boxes = warehouse.boxes
    robot_position = warehouse.robot_position
    # print("Initial state:")
    # visualize(warehouse)
    for move in warehouse.moves:
        next_tile = None
        if move == "<":
            next_tile = (x(robot_position) - 1, y(robot_position))
        elif move == ">":
            next_tile = (x(robot_position) + 1, y(robot_position))
        elif move == "^":
            next_tile = (x(robot_position), y(robot_position) - 1)
        elif move == "v":
            next_tile = (x(robot_position), y(robot_position) + 1)
        moved_boxes = boxes_in_line(robot_position, move, boxes)
        box_hits_wall = any([tile in walls for box_info in moved_boxes for tile in box_info[1]])
        if not (next_tile in walls or box_hits_wall):
            robot_position = next_tile
            start_positions = [left(box) for box in moved_boxes]
            end_positions = [right(box) for box in moved_boxes]
            for position in start_positions:
                boxes.remove(position)
            for position in end_positions:
                boxes.add(position)
        # print("Move " + move + ":")
        # visualize(Warehouse(walls, boxes, robot_position, []))
    return Warehouse(walls, boxes, robot_position, [])

def gps_sum(warehouse: Warehouse) -> int:
    return sum(map(lambda box: x(left(box)) + 100 * y(left(box)), warehouse.boxes))

def visualize(warehouse: Warehouse) -> None:
    xsize = max(map(lambda wall: x(wall), warehouse.walls)) + 1
    ysize = max(map(lambda wall: y(wall), warehouse.walls)) + 1
    boxes_left = [left(box) for box in warehouse.boxes]
    boxes_right = [right(box) for box in warehouse.boxes]
    for i in range(ysize):
        for j in range(xsize):
            position = (j, i)
            if position in warehouse.walls:
                print("#", end="")
            elif position in boxes_left:
                print("[", end="")
            elif position in boxes_right:
                print("]", end="")
            elif position == warehouse.robot_position:
                print("@", end="")
            else:
                print(".", end="")
        print()
    print()

with open("day15/input.txt", "r") as f:
    lines = f.readlines()
    warehouse = parse(lines)
    after = move(warehouse)
    result = gps_sum(after)
    print(result)

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
            position = (j, i)
            if char == "#":
                walls.add(position)
            elif char == "O":
                boxes.add(position)
            elif char == "@":
                robot_position = position
    moves = [char for line in move_lines for char in line]
    return Warehouse(walls, boxes, robot_position, moves)

def x(position: tuple[int, int]) -> int:
    return position[0]

def y(position: tuple[int, int]) -> int:
    return position[1]

def boxes_in_line(robot_position, direction, boxes):
    filtered_boxes = set()
    box_next_tile = None
    if direction == "<":
        filtered_boxes, box_next_tile_delta = helper(x, y, -1, lambda x, y: x < y, min, robot_position, boxes)
        box_next_tile = (box_next_tile_delta, y(robot_position))
    elif direction == ">":
        filtered_boxes, box_next_tile_delta = helper(x, y, 1, lambda x, y: x > y, max, robot_position, boxes)
        box_next_tile = (box_next_tile_delta, y(robot_position))
    elif direction == "^":
        filtered_boxes, box_next_tile_delta = helper(y, x, -1, lambda x, y: x < y, min, robot_position, boxes)
        box_next_tile = (x(robot_position), box_next_tile_delta)
    elif direction == "v":
        filtered_boxes, box_next_tile_delta = helper(y, x, 1, lambda x, y: x > y, max, robot_position, boxes)
        box_next_tile = (x(robot_position), box_next_tile_delta)
    return filtered_boxes, box_next_tile

def helper(comparison_axis, same_axis, direction, comparison, ordering, robot_position, boxes):
    filtered_boxes = set()
    box_next_tile_delta = None
    potential = list(filter(lambda box: same_axis(box) == same_axis(robot_position) and comparison(comparison_axis(box), comparison_axis(robot_position)), boxes))
    potential.sort(key=lambda box: direction * comparison_axis(box))
    if len(potential) == 0 or comparison_axis(potential[0]) - direction != comparison_axis(robot_position):
        return filtered_boxes, box_next_tile_delta
    for i, box in enumerate(potential):
        if i > 0 and abs(comparison_axis(box) - comparison_axis(potential[i-1])) != 1:
            break
        filtered_boxes.add(box)
    if len(filtered_boxes) > 0:
        box_next_tile_delta = ordering(map(lambda box: comparison_axis(box), filtered_boxes)) + direction
    return filtered_boxes, box_next_tile_delta

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
        moved_boxes, box_next_tile = boxes_in_line(robot_position, move, boxes)
        is_box = len(moved_boxes) != 0
        if not (next_tile in walls or (is_box and box_next_tile in walls)):
            robot_position = next_tile
            if is_box:
                boxes.remove(next_tile)
                boxes.add(box_next_tile)
        # print("Move " + move + ":")
        # visualize(Warehouse(walls, boxes, robot_position, []))
    return Warehouse(walls, boxes, robot_position, [])

def gps_sum(warehouse: Warehouse) -> int:
    return sum(map(lambda box: x(box) + 100 * y(box), warehouse.boxes))

def visualize(warehouse: Warehouse) -> None:
    xsize = max(map(lambda wall: x(wall), warehouse.walls)) + 1
    ysize = max(map(lambda wall: y(wall), warehouse.walls)) + 1
    for i in range(ysize):
        for j in range(xsize):
            position = (j, i)
            if position in warehouse.walls:
                print("#", end="")
            elif position in warehouse.boxes:
                print("O", end="")
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

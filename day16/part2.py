from enum import IntEnum
import heapq


class Direction(IntEnum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

def parse(lines):
    start = None
    end = None
    tiles = set()
    lines = [line.strip() for line in lines]
    for i in range(len(lines)):
        line = lines[i]
        for j in range(len(line)):
            char = lines[i][j]
            position = (j, i)
            if char == "S":
                start = position
                tiles.add(position)
            elif char == "E":
                end = position
                tiles.add(position)
            elif char == ".":
                tiles.add(position)
    return start, end, tiles

def x(position):
    return position[0]

def y(position):
    return position[1]

# more helper function alternate names
coordinate = x
heading = y

def cost(tup):
    return tup[2]

class PriorityQueue:
    def __init__(self):
        self.queue = []
    
    def push(self, element, priority):
        heapq.heappush(self.queue, (priority, element))

    def pop(self):
        return heapq.heappop(self.queue)[1]

    def empty(self):
        return len(self.queue) == 0

def to_graph(tiles):
    graph = dict()
    for tile in tiles:
        for direction in [Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST]:
            neighbors = set()
            neighbors.add((tile, (direction + 1) % 4, 1000))
            neighbors.add((tile, (direction - 1) % 4, 1000))
            north = (x(tile), y(tile) - 1)
            south = (x(tile), y(tile) + 1)
            east = (x(tile) + 1, y(tile))
            west = (x(tile) - 1, y(tile))
            if direction == Direction.NORTH and north in tiles:
                neighbors.add((north, direction, 1))
            elif direction == Direction.EAST and east in tiles:
                neighbors.add((east, direction, 1))
            elif direction == Direction.SOUTH and south in tiles:
                neighbors.add((south, direction, 1))
            elif direction == Direction.WEST and west in tiles:
                neighbors.add((west, direction, 1))
            graph[(tile, direction)] = neighbors
    return graph

# there's not really any reason not to use plain old dijkstra for this part,
# but it's easier not to rewrite
def search(graph, start, end):
    heuristic = lambda tile: abs(x(tile) - x(end)) + abs(y(tile) - y(end))
    start_node = (start, Direction.EAST)
    frontier = PriorityQueue()
    frontier.push(start_node, heuristic(start))
    came_from = dict()
    cost_so_far = dict()
    came_from[start_node] = set()
    cost_so_far[start_node] = 0

    while not frontier.empty():
        current = frontier.pop()
        for next in graph[current]:
            new_cost = cost_so_far[current] + cost(next)
            next_node = (coordinate(next), heading(next))
            if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                cost_so_far[next_node] = new_cost
                priority = new_cost + heuristic(coordinate(next))
                frontier.push(next_node, priority)
                came_from[next_node] = {current}
            elif next_node in cost_so_far and new_cost == cost_so_far[next_node]:
                came_from[next_node].add(current)
    
    min_cost = min([node_cost for node, node_cost in cost_so_far.items() if coordinate(node) == end])
    best_end_nodes = {(end, direction) for direction in [Direction.NORTH, Direction.SOUTH, Direction.EAST, Direction.WEST] if (end, direction) in came_from and cost_so_far[(end, direction)] == min_cost}
    return retrace(best_end_nodes, came_from)

def retrace(best_end_nodes, came_from):
    next = best_end_nodes
    tiles = set()
    while len(next) > 0:
        current = next.pop()
        next.update(came_from[current])
        tiles.add(coordinate(current))
    visualize(tiles)
    return len(tiles)

def visualize(tiles):
    # set manually because it isn't actually stored in the model
    xsize = 141
    ysize = 141
    for i in range(ysize):
        for j in range(xsize):
            if (j, i) in tiles:
                print("O", end="")
            else:
                print(".", end="")
        print()
    print()

with open("day16/input.txt", "r") as f:
    lines = f.readlines()
    start, end, tiles = parse(lines)
    graph = to_graph(tiles)
    num_tiles = search(graph, start, end)
    print(num_tiles)

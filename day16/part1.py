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

def search(graph, start, end):
    heuristic = lambda tile: abs(x(tile) - x(end)) + abs(y(tile) - y(end))
    start_node = (start, Direction.EAST)
    frontier = PriorityQueue()
    frontier.push(start_node, heuristic(start))
    came_from = dict()
    cost_so_far = dict()
    came_from[start_node] = None
    cost_so_far[start_node] = 0

    while not frontier.empty():
        current = frontier.pop()
        if coordinate(current) == end:
            break
        for next in graph[current]:
            new_cost = cost_so_far[current] + cost(next)
            next_node = (coordinate(next), heading(next))
            if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                cost_so_far[next_node] = new_cost
                priority = new_cost + heuristic(coordinate(next))
                frontier.push(next_node, priority)
                came_from[next_node] = current
    
    return min([node_cost for node, node_cost in cost_so_far.items() if coordinate(node) == end])

with open("day16/input.txt", "r") as f:
    lines = f.readlines()
    start, end, tiles = parse(lines)
    graph = to_graph(tiles)
    cost = search(graph, start, end)
    print(cost)

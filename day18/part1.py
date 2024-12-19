import heapq

SIZE = 70
NUM_BYTES = 1024

def parse(lines):
    corrupt_tiles = {tuple(map(int, line.strip().split(","))) for line in lines[:NUM_BYTES]}
    return {(x, y) for x in range(SIZE + 1) for y in range(SIZE + 1) if (x, y) not in corrupt_tiles}

class PriorityQueue:
    def __init__(self):
        self._queue = []
    
    def push(self, element, priority):
        heapq.heappush(self._queue, (priority, element))

    def pop(self):
        return heapq.heappop(self._queue)[1]

    def empty(self):
        return len(self._queue) == 0

def adjacent(tile, safe_tiles):
    x, y = tile
    return {tup for tup in {(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)} if in_memory(tup) and tup in safe_tiles}

def in_memory(tile):
    x, y = tile
    return x >= 0 and x <= SIZE and y >= 0 and y <= SIZE

def manhattan_distance(tile1, tile2):
    x1, y1 = tile1
    x2, y2 = tile2
    return abs(x1 - x2) + abs(y1 - y2)

def search(safe_tiles, start, end):
    heuristic = lambda tile: manhattan_distance(tile, end)
    frontier = PriorityQueue()
    frontier.push(start, heuristic(start))
    came_from = {start: None}
    cost_so_far = {start: 0}

    while not frontier.empty():
        current = frontier.pop()
        if current == end:
            break
        for next in adjacent(current, safe_tiles):
            new_cost = cost_so_far[current] + 1
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(next)
                frontier.push(next, priority)
                came_from[next] = current
    
    return cost_so_far[end]

with open("day18/input.txt", "r") as f:
    lines = f.readlines()
    safe_tiles = parse(lines)
    start = (0, 0)
    end = (SIZE, SIZE)
    distance = search(safe_tiles, start, end)
    print(distance)

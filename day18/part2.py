import heapq

SIZE = 70

def parse(lines):
    return [tuple(map(int, line.strip().split(","))) for line in lines]

class PriorityQueue:
    def __init__(self):
        self._queue = []
    
    def push(self, element, priority):
        heapq.heappush(self._queue, (priority, element))

    def pop(self):
        return heapq.heappop(self._queue)[1]

    def empty(self):
        return len(self._queue) == 0

def adjacent(tile, corrupt_tiles):
    x, y = tile
    return {tup for tup in {(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)} if in_memory(tup) and tup not in corrupt_tiles}

def in_memory(tile):
    x, y = tile
    return x >= 0 and x <= SIZE and y >= 0 and y <= SIZE

def manhattan_distance(tile1, tile2):
    x1, y1 = tile1
    x2, y2 = tile2
    return abs(x1 - x2) + abs(y1 - y2)

def search(corrupt_tiles, start, end):
    heuristic = lambda tile: manhattan_distance(tile, end)
    frontier = PriorityQueue()
    frontier.push(start, heuristic(start))
    came_from = {start: None}
    cost_so_far = {start: 0}

    while not frontier.empty():
        current = frontier.pop()
        # visualize(corrupt_tiles, frontier, current)
        if current == end:
            break
        for next in adjacent(current, corrupt_tiles):
            new_cost = cost_so_far[current] + 1
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(next)
                frontier.push(next, priority)
                came_from[next] = current
    
    return end in cost_so_far

def first_tile_cutoff(corrupt_tiles):
    running_corrupt_tiles = set()
    start = (0, 0)
    end = (SIZE, SIZE)

    # we could optimize this considerably by doing binary search
    for tile in corrupt_tiles:
        running_corrupt_tiles.add(tile)
        can_escape = search(running_corrupt_tiles, start, end)
        if not can_escape:
            return tile
    return None

def visualize(corrupt_tiles, frontier, current):
    for i in range(SIZE + 1):
        for j in range(SIZE + 1):
            tile = (j, i)
            if tile in corrupt_tiles:
                print("#", end="")
            elif tile in frontier._queue:
                print("O", end="")
            elif tile == current:
                print("@", end="")
            else:
                print(".", end="")
        print()
    print()

with open("day18/input.txt", "r") as f:
    lines = f.readlines()
    corrupt_tiles = parse(lines)
    tile = first_tile_cutoff(corrupt_tiles)
    print(tile)

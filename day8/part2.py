import itertools
from math import ceil


class AntennaMap():
    def __init__(self, xsize, ysize, frequencies) -> None:
        self.xsize = xsize
        self.ysize = ysize
        self.frequencies = frequencies

def get_antennas(lines):
    frequencies = {}
    for i in range(len(lines)):
        line = lines[i].strip()
        for j in range(len(line)):
            char = lines[i][j]
            if char != ".":
                if char not in frequencies:
                    frequencies[char] = {(j, i)}
                else:
                    frequencies[char].add((j, i))
    return AntennaMap(len(lines[0].strip()), len(lines), frequencies)

def in_map(coord, map):
    x = coord[0]
    y = coord[1]
    return 0 <= x and x < map.xsize and 0 <= y and y < map.ysize

def antinodes(antenna_map):
    antis = set()
    for antennas in antenna_map.frequencies.values():
        pairs = itertools.combinations(antennas, 2)
        for pair in pairs:
            first = pair[0]
            second = pair[1]
            xdiff = first[0] - second[0]
            ydiff = first[1] - second[1]
            max_copies = ceil(abs(max(antenna_map.xsize / xdiff, antenna_map.ysize / ydiff)))
            first_antis = [(first[0] + i * xdiff, first[1] + i * ydiff) for i in range(1, max_copies)]
            second_antis = [(second[0] - i * xdiff, second[1] - i * ydiff) for i in range(1, max_copies)]
            antis.update(first_antis + second_antis + [first, second])
    valid = {anti for anti in antis if in_map(anti, antenna_map)}
    return len(valid)

with open("day8/input.txt", "r") as f:
    lines = f.readlines()
    map = get_antennas(lines)
    count = antinodes(map)
    print(count)

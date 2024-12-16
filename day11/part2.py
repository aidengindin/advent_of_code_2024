NUM_BLINKS = 75

def parse(lines):
    line = lines[0].strip()
    return [int(stone) for stone in line.split()]

def blink(stone, num_blinks, cache):
    if (stone, num_blinks) in cache:
        return cache[(stone, num_blinks)]
    if num_blinks == 0:
        return 1

    result = 0
    num_digits = len(str(stone))
    if stone == 0:
        result = blink(1, num_blinks - 1, cache)
    elif num_digits % 2 == 0:
        first_half = int(str(stone)[:num_digits//2])
        second_half = int(str(stone)[num_digits//2:])
        first_result = blink(first_half, num_blinks - 1, cache)
        second_result = blink(second_half, num_blinks - 1, cache)
        result = first_result + second_result
    else:
        result = blink(stone * 2024, num_blinks - 1, cache)
    cache[(stone, num_blinks)] = result
    return result

def blink_all(stones, num_blinks):
    cache = dict()
    return sum([blink(stone, num_blinks, cache) for stone in stones])

with open("day11/input.txt", "r") as f:
    lines = f.readlines()
    stones = parse(lines)
    num_stones = blink_all(stones, NUM_BLINKS)
    print(num_stones)

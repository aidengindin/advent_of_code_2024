NUM_BLINKS = 25

def parse(lines):
    line = lines[0].strip()
    return [int(stone) for stone in line.split()]

def blink(stones):
    new_stones = []
    for stone in stones:
        if stone == 0:
            new_stones.append(1)
        elif len(str(stone)) % 2 == 0:
            num_digits = len(str(stone))
            first_half = int(str(stone)[:num_digits//2])
            second_half = int(str(stone)[num_digits//2:])
            new_stones.append(first_half)
            new_stones.append(second_half)
        else:
            new_stones.append(stone * 2024)
    return new_stones

with open("day11/input.txt", "r") as f:
    lines = f.readlines()
    stones = parse(lines)
    for _ in range(NUM_BLINKS):
        stones = blink(stones)
    print(len(stones))

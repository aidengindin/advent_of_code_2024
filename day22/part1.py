from functools import reduce


PRUNE_MOD = 16777216
NUM_ITERATIONS = 2000

def parse(lines):
    return [int(line.strip()) for line in lines]

def mix(secret_number: int, target: int) -> int:
    return secret_number ^ target

def prune(num: int) -> int:
    return num % PRUNE_MOD

def next_secret_number(secret_number: int) -> int:
    a = mix(secret_number, secret_number * 64)
    b = prune(a)
    c = mix(b, b // 32)
    d = prune(c)
    e = mix(d, d * 2048)
    f = prune(e)
    return f

def iterate(secret_number: int, num_iterations: int) -> int:
    return reduce(lambda x, _: next_secret_number(x), range(num_iterations), secret_number)

def secret_number_sum(numbers):
    return sum([iterate(number, NUM_ITERATIONS) for number in numbers])

with open("day22/input.txt", "r") as f:
    lines = f.readlines()
    numbers = parse(lines)
    result = secret_number_sum(numbers)
    print(result)

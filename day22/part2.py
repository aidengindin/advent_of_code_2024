from functools import reduce


PRUNE_MOD = 16777216
NUM_ITERATIONS = 2000

def parse(lines):
    return [int(line.strip()) for line in lines]

def mix(secret_number: int, target: int) -> int:
    return secret_number ^ target

def prune(num: int) -> int:
    return num % PRUNE_MOD

def last_digit(x: int) -> int:
    return x % 10

def next_secret_number(secret_number: int) -> int:
    a = mix(secret_number, secret_number * 64)
    b = prune(a)
    c = mix(b, b // 32)
    d = prune(c)
    e = mix(d, d * 2048)
    f = prune(e)
    return f, last_digit(f) - last_digit(secret_number)

def get_prices(secret_number: int, num_iterations: int) -> list[tuple[int, int]]:
        result = [(secret_number, 0)]
        current = secret_number
        for _ in range(num_iterations):
            next_val = next_secret_number(current)
            result.append(next_val)
            current = next_val[0]
        return [(last_digit(num), change) for num, change in result]

def get_all_prices(initial_secrets: int, num_iterations: int) -> list[list[tuple[int, int]]]:
    return [get_prices(secret, num_iterations) for secret in initial_secrets]

def best_sequence(all_prices):
    sequences = dict()
    for buyer in all_prices:
        buyer_sequences = dict()
        for i in range(4, len(buyer)):
            current_price, change0 = buyer[i]    
            change1 = buyer[i - 1][1]
            change2 = buyer[i - 2][1]
            change3 = buyer[i - 3][1]
            sequence = (change3, change2, change1, change0)
            if sequence not in buyer_sequences:
                buyer_sequences[sequence] = current_price
        for sequence, price in buyer_sequences.items():
            if sequence in sequences:
                sequences[sequence] += price
            else:
                sequences[sequence] = price
    best = max(sequences, key=lambda sequence: sequences[sequence])
    return sequences[best]

with open("day22/input.txt", "r") as f:
    lines = f.readlines()
    numbers = parse(lines)
    prices = get_all_prices(numbers, NUM_ITERATIONS)
    best = best_sequence(prices)
    print(best)

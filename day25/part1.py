LOCK_HEIGHT = 7
LOCK_WIDTH = 5

def chunk(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def parse(lines):
    lines = [line.strip() for line in lines if len(line.strip()) > 0]
    locks_and_keys = list(chunk(lines, LOCK_HEIGHT))
    locks = set()
    keys = set()
    for item in locks_and_keys:
        result = [0] * LOCK_WIDTH
        for i in range(LOCK_HEIGHT):
            for j in range(LOCK_WIDTH):
                if item[i][j] == '#':
                    result[j] += 1
        if item[0][0] == '.':
            keys.add(tuple(result))
        elif item[0][0] == '#':
            locks.add(tuple(result))
    return keys, locks

def num_matching_locks(key, locks):
    return sum(1 for lock in locks if all(key[i] + lock[i] <= LOCK_HEIGHT for i in range(LOCK_WIDTH)))

def num_pairs(keys, locks):
    return sum(num_matching_locks(key, locks) for key in keys)

if __name__ == '__main__':
    with open('day25/input.txt', 'r') as f:
        lines = f.readlines()
        keys, locks = parse(lines)
        result = num_pairs(keys, locks)
        print(result)

def parse(line):
    line = line.strip()
    filesystem = []
    num_files = 0
    for i in range(len(line)):
        count = int(line[i])
        if i % 2 == 0:
            filesystem += [num_files] * count
            num_files += 1
        else:
            filesystem += [None] * count
    return filesystem

def compact(filesystem):
    block_pointer = len(filesystem) - 1
    empty_blocks = find_empty_blocks(filesystem)
    while block_pointer > 0:
        if filesystem[block_pointer] == None:
            block_pointer -= 1
            continue
        file_size = 1
        file_id = filesystem[block_pointer]
        for i in range(block_pointer - 1, 0, -1):
            if filesystem[i] != file_id:
                break
            else:
                file_size += 1
        for i, (start_index, empty_size) in enumerate(empty_blocks):
            if file_size <= empty_size:
                if start_index > block_pointer:
                    break
                for j in range(start_index, start_index + file_size):
                    filesystem[j] = file_id
                for j in range(block_pointer, block_pointer - file_size, -1):
                    filesystem[j] = None
                empty_blocks[i] = (start_index + file_size, empty_size - file_size)
                break
        block_pointer -= file_size
    return filesystem

def find_empty_blocks(filesystem):
    empty_size = 0
    start_index = 0
    blocks = []
    for i in range(len(filesystem)):
        block = filesystem[i]
        if block == None:
            if empty_size == 0:
                start_index = i
            empty_size += 1
        elif empty_size > 0:
            blocks.append((start_index, empty_size))
            empty_size = 0
    return blocks

def checksum(filesystem):
    return sum([(index * file_id if file_id != None else 0) for index, file_id in enumerate(filesystem)])

def visualize(filesystem):
    for block in filesystem:
        if block == None:
            print(".", end="")
        else:
            print(block, end="")
    print()

with open("day9/input.txt", "r") as f:
    line = f.readlines()[0]
    filesystem = parse(line)
    filesystem = compact(filesystem)
    check = checksum(filesystem)
    print(check)

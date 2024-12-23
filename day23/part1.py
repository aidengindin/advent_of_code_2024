def parse(lines):
    v = set()
    e = set()
    for line in lines:
        computers = line.strip().split("-")
        v.add(computers[0])
        v.add(computers[1])
        e.add((computers[0], computers[1]))
    return v, e

def connected(computer1, computer2, connections):
    return (computer1, computer2) in connections or (computer2, computer1) in connections

def sorted(l):
    l.sort()
    return l

def matching_cliques(computers, connections):
    result = set()
    for connection in connections:
        a, b = connection
        a_connected = {c for c in computers if connected(a, c, connections)}
        b_connected = {c for c in computers if connected(b, c, connections)}
        result.update({tuple(sorted([a, b, c])) for c in a_connected.intersection(b_connected) if any(name[0] == "t" for name in [a, b, c])})
    return len(result)

with open("day23/input.txt", "r") as f:
    lines = f.readlines()
    computers, connections = parse(lines)
    num = matching_cliques(computers, connections)
    print(num)

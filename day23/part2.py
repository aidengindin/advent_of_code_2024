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

def max_clique_from(
        clique: set[str],
        computers: set[str],
        connections: set[tuple[str, str]],
        memo: dict[tuple[str], set[str]]
        ) -> set[str]:
    key = tuple(sorted(list(clique)))
    if key in memo:
        return memo[key]
    connected_to_all = {computer for computer in computers if all(connected(clique_member, computer, connections) for clique_member in clique)}
    next_cliques = {frozenset(clique.union({computer})) for computer in connected_to_all}
    out = clique
    for next_clique in next_cliques:
        result = max_clique_from(next_clique, computers, connections, memo)
        if len(result) > len(out):
            out = result
    memo[key] = out
    return out

def max_clique_str(computers, connections):
    memo = dict()
    clique = max([max_clique_from({e[0], e[1]}, computers, connections, memo) for e in connections], key=lambda c: len(c))
    return ",".join(sorted(list(clique)))

with open("day23/input.txt", "r") as f:
    lines = f.readlines()
    computers, connections = parse(lines)
    out = max_clique_str(computers, connections)
    print(out)

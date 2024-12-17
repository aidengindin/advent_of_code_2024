import numpy as np

def parse(lines):
    equations = []
    x_coefficients = []
    y_coefficients = []
    for line in lines:
        words = line.split()
        if len(words) == 0:
            continue
        if words[0] == "Button":
            coefficient1 = words[2].split("+")[1].strip(",")
            coefficient2 = words[3].split("+")[1].strip(",")
            x_coefficients.append(coefficient1)
            y_coefficients.append(coefficient2)
        elif words[0] == "Prize:":
            solution1 = int(words[1].split("=")[1].strip(",")) + 10000000000000
            solution2 = int(words[2].split("=")[1].strip(",")) + 10000000000000
            matrix = np.array([x_coefficients, y_coefficients], dtype=np.dtype(int))
            solution = np.array([solution1, solution2], dtype=np.dtype(int))
            equations.append((matrix, solution))
            x_coefficients = []
            y_coefficients = []
    return equations

def num_tokens(equation):
    coefficients = equation[0]
    rhs = equation[1]
    solution = np.linalg.solve(coefficients, rhs)
    a = solution[0]
    b = solution[1]
    if is_almost_integer(a) and is_almost_integer(b):
        return 3 * round(a) + round(b)
    return 0

def is_almost_integer(x, tolerance=1e-13):
    return abs(x - round(x)) / abs(x) < tolerance if x != 0 else abs(x - round(x)) < tolerance

def total_tokens(equations):
    return sum([num_tokens(equation) for equation in equations])

with open("day13/input.txt", "r") as f:
    lines = f.readlines()
    equations = parse(lines)
    tokens = total_tokens(equations)
    print(tokens)

from abc import ABC, abstractmethod
from enum import Enum
import re


class Key(str, Enum):
    ZERO = "0"
    ONE = "1"
    TWO = "2"
    THREE = "3"
    FOUR = "4"
    FIVE = "5"
    SIX = "6"
    SEVEN = "7"
    EIGHT = "8"
    NINE = "9"
    
    ENTER = "A"

    UP = "^"
    DOWN = "v"
    LEFT = "<"
    RIGHT = ">"

    PANIC = " "

class Direction(str, Enum):
    UP = "^"
    DOWN = "v"
    LEFT = "<"
    RIGHT = ">"

NUMERIC_LAYOUT = [[Key.SEVEN, Key.EIGHT, Key.NINE],
                  [Key.FOUR, Key.FIVE, Key.SIX],
                  [Key.ONE, Key.TWO, Key.THREE],
                  [Key.PANIC, Key.ZERO, Key.ENTER]]

DIRECTIONAL_LAYOUT = [[Key.PANIC, Key.UP, Key.ENTER],
                      [Key.LEFT, Key.DOWN, Key.RIGHT]]

class Keypad(ABC):
    def __init__(self, key_layout: list[list[Key]]):
        self.key_layout = key_layout

    def move(self, start: tuple[int, int], direction: Direction):
        row, col = start
        new_position = None
        if direction == Direction.UP:
            new_position = (row - 1, col)
        elif direction == Direction.DOWN:
            new_position = (row + 1, col)
        elif direction == Direction.LEFT:
            new_position = (row, col - 1)
        elif direction == Direction.RIGHT:
            new_position = (row, col + 1)
        if not self.in_layout(new_position):
            raise IndexError("Illegal move")
        return new_position

    def in_layout(self, position: tuple[int, int]) -> bool:
        row, col = position
        return 0 <= row < len(self.key_layout) and 0 <= col < len(self.key_layout[0])

    @abstractmethod
    def move_to(self, target: tuple[int, int]) -> list[Direction]:
        pass


    def get_position(self, key: Key) -> tuple[int, int]:
        for row_index, row in enumerate(self.key_layout):
            if key in row:
                return (row_index, row.index(key))
        return None

class NumericKeypad(Keypad):
    def __init__(self):
        super().__init__(NUMERIC_LAYOUT)
    
    def paths_to(self, start: tuple[int, int], end: tuple[int, int]) -> set[list[Direction]]:
        row_diff, col_diff = end[0] - start[0], end[1] - start[1]
        row_direction = Direction.UP if row_diff < 0 else Direction.DOWN
        col_direction = Direction.LEFT if col_diff < 0 else Direction.RIGHT
        row_diff, col_diff = abs(row_diff), abs(col_diff)

        h_then_v = [row_direction] * row_diff + [col_direction] * col_diff
        v_then_h = [col_direction] * col_diff + [row_direction] * row_diff
        return set(map(tuple, filter(lambda path: self.is_valid(start, path), [h_then_v, v_then_h])))
    
    def is_valid(self, start: tuple[int, int], path: list[Direction]) -> bool:
        position = start
        for direction in path:
            position = self.move(position, direction)
            row, col = position
            if self.key_layout[row][col] == Key.PANIC:
                return False
        return True


    def move_to(self, start: tuple[int, int], end: tuple[int, int]) -> list[Direction]:
        row_diff, col_diff = end[0] - start[0], end[1] - start[1]
        row_direction = Direction.UP if row_diff < 0 else Direction.DOWN
        col_direction = Direction.LEFT if col_diff < 0 else Direction.RIGHT
        row_diff, col_diff = abs(row_diff), abs(col_diff)
        moves = []

        # if moving up, move vertically first, then horizontally, to avoid panic zone
        # if moving down, opposite
        if row_direction == Direction.UP:
            for _ in range(row_diff):
                # self.move(row_direction)
                moves.append(row_direction)
        for _ in range(col_diff):
            # self.move(col_direction)
            moves.append(col_direction)
        if row_direction == Direction.DOWN:
            for _ in range(row_diff):
                # self.move(row_direction)
                moves.append(row_direction)

        return moves

class DirectionalKeypad(Keypad):
    def __init__(self):
        super().__init__(DIRECTIONAL_LAYOUT)

    def keypresses_to_move(self, start: tuple[int, int], end: tuple[int, int]) -> list[Key]:
        return list(map(get_direction_key, self.move_to(start, end))) + [Key.ENTER]

    def move_to(self, start: tuple[int, int], end: tuple[int, int]) -> list[Direction]:
        row_diff, col_diff = end[0] - start[0], end[1] - start[1]
        row_direction = Direction.UP if row_diff < 0 else Direction.DOWN
        col_direction = Direction.LEFT if col_diff < 0 else Direction.RIGHT
        row_diff, col_diff = abs(row_diff), abs(col_diff)
        moves = []

        # if moving down, move vertically first, then horizontally, to avoid panic zone
        # if moving up, opposite
        if row_direction == Direction.DOWN:
            for _ in range(row_diff):
                # self.move(row_direction)
                moves.append(row_direction)
        for _ in range(col_diff):
            # self.move(col_direction)
            moves.append(col_direction)
        if row_direction == Direction.UP:
            for _ in range(row_diff):
                # self.move(row_direction)
                moves.append(row_direction)

        return moves

def get_direction_key(direction: Direction) -> Key:
    if direction == Direction.UP:
        return Key.UP
    if direction == Direction.DOWN:
        return Key.DOWN
    if direction == Direction.LEFT:
        return Key.LEFT
    if direction == Direction.RIGHT:
        return Key.RIGHT

def generate_moves(lines: list[str]) -> list[Direction]:

    # sequence: our moves -> first_directional_keypad -> second_directional_keypad -> numeric_keypad
    first_directional_keypad = DirectionalKeypad()
    second_directional_keypad = DirectionalKeypad()
    numeric_keypad = NumericKeypad()
    moves: dict[str, list[Direction]] = dict()
    numeric_keypad_position = (3,2)
    second_directional_keypad_position = (0,2)
    first_directional_keypad_position = (0,2)

    for code in lines:
        for key in code:
            new_numeric_keypad_position = numeric_keypad.get_position(key)
            numeric_keypad_paths = numeric_keypad.paths_to(numeric_keypad_position, new_numeric_keypad_position)
            path_sequences = {k: [] for k in numeric_keypad_paths}
            saved_first_directional_keypad_position = first_directional_keypad_position
            saved_second_direction_keypad_position = second_directional_keypad_position
            for path in numeric_keypad_paths:
                first_directional_keypad_position = saved_first_directional_keypad_position
                second_directional_keypad_position = saved_second_direction_keypad_position
                numeric_keypad_moves = list(map(get_direction_key, path)) + [Key.ENTER]
                for numeric_keypad_move in numeric_keypad_moves:
                    new_second_directional_keypad_position = second_directional_keypad.get_position(numeric_keypad_move)
                    second_directional_keypad_moves = second_directional_keypad.keypresses_to_move(second_directional_keypad_position, new_second_directional_keypad_position)
                    for second_directional_keypad_move in second_directional_keypad_moves:
                        new_first_directional_keypad_position = first_directional_keypad.get_position(second_directional_keypad_move)
                        first_directional_keypad_moves = first_directional_keypad.keypresses_to_move(first_directional_keypad_position, new_first_directional_keypad_position)
                        path_sequences[path] += first_directional_keypad_moves
                        first_directional_keypad_position = new_first_directional_keypad_position
                    second_directional_keypad_position = new_second_directional_keypad_position
            best_path_sequence = min([sequence for _, sequence in path_sequences.items()], key=lambda path: len(path))
            if code in moves:
                moves[code] += best_path_sequence
            else:
                moves[code] = best_path_sequence
            numeric_keypad_position = new_numeric_keypad_position

    return moves

def complexity(code, moves):
    length = len(moves)
    numeric = sum(map(int, re.compile(r"\d+").findall(code)))
    return length * numeric

def complexity_sum(moves_dict):
    return sum(complexity(code, moves) for code, moves in moves_dict.items())

with open("day21/input.txt", "r") as f:
    lines = [line.strip() for line in f.readlines()]
    # lines = ["029A"]
    moves_dict = generate_moves(lines)
    result = complexity_sum(moves_dict)
    print(result)

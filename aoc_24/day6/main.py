# pylint: disable=C0114,C0116
# pylint: disable=C0413,E0611
import sys
from pathlib import Path
from typing import List

utils_path = Path(__file__).resolve().parents[2] / "utils"
sys.path.insert(0, str(utils_path))
from collections import defaultdict
from profile import timeit


def parse_map(lines):
    start = "^"
    matrix = list([list(line.strip()) for line in lines])
    height = len(matrix)
    width = len(matrix[0])
    for i in range(height):
        for j in range(width):
            if matrix[i][j] == start:
                return matrix, (i, j)


def is_inside(height, width, next_position):
    if 0 <= next_position[0] < height and 0 <= next_position[1] < width:
        return True
    return False


def patrol(matrix, starting_position, direction):
    height, width = len(matrix), len(matrix[0])
    delta = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # NORTH, EAST, SOUTH, WEST
    obstacle = "#"
    visited = defaultdict(list)
    visited[starting_position].append(direction)
    last_position = starting_position
    while True:
        next_position = (
            last_position[0] + delta[direction][0],
            last_position[1] + delta[direction][1],
        )
        if not is_inside(
            height=height, width=width, next_position=next_position
        ):
            return True, visited

        if matrix[next_position[0]][next_position[1]] == obstacle:
            direction = (direction + 1) % 4
        else:
            last_position = next_position
            if (
                last_position in visited.keys()
                and direction in visited[last_position]
            ):
                return False, visited
            visited[last_position].append(direction)


def p1(lines: List[str]):
    matrix, starting_position = parse_map(lines)
    _, visited = patrol(matrix, starting_position, direction=0)
    return len(visited)


def p2(lines: List[str]):
    result = 0
    matrix, starting_position = parse_map(lines)
    exited, visited = patrol(matrix, starting_position, direction=0)
    del visited[starting_position]
    for position in visited.keys():
        matrix[position[0]][position[1]] = "#"
        exited, _ = patrol(matrix, starting_position, direction=0)
        if not exited:
            result += 1
        matrix[position[0]][position[1]] = "."
    return result


# Using complex numbers
def parse_map_complex(lines):
    matrix = {
        i + j * 1j: c
        for i, r in enumerate(lines)
        for j, c in enumerate(r.strip())
    }
    return matrix


def patrol_complex(matrix):
    start = min(pos for pos in matrix if matrix[pos] == "^")
    pos, direction, seen = start, -1, set()
    while pos in matrix and (pos, direction) not in seen:
        seen |= {(pos, direction)}
        if matrix.get(pos + direction) == "#":
            direction *= -1j
        else:
            pos += direction
    return {p for p, _ in seen}, (pos, direction) in seen


def p1_complex(lines):
    matrix = parse_map_complex(lines)
    path = patrol_complex(matrix)[0]
    return len(path)


# Seen this solution on internet. However is considerably slower than the previous implementation.
def p2_complex(lines):
    matrix = parse_map_complex(lines)
    start = min(pos for pos in matrix if matrix[pos] == "^")
    path = patrol_complex(matrix)[0]
    return sum(
        patrol_complex(matrix | {o: "#"})[1] for o in path if o != start
    )


if __name__ == "__main__":
    with open("input.txt", encoding="utf8") as f:
        input_lines = f.readlines()
        print(f"First part: {p1(input_lines)}")
        # print(f"Second part: {p2(input_lines)}")
        print(f"First part using complex: {p1_complex(input_lines)}")
        print(f"Second part using complex: {p2_complex(input_lines)}")

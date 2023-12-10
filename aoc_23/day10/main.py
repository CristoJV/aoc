import logging

import numpy as np


def parse_lines(lines):
    sketch = [list(line.strip()) for line in lines]
    return sketch


def find_loop(sketch):
    # Fin the starting point (S)
    idx, jdx = 0, 0
    for i in range(len(sketch)):
        for J in range(len(sketch[0])):
            if sketch[i][J] == "S":
                idx, jdx = i, J
                break

    src = (idx, jdx)
    starts = next(idx, jdx, "S", sketch)
    visited = []
    next_move = [starts[0]]
    while len(next_move) != 0:
        next_move = next_move[0]
        visited.append(next_move)

        next_valid_moves = next(
            next_move[0],
            next_move[1],
            sketch[next_move[0]][next_move[1]],
            sketch,
        )

        next_move = [
            next_move
            for next_move in next_valid_moves
            if next_move not in visited
        ]
    return visited, src


def part_1(lines):
    sketch = parse_lines(lines)
    visited, src = find_loop(sketch)
    return len(visited) // 2 + 1


def next(idx, jdx, pipe_type, sketch):
    next_valid_moves = []

    def add_top():
        top = (idx - 1, jdx)
        if top[0] >= 0 and sketch[top[0]][top[1]] in ["F", "7", "|"]:
            next_valid_moves.append(top)

    def add_left():
        left = (idx, jdx - 1)
        if left[1] >= 0 and sketch[left[0]][left[1]] in ["L", "F", "-"]:
            next_valid_moves.append(left)

    def add_bot():
        bot = (idx + 1, jdx)
        if bot[0] < len(sketch) and sketch[bot[0]][bot[1]] in ["L", "J", "|"]:
            next_valid_moves.append(bot)

    def add_right():
        right = (idx, jdx + 1)
        if right[1] < len(sketch[0]) and sketch[right[0]][right[1]] in [
            "-",
            "J",
            "7",
        ]:
            next_valid_moves.append(right)

    if pipe_type == "|":
        add_top()
        add_bot()
    elif pipe_type == "-":
        add_left()
        add_right()
    elif pipe_type == "L":
        add_top()
        add_right()
    elif pipe_type == "J":
        add_top()
        add_left()
    elif pipe_type == "7":
        add_bot()
        add_left()
    elif pipe_type == "F":
        add_bot()
        add_right()
    elif pipe_type == "S":
        add_top()
        add_left()
        add_bot()
        add_right()
    return next_valid_moves


def part_2(lines):
    sketch = parse_lines(lines)
    visited, src = find_loop(sketch)
    visited.append(src)

    # Ray casting
    visited_np = np.asarray([list(v) for v in visited])
    min_y, min_x = visited_np.min(axis=0)
    max_y, max_x = visited_np.max(axis=0)

    points = np.zeros((max_y - min_y + 1, max_x - min_x + 1), dtype=int)
    for v in visited:
        points[v[0] - min_y, v[1] - min_x] = 1

    evaluation_points = np.argwhere(points == 0)
    for v in visited:
        if sketch[v[0]][v[1]] == "-":
            points[v[0] - min_y, v[1] - min_x] = 0

    for i in range(min_y, max_y + 1):
        for j in range(min_x, max_x + 1):
            if sketch[i][j] == "L":
                for k in range(j + 1, max_x + 1):
                    if sketch[i][k] == "-":
                        continue
                    elif sketch[i][k] == "7":
                        points[i - min_y, j - min_x : k - min_x] = 0
                        break
                    else:
                        break
            elif sketch[i][j] == "F":
                for k in range(j + 1, max_x + 1):
                    if sketch[i][k] == "-":
                        continue
                    elif sketch[i][k] == "J":
                        points[i - min_y, j - min_x : k - min_x] = 0
                        break
                    else:
                        break

    inside_points = 0
    for evaluation_point in evaluation_points:
        interval = points[evaluation_point[0], : evaluation_point[1]]
        interval_sum = interval.sum()
        is_inside = interval_sum % 2 == 1
        if is_inside:
            inside_points += 1
    return inside_points


if __name__ == "__main__":
    with open("input.txt") as f:
        lines = f.readlines()

    logging.basicConfig(level=logging.INFO)

    logging.info(f"Part 1: {part_1(lines)}")
    logging.info(f"Part 2: {part_2(lines)}")

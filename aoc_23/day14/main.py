import logging
from copy import copy

import numpy as np


def parse_lines(lines):
    platform_map = np.asarray([list(line.strip()) for line in lines])
    return platform_map


def part(lines, part):
    platform_map = parse_lines(lines)
    rocks = np.argwhere((platform_map == "#") | (platform_map == "O")).tolist()
    points = 0
    len_rows = len(platform_map)

    score = 0
    fixed_rocks_rows_for_each_col = {}

    for rock in rocks:
        if platform_map[rock[0]][rock[1]] == "#":
            fixed_rocks_rows_for_each_col[rock[1]] = rock[0]
        elif platform_map[rock[0]][rock[1]] == "O":
            if rock[1] not in fixed_rocks_rows_for_each_col:
                fixed_rocks_rows_for_each_col[rock[1]] = 0
                points = len_rows - 0
                score += points
            elif rock[0] < fixed_rocks_rows_for_each_col[rock[1]]:
                fixed_rocks_rows_for_each_col[rock[1]] = 0
                points = len_rows - fixed_rocks_rows_for_each_col[rock[1]]
                score += points
            elif rock[0] > fixed_rocks_rows_for_each_col[rock[1]]:
                fixed_rocks_rows_for_each_col[rock[1]] += 1
                points = len_rows - fixed_rocks_rows_for_each_col[rock[1]]
                score += points
        else:
            print("No points")

    return score


if __name__ == "__main__":
    with open("input.txt") as f:
        lines = f.readlines()

    logging.basicConfig(level=logging.INFO)

    logging.info(f"Part 1: {part(lines, part=1)}")
    logging.info(f"Part 2: {part(lines, part=2)}")

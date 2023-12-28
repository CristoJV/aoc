import itertools
import logging

import numpy as np


def parse_lines(lines):
    trayectories = [line.strip().split("@") for line in lines]
    trayectories = [
        [list(map(int, x[0].split(", "))), list(map(int, x[1].split(", ")))]
        for x in trayectories
    ]
    return trayectories


def get_coefficient_matrix(x0, y0, vx, vy):
    return np.asarray([[1, -vy / vx, y0 - vy / vx * x0]])


def row_scale(matrix, row, factor):
    matrix[row] = matrix[row] * factor
    return matrix


def row_add(matrix, row, factor, row_to_add):
    matrix[row] = matrix[row] + matrix[row_to_add] * factor
    return matrix


def check_if_intersect_happens_in_future(x, x0, vx):
    # Compute the time when the two lines intersect
    t = (x - x0) / vx
    # Check if the intersection happens in the future
    if t < 0:
        return False
    else:
        return True


def check_if_intersect_happens_in_test_area(min_x, max_x, min_y, max_y, x, y):
    if x < min_x or x > max_x:
        return False
    if y < min_y or y > max_y:
        return False
    return True


def part_1(lines, min_x=7, max_x=27, min_y=7, max_y=27):
    trayectories = parse_lines(lines)
    pairs = list(itertools.combinations(trayectories, 2))
    count = 0
    for pair in pairs:
        pair_a = pair[0]
        pair_b = pair[1]

        coeff_a = get_coefficient_matrix(*pair_a[0][:2], *pair_a[1][:2])
        coeff_b = get_coefficient_matrix(*pair_b[0][:2], *pair_b[1][:2])
        matrix = np.concatenate((coeff_a, coeff_b))
        # Gaussian elimination
        matrix = row_add(matrix, 1, -matrix[1, 0], 0)
        if matrix[1, 1] == 0:  # No solution
            continue
        matrix = row_scale(matrix, 1, 1 / matrix[1, 1])
        x = matrix[1, 2]
        y = matrix[0, 2] - matrix[0, 1] * x
        if check_if_intersect_happens_in_future(
            x, pair_a[0][0], pair_a[1][0]
        ) and check_if_intersect_happens_in_future(
            x, pair_b[0][0], pair_b[1][0]
        ):
            if check_if_intersect_happens_in_test_area(
                min_x, max_x, min_y, max_y, x, y
            ):
                count += 1
    return count


if __name__ == "__main__":
    with open("input.txt") as f:
        lines = f.readlines()

    logging.basicConfig(level=logging.INFO)

    logging.info(
        f"Part 1: {part_1(lines, 
                          min_x=200000000000000,
                          max_x=400000000000000, 
                          min_y=200000000000000, 
                          max_y=400000000000000)}"
    )
    # logging.info(f"Part 2: {part_1(lines)}")

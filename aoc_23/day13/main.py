import logging

import numpy as np


def parse_lines(lines):
    patterns = [
        pattern.strip().split("\n") for pattern in "".join(lines).split("\n\n")
    ]
    return [np.asarray([list(row) for row in pattern]) for pattern in patterns]


def find_mirror(pattern, part, axis="column"):
    """Find the mirror line of a pattern.
    If part == 1, return the index of the mirror line.
    If part == 2, return a new the mirror line generated after
    swapping a single element (i.e. ass or rock).
    """
    len_pattern = pattern.shape[1 if axis == "column" else 0]
    for i in range(1, len_pattern):
        elements = min(i, len_pattern - i)

        if axis == "column":
            first_half = np.flip(pattern[:, i - elements : i], axis=1)
            second_half = pattern[:, i : elements + i]
        else:
            first_half = np.flip(pattern[i - elements : i, :], axis=0)
            second_half = pattern[i : elements + i, :]

        comparison = first_half != second_half
        if part == 1:
            if np.all(first_half == second_half):
                return i
        elif part == 2:
            if np.sum(comparison) == 1:
                return i
    return None


def part(lines, part):
    patterns = parse_lines(lines)
    total_value = 0

    for pattern in patterns:
        pattern = np.asarray(pattern)
        col = find_mirror(pattern, part=part, axis="column")
        if col is not None:
            total_value += col
        else:
            row = find_mirror(pattern, part=part, axis="row")
            if row is not None:
                total_value += row * 100
            else:
                print("Error no column or row found")

    return total_value


if __name__ == "__main__":
    with open("input.txt") as f:
        lines = f.readlines()

    logging.basicConfig(level=logging.INFO)

    logging.info(f"Part 1: {part(lines, part=1)}")
    logging.info(f"Part 2: {part(lines, part=2)}")

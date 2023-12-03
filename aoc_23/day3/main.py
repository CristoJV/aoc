from functools import reduce
from itertools import groupby

import numpy as np
from scipy import signal


def parse_input(lines):
    input_matrix = []
    for line in lines:
        line = line.strip()
        input_matrix.append(list(line))
    return input_matrix


def part_1_using_convolutions(lines):
    input_matrix = parse_input(lines)
    input_matrix_np = np.asarray(input_matrix)
    symbols_indexes = np.logical_not(
        np.char.isdigit(input_matrix_np)
        == False | np.char.not_equal(input_matrix_np, ".")
    )

    # Find where the symbols are
    # This returns a matrix with 1s where the symbols are and 0s
    # otherwise
    symbols_indexes = symbols_indexes.astype(int)

    # Dilate the ones (symbols) to the right, left, up and down using
    # a 3x3 kernel
    kernel = np.ones((3, 3), dtype=int)
    output = signal.convolve(symbols_indexes, kernel, mode="same").astype(int)

    # Find the digits
    digits = np.char.isdigit(input_matrix_np)

    # Find the digits that are next to a symbol
    digits_with_symbols = np.logical_and(digits, output)

    # Iterate over the digits to group them
    count = 0

    for idx, line in enumerate(input_matrix_np):
        # Group the digits in the same row
        groups = [
            list(group)
            for _, group, in groupby(line, key=lambda x: x.isdigit())
        ]
        index = 0

        # Iterate over the groups and check if they are next to a symbol
        for group in groups:
            max_len = index + len(group)

            # Check if the group is a number
            # If it is, check if it is next to a symbol
            # if not, skip it
            try:
                number = int("".join(group))
                if digits_with_symbols[idx, index:max_len].any():
                    count += number
            except:
                pass
            index = max_len
    return count


def part_2(lines):
    input_matrix = parse_input(lines)

    # Find the position of the gears
    input_matrix_np = np.asarray(input_matrix)
    symbols_indexes = np.char.equal(input_matrix_np, "*")
    symbols_indexes = symbols_indexes.astype(int)
    gears_indexes = np.argwhere(symbols_indexes)

    # Create a dictionary with the position of the gears as keys and an
    # empty list as value. The list will contain the digits that are
    # next to the gear
    gears = {(row, column): [] for (row, column) in gears_indexes}

    # Group the digits in the same row
    grouped_digits = []
    for line in input_matrix:
        groups = [
            list(group)
            for _, group, in groupby(line, key=lambda x: x.isdigit())
        ]
        grouped_digits.append(groups)

    # Iterate over the grouped digits and check if they are next to a gear
    for row_idx, row in enumerate(grouped_digits):
        start_column = 0

        for group in row:
            end_column = start_column + len(group)

            # Check if the group is a number
            # If not, skip it
            try:
                number = int("".join(group))

                # Create the surroundings coordinates around the number

                # Note: it does not matter if the start_column_coordinate
                # is negative, as we are not going to use it to index the
                # matrix, only to check if there is a gear next to it
                start_column_coordinate = start_column - 1
                end_column_coordinate = end_column + 1
                start_row_to_count = row_idx - 1
                end_row_to_count = row_idx + 2

                column_coordinates = np.arange(
                    start_column_coordinate, end_column_coordinate
                )
                row_coordinates = np.arange(
                    start_row_to_count, end_row_to_count
                )

                # Iterate over the coordinates and check if there is a gear
                # next to the number
                # If there is a gear, append the number to the list of
                # numbers that are next to the gear
                for row_coordinate in row_coordinates:
                    for column_coordinate in column_coordinates:
                        coordinates = (row_coordinate, column_coordinate)
                        if coordinates in gears:
                            gears[coordinates].append(number)

            except Exception as e:
                pass

            # Update the start column to the end column of the group
            start_column = end_column

    # Iterate over the gears and check if they have 2 numbers next to
    # them
    # If they do, multiply the numbers and add the result to the count
    count = 0
    for founded_gear in gears:
        if len(gears[founded_gear]) == 2:
            product = reduce(lambda x, y: x * y, gears[founded_gear])
            count += product
    return count
    print(count)


if __name__ == "__main__":
    with open("input.txt") as f:
        lines = f.readlines()

    print(f"Part 1: {part_1_using_convolutions(lines)}")
    print(f"Part 2: {part_2(lines)}")

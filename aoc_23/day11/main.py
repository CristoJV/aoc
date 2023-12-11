import logging

import numpy as np


def parse_lines(lines):
    universe = [list(line.strip()) for line in lines]
    return universe


def compute_hamming_distance(positions):
    """
    Compute the hamming distance between all pairs of positions,
    considering no repeated pairs.
    """
    diffs = np.abs(positions[:, np.newaxis] - positions)
    hamming_distances = np.sum(diffs, axis=2)
    distances = np.triu(hamming_distances)
    return distances


def update_coordinates_based_on_expansion(
    positions, expansion_rows, expansion_cols, expansion_factor
):
    """
    Update the coordinates of the positions based on the expansion
    of the universe.
    Rows and columns with no galaxies are expanded by the expansion
    factor. For instance, if the expansion factor is 2, then the
    coordinates of a galaxy found after one expanded row will be
    increased by 1, after two expanded rows will be increased by 2, and
    so on.
    """
    expansion_rows = np.asarray(expansion_rows)
    expansion_cols = np.asarray(expansion_cols)

    n_expansion_rows_before_coordinate_row = np.sum(
        expansion_rows[:, np.newaxis] < positions[:, 0], axis=0
    )

    n_expansion_cols_before_coordinate_col = np.sum(
        expansion_cols[:, np.newaxis] < positions[:, 1],
        axis=0,
    )

    positions[:, 0] += n_expansion_rows_before_coordinate_row * (
        expansion_factor - 1
    )
    positions[:, 1] += n_expansion_cols_before_coordinate_col * (
        expansion_factor - 1
    )
    return positions


def find_no_galaxy_rows_and_cols(universe):
    """
    Find the rows and columns with no galaxies.
    """
    rows_with_no_galaxies = np.where(np.all(universe != "#", axis=1))[0]
    cols_with_no_galaxies = np.where(np.all(universe != "#", axis=0))[0]
    return rows_with_no_galaxies, cols_with_no_galaxies


def part(lines, expansion_factor):
    universe = np.asarray(parse_lines(lines))
    (
        rows_with_no_galaxies,
        cols_with_no_galaxies,
    ) = find_no_galaxy_rows_and_cols(universe)

    positions = np.argwhere(universe == "#")

    positions = update_coordinates_based_on_expansion(
        positions,
        rows_with_no_galaxies,
        cols_with_no_galaxies,
        expansion_factor,
    )

    distances = compute_hamming_distance(positions)
    total_distance = np.sum(distances)
    return total_distance


if __name__ == "__main__":
    with open("input.txt") as f:
        lines = f.readlines()

    logging.basicConfig(level=logging.INFO)

    logging.info(f"Part 1: {part(lines, expansion_factor=2)}")
    logging.info(f"Part 2: {part(lines, expansion_factor=1000000)}")

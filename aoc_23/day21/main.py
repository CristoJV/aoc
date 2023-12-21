import logging

import numpy as np


def parse_lines(lines):
    garden = [list(line.strip()) for line in lines]
    garden = np.asarray(garden)
    return garden


def get_neighbors(garden, position, closed_set):
    """
    Returns a list of the top, bot, left, and right neighbors of a position,
    and that are withing the bounds of the garden, and that are not a rock.
    """
    neighbors = []
    x, y = position
    if x > 0 and garden[x - 1, y] != "#":
        neighbors.append((x - 1, y))
    if x < garden.shape[0] - 1 and garden[x + 1, y] != "#":
        neighbors.append((x + 1, y))
    if y > 0 and garden[x, y - 1] != "#":
        neighbors.append((x, y - 1))
    if y < garden.shape[1] - 1 and garden[x, y + 1] != "#":
        neighbors.append((x, y + 1))
    return neighbors


def part_1(lines, steps=6):
    garden = parse_lines(lines)
    start_position = np.argwhere(garden == "S")[0]
    logging.info(f"Start position: {start_position}")
    open_set = {tuple(start_position)}
    closed_set = set()
    for _ in range(steps):
        for position in open_set:
            new_open_set = set()
            neighbors = get_neighbors(garden, position, closed_set)
            for neighbor in neighbors:
                new_open_set.add(neighbor)
            open_set = open_set.union(new_open_set)
            open_set.remove(position)
    print_map(garden, open_set)
    return len(open_set)


def print_map(garden, open_set):
    for i in range(garden.shape[0]):
        for j in range(garden.shape[1]):
            if (i, j) in open_set:
                print("O", end="")
            else:
                print(garden[i, j], end="")
        print()


def part_2(lines):
    pass


if __name__ == "__main__":
    with open("input.txt") as f:
        lines = f.readlines()

    logging.basicConfig(level=logging.INFO)

    logging.info(f"Part 1: {part_1(lines, steps=64)}")
    logging.info(f"Part 2: {part_2(lines)}")

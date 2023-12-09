import logging
from math import lcm


def parse_lines(lines):
    series = [line.strip().split(" ") for line in lines]
    for i, serie in enumerate(series):
        for j, n in enumerate(serie):
            series[i][j] = int(n)
    return series


def difference(serie):
    diff = [j - i for i, j in zip(serie[:-1], serie[1:])]
    return diff


def check_all_zeroes(serie):
    return all([i == 0 for i in serie])


def part_1(lines):
    series = parse_lines(lines)
    next_values = []

    for serie in series:
        latest_previous = []
        diff = serie

        while not check_all_zeroes(diff):
            latest_previous.append(diff[-1])
            diff = difference(diff)
        next_value = sum(latest_previous)
        next_values.append(next_value)
    return sum(next_values)


def part_2(lines):
    series = parse_lines(lines)
    previous_values = []

    for serie in series:
        first_previous = []
        diff = serie

        while not check_all_zeroes(diff):
            first_previous.append(diff[0])
            diff = difference(diff)

        previous_value = 0
        for i in range(len(first_previous), 0, -1):
            previous_value = first_previous[i - 1] - previous_value

        previous_values.append(previous_value)

    return sum(previous_values)


if __name__ == "__main__":
    with open("input.txt") as f:
        lines = f.readlines()

    logging.basicConfig(level=logging.INFO)

    logging.info(f"Part 1: {part_1(lines)}")
    logging.info(f"Part 2: {part_2(lines)}")

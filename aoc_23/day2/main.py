from functools import reduce
from math import inf

import regex as re


def validate_bag_contents(occurrences, contents):
    for occurrence in occurrences:
        items = occurrence.split(",")
        for item in items:
            amount, color = item.strip().split(" ")
            if int(amount) > contents[color]:
                return False
    return True


def minimize_bag_contents(occurrences):
    contents = {"red": 0, "green": 0, "blue": 0}

    for occurrence in occurrences:
        items = occurrence.split(",")
        for item in items:
            amount, color = item.strip().split(" ")
            if int(amount) > contents[color]:
                contents[color] = max(contents[color], int(amount))

    return contents


def count_cubes_in_bag(lines, part=1):
    id_sum = 0
    power_sums = 0
    contents = {"red": 12, "green": 13, "blue": 14}
    for id, line in enumerate(lines):
        occurrences = line.strip().lower().split(":")[1].split(";")
        if part == 1:
            if validate_bag_contents(occurrences, contents=contents):
                id_sum += id + 1
        elif part == 2:
            minimized_contents = minimize_bag_contents(occurrences)
            power_sum = reduce(lambda x, y: x * y, minimized_contents.values())
            power_sums += power_sum
        else:
            print("Invalid part")

    if part == 1:
        return id_sum
    elif part == 2:
        return power_sums
    else:
        return 0


if __name__ == "__main__":
    with open("input.txt") as f:
        lines = f.readlines()

        print(f"Part 1: {count_cubes_in_bag(lines, part=1)}")
        print(f"Part 2: {count_cubes_in_bag(lines, part=2)}")

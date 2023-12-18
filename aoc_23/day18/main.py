import logging

import numpy as np


def parse_lines(lines):
    dig_instructions = [
        {"direction": v[0], "distance": int(v[1]), "color": v[2][1:-1]}
        for v in [line.strip().split(" ") for line in lines]
    ]
    return dig_instructions


def area_with_shoelace(coordinates):
    x = coordinates[:, 0]
    y = coordinates[:, 1]
    return 0.5 * np.abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))


def parse_instructions(instructions):
    parsed_instructions = []
    for instruction in instructions:
        color = instruction["color"]
        match color[-1]:
            case "0":
                direction = "R"
            case "1":
                direction = "D"
            case "2":
                direction = "L"
            case "3":
                direction = "U"
        distance = int("0x" + color[1:-1], 16)
        parsed_instruction = {"direction": direction, "distance": distance}
        parsed_instructions.append(parsed_instruction)
    return parsed_instructions


def part_1(
    lines,
    part,
):
    dig_instructions = parse_lines(lines)
    if part == 2:
        dig_instructions = parse_instructions(dig_instructions)
    coordinates = np.zeros((len(dig_instructions) + 1, 2), dtype=np.int64)
    coordinates[0] = [0, 0]
    perimeter = 0
    for i, dig_instruction in enumerate(dig_instructions):
        match dig_instruction["direction"]:
            case "R":
                coordinates[i + 1] = coordinates[i] + [
                    dig_instruction["distance"],
                    0,
                ]
            case "L":
                coordinates[i + 1] = coordinates[i] - [
                    dig_instruction["distance"],
                    0,
                ]
            case "U":
                coordinates[i + 1] = coordinates[i] - [
                    0,
                    dig_instruction["distance"],
                ]
            case "D":
                coordinates[i + 1] = coordinates[i] + [
                    0,
                    dig_instruction["distance"],
                ]
        perimeter += dig_instruction["distance"]

    internal_area = area_with_shoelace(np.flip(coordinates[:-1], axis=0))
    total_area = internal_area + perimeter // 2 + 1
    return int(total_area)


if __name__ == "__main__":
    with open("input.txt") as f:
        lines = f.readlines()

    logging.basicConfig(level=logging.INFO)

    logging.info(f"Part 1: {part_1(lines, part=1)}")
    logging.info(f"Part 2: {part_1(lines, part=2)}")

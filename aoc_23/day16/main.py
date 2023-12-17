import logging


def parse_lines(lines):
    mirror_map = [line.strip() for line in lines]
    return mirror_map


def print_map(mirror_map):
    print("\n".join(mirror_map))


def manhattan_distance(src, dest):
    return abs(src[0] - dest[0]) + abs(src[1] - dest[1])


def find_next_mirror(src, heading, mirror_map):
    match heading:
        case "N":
            for i in range(src[0], -1, -1):
                if mirror_map[i][src[1]] != ".":
                    return [i, src[1]]
            return [0, src[1]]
        case "S":
            for i in range(src[0], len(mirror_map)):
                if mirror_map[i][src[1]] != ".":
                    return [i, src[1]]
            return [len(mirror_map) - 1, src[1]]
        case "E":
            for i in range(src[1], len(mirror_map[0])):
                if mirror_map[src[0]][i] != ".":
                    return [src[0], i]
            return [src[0], len(mirror_map[0]) - 1]
        case "W":
            for i in range(src[1], -1, -1):
                if mirror_map[src[0]][i] != ".":
                    return [src[0], i]
            return [src[0], 0]


def travel_to(src, heading, mirror_map, checked_positions):
    def go_to_north():
        return travel_to(
            (src[0] - 1, src[1]),
            "N",
            mirror_map,
            checked_positions,
        )

    def go_to_east():
        return travel_to(
            (src[0], src[1] + 1),
            "E",
            mirror_map,
            checked_positions,
        )

    def go_to_south():
        return travel_to(
            (src[0] + 1, src[1]),
            "S",
            mirror_map,
            checked_positions,
        )

    def go_to_west():
        return travel_to(
            (src[0], src[1] - 1),
            "W",
            mirror_map,
            checked_positions,
        )

    # Exit conditions
    if src[0] < 0 or src[0] >= len(mirror_map):
        return
    if src[1] < 0 or src[1] >= len(mirror_map[0]):
        return
    if src in checked_positions:
        if heading in checked_positions[src]:
            return
        else:
            checked_positions[src].append(heading)
    else:
        checked_positions[src] = [heading]

    current_element = mirror_map[src[0]][src[1]]

    match current_element:
        case "|":
            match heading:
                case "N":
                    return go_to_north()
                case "S":
                    return go_to_south()
                case "E":
                    go_to_north()
                    go_to_south()
                    return
                case "W":
                    go_to_north()
                    go_to_south()
                    return
        case "-":
            match heading:
                case "E":
                    return go_to_east()
                case "W":
                    return go_to_west()
                case "N":
                    go_to_east()
                    go_to_west()
                    return
                case "S":
                    go_to_east()
                    go_to_west()
                    return
        case "\\":
            match heading:
                case "S":
                    return go_to_east()
                case "N":
                    return go_to_west()
                case "E":
                    return go_to_south()
                case "W":
                    return go_to_north()
        case "/":
            match heading:
                case "S":
                    return go_to_west()
                case "N":
                    return go_to_east()
                case "E":
                    return go_to_north()
                case "W":
                    return go_to_south()
        case ".":
            match heading:
                case "S":
                    return go_to_south()
                case "N":
                    return go_to_north()
                case "E":
                    return go_to_east()
                case "W":
                    return go_to_west()


def part_1(lines):
    mirror_map = parse_lines(lines)
    start_position = (0, 0)
    start_heading = "E"
    checked_positions = {}
    travel_to(start_position, start_heading, mirror_map, checked_positions)
    return len(checked_positions)


def part_2(lines):
    mirror_map = parse_lines(lines)
    max_energy = 0
    for i in range(len(mirror_map)):
        start_position = (i, 0)
        start_heading = "E"
        checked_positions = {}
        travel_to(start_position, start_heading, mirror_map, checked_positions)
        energy = len(checked_positions)
        if energy > max_energy:
            max_energy = energy
        start_position = (i, len(mirror_map[0]) - 1)
        start_heading = "W"
        checked_positions = {}
        travel_to(start_position, start_heading, mirror_map, checked_positions)
        energy = len(checked_positions)
        if energy > max_energy:
            max_energy = energy
    for j in range(len(mirror_map[0])):
        start_position = (0, j)
        start_heading = "S"
        checked_positions = {}
        travel_to(start_position, start_heading, mirror_map, checked_positions)
        energy = len(checked_positions)
        if energy > max_energy:
            max_energy = energy
        start_position = (len(mirror_map) - 1, j)
        start_heading = "N"
        checked_positions = {}
        travel_to(start_position, start_heading, mirror_map, checked_positions)
        energy = len(checked_positions)
        if energy > max_energy:
            max_energy = energy
    return max_energy


import sys

if __name__ == "__main__":
    with open("input.txt") as f:
        lines = f.readlines()
    sys.setrecursionlimit(10000)
    logging.basicConfig(level=logging.INFO)

    logging.info(f"Part 1: {part_1(lines)}")
    logging.info(f"Part 2: {part_2(lines)}")

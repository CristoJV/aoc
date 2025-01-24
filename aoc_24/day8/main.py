# pylint: disable=C0114,C0116
# pylint: disable=C0413,E0611
import sys
from pathlib import Path
from typing import List

utils_path = Path(__file__).resolve().parents[2] / "utils"
sys.path.insert(0, str(utils_path))


def parse_map(lines: List[str]):
    antenna_map = {}
    for y, line in enumerate(lines):
        for x, c in enumerate(line.strip()):
            if c.isnumeric and c.isalpha and c not in (".", "#"):
                if antenna_map.get(c, None) is None:
                    antenna_map[c] = [(x, y)]
                else:
                    antenna_map[c].append((x, y))
    return (
        antenna_map,
        (len(lines[0].strip()), len(lines)),
    )


def p1(lines: List[str]):
    antenna_map, (width, height) = parse_map(lines)

    def get_antinodes(pos1, pos2, width, height):
        increment = (pos2[0] - pos1[0], pos2[1] - pos1[1])
        x_left, y_left = (pos2[0] + increment[0], pos2[1] + increment[1])
        x_right, y_right = (pos1[0] - increment[0], pos1[1] - increment[1])
        antinodes = []
        if 0 <= x_left < width and 0 <= y_left < height:
            antinodes.append((x_left, y_left))
        if 0 <= x_right < width and 0 <= y_right < height:
            antinodes.append((x_right, y_right))
        return antinodes

    all_antinodes = []

    for _, antenna_positions in antenna_map.items():
        for idx, pos1 in enumerate(antenna_positions):
            for jdx, pos2 in enumerate(antenna_positions):
                if idx < jdx:
                    antinodes = get_antinodes(
                        pos1, pos2, width=width, height=height
                    )
                    all_antinodes.extend(antinodes)

    return len(set(all_antinodes))


def p2(lines: List[str]):
    def get_antinodes(pos1, pos2, width, height):
        increment = (pos2[0] - pos1[0], pos2[1] - pos1[1])

        iteration = 0
        continue_iterating_left = True
        continue_iterating_right = True
        antinodes = []
        while continue_iterating_left or continue_iterating_right:
            if continue_iterating_left:
                x_left, y_left = (
                    pos2[0] + iteration * increment[0],
                    pos2[1] + iteration * increment[1],
                )
                if 0 <= x_left < width and 0 <= y_left < height:
                    antinodes.append((x_left, y_left))
                else:
                    continue_iterating_left = False
            if continue_iterating_right:
                x_right, y_right = (
                    pos1[0] - iteration * increment[0],
                    pos1[1] - iteration * increment[1],
                )
                if 0 <= x_right < width and 0 <= y_right < height:
                    antinodes.append((x_right, y_right))
                else:
                    continue_iterating_right = False
            iteration += 1
        return antinodes

    antenna_map, (width, height) = parse_map(lines)

    all_antinodes = []

    for _, antenna_positions in antenna_map.items():
        for idx, pos1 in enumerate(antenna_positions):
            for jdx, pos2 in enumerate(antenna_positions):
                if idx < jdx:
                    antinodes = get_antinodes(
                        pos1, pos2, width=width, height=height
                    )
                    all_antinodes.extend(antinodes)

    return len(set(all_antinodes))


if __name__ == "__main__":
    with open("input.txt", encoding="utf8") as f:
        input_lines = f.readlines()
        print(f"First part: {p1(input_lines)}")
        print(f"Second part: {p2(input_lines)}")

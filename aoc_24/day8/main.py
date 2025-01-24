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
            if c.isalnum() and c not in (".", "#"):
                antenna_map.setdefault(c, []).append((x, y))
    return (
        antenna_map,
        (len(lines[0].strip()), len(lines)),
    )


def get_antinodes(
    pos1,
    pos2,
    width,
    height,
    count_antenna_positions: bool = False,
    unbounded: bool = False,
):
    increment = (pos2[0] - pos1[0], pos2[1] - pos1[1])
    keep_left = True
    keep_right = True
    antinodes = []

    iteration = 0 if count_antenna_positions else 1

    while keep_left or keep_right:

        if keep_left:
            x_left = pos2[0] + iteration * increment[0]
            y_left = pos2[1] + iteration * increment[1]

            if 0 <= x_left < width and 0 <= y_left < height:
                antinodes.append((x_left, y_left))
            else:
                keep_left = False

        if keep_right:
            x_right = pos1[0] - iteration * increment[0]
            y_right = pos1[1] - iteration * increment[1]

            if 0 <= x_right < width and 0 <= y_right < height:
                antinodes.append((x_right, y_right))
            else:
                keep_right = False

        iteration += 1
        if not unbounded:
            break
    return antinodes


def count_antinodes(
    lines: List[str], count_antenna_positions=False, unbounded=False
):
    antenna_map, (width, height) = parse_map(lines)

    all_antinodes = []

    for _, antenna_positions in antenna_map.items():
        for idx, pos1 in enumerate(antenna_positions):
            for jdx, pos2 in enumerate(antenna_positions):
                if idx < jdx:
                    antinodes = get_antinodes(
                        pos1,
                        pos2,
                        width=width,
                        height=height,
                        count_antenna_positions=count_antenna_positions,
                        unbounded=unbounded,
                    )
                    all_antinodes.extend(antinodes)

    return len(set(all_antinodes))


def p1(lines: List[str]):
    return count_antinodes(
        lines, count_antenna_positions=False, unbounded=False
    )


def p2(lines: List[str]):
    return count_antinodes(lines, count_antenna_positions=True, unbounded=True)


if __name__ == "__main__":
    with open("input.txt", encoding="utf8") as f:
        input_lines = f.readlines()
        print(f"First part: {p1(input_lines)}")
        print(f"Second part: {p2(input_lines)}")

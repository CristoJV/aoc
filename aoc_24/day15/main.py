# pylint: disable=C0114,C0116
# pylint: disable=C0413,E0611
import sys
from pathlib import Path
from typing import Dict, List

import numpy as np

utils_path = Path(__file__).resolve().parents[2] / "utils"
sys.path.insert(0, str(utils_path))


def parse_warehouse(lines: List[str]):
    lines = "".join(lines)
    lines = lines.split("\n\n")
    warehouse, movements = lines[0], lines[1]
    warehouse_rows = warehouse.split("\n")
    warehouse_map: Dict[complex, str] = {}
    robot_loc = 0
    height = len(warehouse_rows)
    width = len(warehouse_rows[0])
    for j, row in enumerate(warehouse_rows):
        for i, block in enumerate(list(row)):
            if block == "@":
                robot_loc = i + 1j * j
            warehouse_map[i + 1j * j] = block
    parsed_movements: List[complex] = []
    for movement in movements:
        if movement == ">":
            parsed_movements.append(1)
        elif movement == "<":
            parsed_movements.append(-1)
        elif movement == "v":
            parsed_movements.append(1j)
        elif movement == "^":
            parsed_movements.append(-1j)
        else:
            print(f"Unrecognized movement {movement}")
    return warehouse_map, parsed_movements, robot_loc, width, height


WALL = "#"
BOX = "O"


def step(warehouse: Dict[complex, str], pos, movement):
    next_pos = pos + movement
    next_block = warehouse[next_pos]
    if next_block == "#":
        return False
    elif next_block == ".":
        return True
    elif next_block == "O":
        continue_pos = step(warehouse, next_pos, movement)
        if continue_pos:
            warehouse[next_pos] = "."
            warehouse[next_pos + movement] = "O"
            return True
    return False


def plot_map(warehouse, width, height):
    img = np.zeros((height, width, 3))
    for pos, block in warehouse.items():
        if block == "#":
            img[int(pos.imag), int(pos.real), :] = [1, 0, 0]
        elif block == "O":
            img[int(pos.imag), int(pos.real), :] = [1, 1, 0]
        elif block == "@":
            img[int(pos.imag), int(pos.real), :] = [0, 0, 1]
    return img


def p1(lines: List[str]):
    warehouse, movements, robot_loc, width, height = parse_warehouse(lines)
    for movement in movements:
        continue_moving = step(warehouse, robot_loc, movement)
        if continue_moving:
            warehouse[robot_loc] = "."
            robot_loc += movement
            warehouse[robot_loc] = "@"
    boxes = [k for k, v in warehouse.items() if v == "O"]
    gps_coordinates = sum([100 * box.imag + box.real for box in boxes])
    return gps_coordinates


def p2(lines: List[str]):
    pass


if __name__ == "__main__":
    testing: bool = False
    with open(
        "input.txt" if not testing else "test.txt", encoding="utf8"
    ) as f:
        input_lines = f.readlines()
        print(f"First part: {p1(input_lines)}")
        print(f"Second part: {p2(input_lines)}")

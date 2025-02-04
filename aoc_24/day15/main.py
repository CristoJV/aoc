# pylint: disable=C0114,C0116
# pylint: disable=C0413,E0611
import sys
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np

utils_path = Path(__file__).resolve().parents[2] / "utils"
sys.path.insert(0, str(utils_path))

MOVEMENT_MAP: Dict[str, complex] = {
    ">": 1,
    "<": -1,
    "^": -1j,
    "v": 1j,
}


def parse_movement_instructions(movements_str: str) -> List[complex]:
    """
    Parse the movements string into a list of complex offsets
    based on MOVEMENT_MAP.
    """
    return [MOVEMENT_MAP[ch] for ch in movements_str if ch in MOVEMENT_MAP]


def parse_warehouse(
    lines: List[str], expanded: bool = False
) -> Tuple[Dict[complex, str], List[complex], complex]:
    full_text = "".join(lines).split("\n\n")
    warehouse_str, movement_instructions_str = full_text[0], full_text[1]

    warehouse_rows = warehouse_str.split("\n")

    # Parse movements
    movement_instructions = parse_movement_instructions(
        movement_instructions_str
    )

    warehouse_map: Dict[complex, str] = {}
    robot_pos: complex = 0

    if not expanded:
        # Standard parsing
        for j, row in enumerate(warehouse_rows):
            for i, block in enumerate(row):
                pos = complex(i, j)
                warehouse_map[pos] = block
                if block == "@":
                    robot_pos = pos
    else:
        # Expanded parsing
        for j, row in enumerate(warehouse_rows):
            for i, block in enumerate(row):
                left_pos = complex(i * 2, j)
                right_pos = left_pos + 1

                if block == "@":
                    warehouse_map[left_pos] = "@"
                    warehouse_map[right_pos] = "."
                    robot_pos = left_pos
                elif block == "O":
                    warehouse_map[left_pos] = "["
                    warehouse_map[right_pos] = "]"
                else:
                    warehouse_map[left_pos] = block
                    warehouse_map[right_pos] = block

    return warehouse_map, movement_instructions, robot_pos


def step(warehouse: Dict[complex, str], pos, movement) -> List[complex]:
    next_pos = pos + movement
    next_block = warehouse.get(next_pos, "#")

    if next_block == "#":
        return False, []

    if next_block == ".":
        return True, [pos]

    if next_block == "O":
        can_move, positions_to_update = step(warehouse, next_pos, movement)
        if can_move:
            positions_to_update.append(pos)
            return True, positions_to_update
        return False, []

    if next_block in ["[", "]"]:
        if movement in [1, -1]:
            can_move, positions_to_update = step(warehouse, next_pos, movement)
            if can_move:
                positions_to_update.append(pos)
                return True, positions_to_update
            return False, []
        else:  # movement in [1j, -1j] (down or up)
            if next_block == "[":
                next_pos_left = next_pos
                next_pos_right = next_pos + 1
            else:
                next_pos_left = next_pos - 1
                next_pos_right = next_pos

            can_move_left, positions_to_update_left = step(
                warehouse, next_pos_left, movement
            )
            can_move_right, positions_to_update_right = step(
                warehouse, next_pos_right, movement
            )

            if can_move_left and can_move_right:
                positions_to_update = list(
                    set(positions_to_update_left + positions_to_update_right)
                )
                positions_to_update.append(pos)
                return True, positions_to_update
            return False, []
    return False, []


def move(
    warehouse: Dict[complex, str], positions_to_update, movement, robot_pos
):
    if movement == -1j:  # Up
        # Move from top to bottom
        positions_to_update.sort(key=lambda x: x.imag, reverse=False)
    elif movement == 1j:  # Down
        # Move from bottom to top
        positions_to_update.sort(key=lambda x: x.imag, reverse=True)
    elif movement == -1:  # Left
        # Move from left to right
        positions_to_update.sort(key=lambda x: x.real, reverse=False)
    elif movement == 1:  # Right
        # Move from right to left
        positions_to_update.sort(key=lambda x: x.real, reverse=True)

    for block_pos in positions_to_update:
        current_block = warehouse[block_pos]
        new_pos = block_pos + movement

        warehouse[block_pos] = "."
        warehouse[new_pos] = current_block

        if current_block == "@":
            robot_pos += movement

    return robot_pos


def plot_map(warehouse, width, height):
    img = np.zeros((height, width, 3), dtype=float)

    color_map = {
        "#": [1, 0, 0],  # Red
        "O": [1, 1, 0],  # Yellow
        "@": [0, 0, 1],  # Blue
        "[": [0, 1, 0],  # Green
        "]": [1, 1, 0],  # Yellow
        ".": [0, 0, 0],  # Black
    }

    for pos, block in warehouse.items():
        x, y = int(pos.real), int(pos.imag)
        if block in color_map:
            img[y, x, :] = color_map[block]

    return img


def p1(lines: List[str]):
    warehouse_map, movements, robot_pos = parse_warehouse(lines)

    for movement in movements:
        can_move, positions_to_update = step(
            warehouse_map, robot_pos, movement
        )
        if can_move:
            robot_pos = move(
                warehouse_map, positions_to_update, movement, robot_pos
            )

    # Gather box locations
    boxes = [pos for pos, v in warehouse_map.items() if v == "O"]
    gps_coordinates = sum(
        [100 * int(box.imag) + int(box.real) for box in boxes]
    )
    return int(gps_coordinates)


def p2(lines: List[str]):
    warehouse_map, movements, robot_pos = parse_warehouse(lines, expanded=True)

    for movement in movements:
        can_move, positions_to_update = step(
            warehouse_map, robot_pos, movement
        )
        if can_move:
            robot_pos = move(
                warehouse_map, positions_to_update, movement, robot_pos
            )

    # Gather box locations (left bracket)
    left_brackets = [pos for pos, v in warehouse_map.items() if v == "["]
    gps_coordinates = sum(
        [100 * int(b.imag) + int(b.real) for b in left_brackets]
    )

    return int(gps_coordinates)


if __name__ == "__main__":
    testing: bool = False
    with open(
        "input.txt" if not testing else "test.txt", encoding="utf8"
    ) as f:
        input_lines = f.readlines()
        print(f"First part: {p1(input_lines)}")
        print(f"Second part: {p2(input_lines)}")

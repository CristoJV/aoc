# pylint: disable=C0114,C0116
# pylint: disable=C0413,E0611
import sys
from collections import namedtuple
from pathlib import Path
from typing import Dict, List, Set

utils_path = Path(__file__).resolve().parents[2] / "utils"
sys.path.insert(0, str(utils_path))


Limits = namedtuple("Limits", ["width", "height"])


def parse_topographic_map(lines: List[str]):
    topographic_map: Dict[complex, int] = {}
    trail_heads: List[complex] = []
    for jdx, line in enumerate(lines):
        for idx, height in enumerate(list(line.strip())):
            height = int(height)
            coords = complex(idx, jdx)
            topographic_map[coords] = height
            if height == 0:
                trail_heads.append(coords)
    return (
        topographic_map,
        trail_heads,
        Limits(len(lines[0].strip()), len(lines)),
    )


def get_valid_neighbors_coords(coords: complex, limits: Limits):

    top = 1j
    right = 1
    bot = -1j
    left = -1
    directions = [top, right, bot, left]

    def is_within_bounds(coords):
        return (
            0 <= coords.real < limits.width
            and 0 <= coords.imag < limits.height
        )

    return list(
        filter(
            is_within_bounds, [coords + direction for direction in directions]
        )
    )


def find_paths(
    path: List[complex], topographic_map: Dict[complex, int], limits: Limits
) -> List[List[complex]]:
    last_step_coords = path[-1]
    last_step_height = topographic_map.get(last_step_coords)
    if last_step_height == 9:
        return [path]
    paths: List[List[complex]] = []

    neighbors_coords = get_valid_neighbors_coords(last_step_coords, limits)
    for neighbor_coords in neighbors_coords:
        if topographic_map[neighbor_coords] == last_step_height + 1:
            next_path = path.copy() + [neighbor_coords]
            following_paths = find_paths(next_path, topographic_map, limits)
            if following_paths:
                paths.extend(following_paths)
    return paths


def p1(lines: List[str]):
    topographic_map, trail_heads, limits = parse_topographic_map(lines)

    trail_ends_count: int = 0
    for trail_head in trail_heads:
        paths = find_paths([trail_head], topographic_map, limits)
        trail_ends_set: Set[complex] = set()
        for path in paths:
            trail_ends_set.add(path[-1])

        trail_ends_count += len(trail_ends_set)

    return trail_ends_count


if __name__ == "__main__":
    with open("input.txt", encoding="utf8") as f:
        input_lines = f.readlines()
        print(f"First part: {p1(input_lines)}")
        print(f"Second part: {p2(input_lines)}")

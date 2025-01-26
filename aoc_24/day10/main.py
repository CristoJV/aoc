# pylint: disable=C0114,C0116
# pylint: disable=C0413,E0611
import sys
from dataclasses import dataclass
from functools import partial, wraps
from pathlib import Path
from typing import Dict, List, Set

utils_path = Path(__file__).resolve().parents[2] / "utils"
sys.path.insert(0, str(utils_path))
from profile import timeit


def call_counter(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        wrapper.counter += 1
        return func(*args, **kwargs)

    wrapper.counter = 0
    return wrapper


@dataclass(frozen=True)
class Limits:
    width: int
    height: int


def parse_topographic_map(lines: List[str]):

    topographic_map: Dict[complex, int] = {}
    trail_heads: List[complex] = []

    for jdx, line in enumerate(lines):
        for idx, map_height in enumerate(list(line.strip())):
            map_height = int(map_height)
            coords = complex(idx, jdx)
            topographic_map[coords] = map_height
            if map_height == 0:
                trail_heads.append(coords)

    map_height = len(lines)
    map_width = len(lines[0].strip())
    return (
        topographic_map,
        trail_heads,
        Limits(map_width, map_height),
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

    neighbors_coords = []
    for d in directions:
        neighbor_coords = coords + d
        if is_within_bounds(neighbor_coords):
            neighbors_coords.append(neighbor_coords)

    return neighbors_coords


@call_counter
def find_paths(
    coord: complex, topographic_map: Dict[complex, int], limits: Limits
) -> List[List[complex]]:

    current_height = topographic_map[coord]
    if current_height == 9:
        return [[coord]]

    all_paths_from_coord: List[List[complex]] = []
    for neighbor in get_valid_neighbors_coords(coord, limits):
        if topographic_map[neighbor] == current_height + 1:
            sub_paths = find_paths(neighbor, topographic_map, limits)
            for sub_path in sub_paths:
                all_paths_from_coord.append([coord] + sub_path)

    return all_paths_from_coord


@call_counter
def find_paths_memoized(
    coord: complex,
    topographic_map: Dict[complex, int],
    limits: Limits,
    memo: Dict[complex, List[List[complex]]],
) -> List[List[complex]]:

    if coord in memo:
        return memo[coord]

    current_height = topographic_map.get(coord)

    if current_height == 9:
        memo[coord] = [[coord]]
        return memo[coord]

    all_paths_from_coord: List[List[complex]] = []

    for neighbor_coords in get_valid_neighbors_coords(coord, limits):
        if topographic_map[neighbor_coords] == current_height + 1:
            sub_paths = find_paths_memoized(
                neighbor_coords, topographic_map, limits, memo
            )
            for sub_path in sub_paths:
                all_paths_from_coord.append([coord] + sub_path)

    memo[coord] = all_paths_from_coord
    return all_paths_from_coord


@timeit(repeats=1)
def p1(lines: List[str], use_memoization: bool):

    if use_memoization:
        memo = {}
        find_paths_fn = partial(find_paths_memoized, memo=memo)
        counter_func = find_paths_memoized  # Reference the original function
    else:
        find_paths_fn = find_paths
        counter_func = find_paths

    topographic_map, trail_heads, limits = parse_topographic_map(lines)

    trail_ends_count: int = 0
    for trail_head in trail_heads:
        paths_from_head = find_paths_fn(trail_head, topographic_map, limits)
        distinct_trail_ends: Set[complex] = {
            path[-1] for path in paths_from_head
        }
        trail_ends_count += len(distinct_trail_ends)
    print(f"Total number of iterations: {counter_func.counter}")
    return trail_ends_count


@timeit(repeats=1)
def p2(lines: List[str], use_memoization: bool):

    if use_memoization:
        memo = {}
        find_paths_fn = partial(find_paths_memoized, memo=memo)
        counter_func = find_paths_memoized  # Reference the original function
    else:
        find_paths_fn = find_paths
        counter_func = find_paths

    topographic_map, trail_heads, limits = parse_topographic_map(lines)
    total_paths_count = 0
    for trail_head in trail_heads:
        paths_from_head = find_paths_fn(trail_head, topographic_map, limits)
        total_paths_count += len(paths_from_head)

    print(f"Total number of iterations: {counter_func.counter}")
    return total_paths_count


if __name__ == "__main__":
    with open("input.txt", encoding="utf8") as f:
        input_lines = f.readlines()
        print(f"First part: {p1(input_lines, use_memoization=True)}")
        print(f"Second part: {p2(input_lines, use_memoization=True)}")

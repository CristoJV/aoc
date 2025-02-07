# pylint: disable=C0114,C0116
# pylint: disable=C0413,E0611
import heapq
import queue
import sys
from math import inf
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np

utils_path = Path(__file__).resolve().parents[2] / "utils"
sys.path.insert(0, str(utils_path))


def parse_corrupted_locations(lines: List[str]):
    corrupted_locations = [(line.strip().split(",")) for line in lines]
    corrupted_locations = [
        (int(pos[0]), int(pos[1])) for pos in corrupted_locations
    ]
    return corrupted_locations


def is_within_bounds(pos: Tuple[int, int], limits: Tuple[int, int]):
    return 0 <= pos[0] < limits[0] and 0 <= pos[1] < limits[1]


def get_neighbor_costs(
    pos: Tuple[int, int],
    corrupted_poss: List[Tuple[int, int]],
    limits: Tuple[int, int],
):

    directions = [
        (0, -1),  # Top
        (1, 0),  # Right
        (0, 1),  # Bot
        (-1, 0),  # Left
    ]
    neighbor_costs: List[Tuple[int, Tuple[int, int]]] = []
    for direction in directions:
        neighbor_pos = (pos[0] + direction[0], pos[1] + direction[1])
        if (
            is_within_bounds(neighbor_pos, limits)
            and neighbor_pos not in corrupted_poss
        ):
            neighbor_costs.append((1, neighbor_pos))
    return neighbor_costs


def dijistra(
    start_pos: Tuple[int, int],
    corrupted_poss: List[List[int]],
    limits: Tuple[int, int],
) -> Dict[Tuple[int, int], Tuple[int, int]]:
    costs: Dict[Tuple[int, int]] = {}
    path: Dict[Tuple[int, int], Tuple[int, int]] = {}
    priority_queue: queue = []
    costs[start_pos] = 0

    heapq.heappush(priority_queue, (0, start_pos))

    while priority_queue:
        cost_to_pos, pos = heapq.heappop(priority_queue)
        # visited.append(pos)
        if costs[pos] < cost_to_pos:
            continue
        for neighbor_step_cost, neighbor_pos in get_neighbor_costs(
            pos, corrupted_poss=corrupted_poss, limits=limits
        ):
            neighbor_cost = costs.get(neighbor_pos, inf)
            alternative_cost = cost_to_pos + neighbor_step_cost
            if neighbor_cost > alternative_cost:
                costs[neighbor_pos] = alternative_cost
                heapq.heappush(
                    priority_queue, (alternative_cost, neighbor_pos)
                )
                path[neighbor_pos] = pos
    return path


def retrieve_best_path(paths, start_pos, end_pos):
    best_path = []
    if end_pos not in paths:
        return False, []
    pos = end_pos
    best_path.append(end_pos)
    while pos != start_pos:
        pos = paths[pos]
        best_path.append(pos)
    best_path.append(start_pos)
    best_path.reverse()
    return True, best_path


def plot_map(corrupted_positions, limits):
    memory_map = np.zeros((limits[0], limits[1], 3))
    for corrupted_pos in corrupted_positions:
        if is_within_bounds(corrupted_pos, limits):
            memory_map[corrupted_pos[1], corrupted_pos[0], :] = [1, 0, 0]
    return memory_map


def p1(lines: List[str], limits=(7, 7), fallen_bytes: int = 1024):
    corrupted_positions = parse_corrupted_locations(lines)
    paths = dijistra((0, 0), corrupted_positions[:fallen_bytes], limits=limits)
    is_there_a_path, path = retrieve_best_path(
        paths, start_pos=(0, 0), end_pos=(limits[0] - 1, limits[1] - 1)
    )
    return len(path) - 2


def p2(lines: List[str], limits: Tuple[int, int], fallen_bytes: int):
    corrupted_positions = parse_corrupted_locations(lines)
    start_pos = (0, 0)
    end_pos = (limits[0] - 1, limits[1] - 1)
    paths = dijistra(
        start_pos, corrupted_positions[:fallen_bytes], limits=limits
    )
    is_there_a_path, path = retrieve_best_path(
        paths, start_pos, end_pos=end_pos
    )
    idx = fallen_bytes
    while is_there_a_path:
        idx += 1
        if idx >= len(corrupted_positions):
            return corrupted_positions[-1]
        if corrupted_positions[idx] in path:
            paths = dijistra(
                start_pos, corrupted_positions[: idx + 1], limits=limits
            )
            is_there_a_path, path = retrieve_best_path(
                paths, start_pos, end_pos=end_pos
            )
    return corrupted_positions[idx]


if __name__ == "__main__":
    testing: bool = False
    limits = (71, 71)
    fallen_bytes = 1024
    with open(
        "input.txt" if not testing else "test.txt", encoding="utf8"
    ) as f:
        input_lines = f.readlines()
        print(f"First part: {p1(input_lines, limits, fallen_bytes)}")
        print(f"Second part: {p2(input_lines, limits, fallen_bytes)}")

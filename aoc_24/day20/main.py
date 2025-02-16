# pylint: disable=C0114,C0116
# pylint: disable=C0413,E0611
import math
import sys
from enum import Enum
from pathlib import Path
from typing import List, Tuple

utils_path = Path(__file__).resolve().parents[2] / "utils"
sys.path.insert(0, str(utils_path))
from profile import timeit


class Block(Enum):
    WALL = 0
    TRACK = 1


DIRECTIONS = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # Top  # Right  # Bot  # Left


def parse_racetrack(
    lines: List[str],
) -> Tuple[List[List[Block]], Tuple[int, int], Tuple[int, int]]:
    height = len(lines)
    width = len(lines[0].strip())
    racetrack: List[List[Block]] = [
        [0 for _ in range(width)] for _ in range(height)
    ]
    start: Tuple[int, int] = (0, 0)
    end: Tuple[int, int] = (0, 0)
    for j, row in enumerate(lines):
        if j < height:
            for i, col in enumerate(row):
                if i < width:
                    racetrack[j][i] = Block.WALL if col == "#" else Block.TRACK
                    if col == "S":
                        start = (j, i)
                    elif col == "E":
                        end = (j, i)
    return racetrack, start, end


import heapq


def is_within_bounds(pos: Tuple[int, int], height: int, width: int) -> bool:
    return 0 <= pos[0] < height and 0 <= pos[1] < width


def get_neighbors(pos: Tuple[int, int], racetrack: List[List[Block]]):
    height, width = len(racetrack), len(racetrack[0])

    neighbors: List[Tuple[int, int]] = []
    for direction in DIRECTIONS:
        neighbor_pos: Tuple[int, int] = (
            pos[0] + direction[0],
            pos[1] + direction[1],
        )
        if (
            is_within_bounds(neighbor_pos, height, width)
            and racetrack[neighbor_pos[0]][neighbor_pos[1]] == Block.TRACK
        ):
            neighbors.append(neighbor_pos)
    return neighbors


def djistra(
    racetrack: List[List[Block]], start: Tuple[int, int]
) -> List[List[int]]:
    height, width = len(racetrack), len(racetrack[0])
    priority_queue: List[Tuple[int, Tuple[int, int]]] = []
    visited: List[Tuple[int, int]] = []
    costs: List[List[int]] = [
        [math.inf for _ in range(width)] for _ in range(height)
    ]

    heapq.heappush(priority_queue, (0, start))
    costs[start[0]][start[1]] = 0

    while priority_queue:
        cost, pos = heapq.heappop(priority_queue)
        visited.append(pos)

        for neighbor_pos in get_neighbors(pos, racetrack):
            if neighbor_pos not in visited:
                neighbor_step_cost: int = 1
                neighbor_pos_y = neighbor_pos[0]
                neighbor_pos_x = neighbor_pos[1]
                if (
                    cost + neighbor_step_cost
                    < costs[neighbor_pos_y][neighbor_pos_x]
                ):
                    costs[neighbor_pos_y][neighbor_pos_x] = (
                        cost + neighbor_step_cost
                    )
                    heapq.heappush(
                        priority_queue,
                        (costs[neighbor_pos_y][neighbor_pos_x], neighbor_pos),
                    )

    return costs


def detect_alleys(
    racetrack: List[List[Block]],
) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
    height, width = len(racetrack), len(racetrack[0])
    alleys: List[Tuple[Tuple[int, int], Tuple[int, int]]] = []
    for j, row in enumerate(racetrack):
        for i, col in enumerate(row):
            if col == Block.WALL:
                # Horizontal alleys
                left_conn = (j, i - 1)
                right_conn = (j, i + 1)
                if (
                    is_within_bounds(left_conn, height, width)
                    and racetrack[left_conn[0]][left_conn[1]] == Block.TRACK
                    and is_within_bounds(right_conn, height, width)
                    and racetrack[right_conn[0]][right_conn[1]] == Block.TRACK
                ):
                    alleys.append((left_conn, right_conn))

                # Vertical alleys
                top_conn = (j - 1, i)
                bot_conn = (j + 1, i)
                if (
                    is_within_bounds(top_conn, height, width)
                    and racetrack[top_conn[0]][top_conn[1]] == Block.TRACK
                    and is_within_bounds(bot_conn, height, width)
                    and racetrack[bot_conn[0]][bot_conn[1]] == Block.TRACK
                ):
                    alleys.append((top_conn, bot_conn))
    return alleys


def p1(lines: List[str]):
    racetrack, start, end = parse_racetrack(lines)
    alleys = detect_alleys(racetrack)
    costs_from_start: List[List[int]] = djistra(racetrack, start)
    costs_from_end: List[List[int]] = djistra(racetrack, end)
    min_cost_without_cheats = costs_from_start[end[0]][end[1]]
    num_saves_greater_than_100: int = 0
    for alley in alleys:
        # From start to end
        alley_a, alley_b = alley
        ay, ax = alley_a
        by, bx = alley_b
        cost_a_from_start = costs_from_start[ay][ax]
        cost_b_from_end = costs_from_end[by][bx]
        cost_ab = cost_a_from_start + cost_b_from_end + 2

        cost_a_from_end = costs_from_end[ay][ax]
        cost_b_from_start = costs_from_start[by][bx]
        cost_ba = cost_a_from_end + cost_b_from_start + 2
        min_cost = min(cost_ab, cost_ba)
        diff = min_cost_without_cheats - min_cost
        if diff >= 100:
            num_saves_greater_than_100 += 1
    return num_saves_greater_than_100


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

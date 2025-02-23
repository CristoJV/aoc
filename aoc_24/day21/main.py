# pylint: disable=C0114,C0116
# pylint: disable=C0413,E0611
import heapq
import math
import sys
from enum import Enum
from pathlib import Path
from typing import Dict, List, NamedTuple, Tuple

utils_path = Path(__file__).resolve().parents[2] / "utils"
sys.path.insert(0, str(utils_path))
from profile import timeit


class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3
    START = -1


direction2arrow: Dict[Direction, str] = {
    Direction.UP: "^",
    Direction.RIGHT: ">",
    Direction.DOWN: "v",
    Direction.LEFT: "<",
    Direction.START: ".",
}


num2pos: Dict[str, Tuple[int, int]] = {
    "A": (3, 2),
    "0": (3, 1),
    "void": (3, 0),
    "1": (2, 0),
    "2": (2, 1),
    "3": (2, 2),
    "4": (1, 0),
    "5": (1, 1),
    "6": (1, 2),
    "7": (0, 0),
    "8": (0, 1),
    "9": (0, 2),
}
pos2num: Dict[Tuple[int, int], str] = {
    val: key for key, val in num2pos.items()
}

arrow2pos: Dict[str, Tuple[int, int]] = {
    "void": (0, 0),
    "^": (0, 1),
    "A": (0, 2),
    "<": (1, 0),
    "v": (1, 1),
    ">": (1, 2),
}

pos2arrow: Dict[Tuple[int, int], str] = {
    val: key for key, val in arrow2pos.items()
}


def is_valid(pos: Tuple[int, int], graph: Dict[Tuple[int, int], str]):
    return pos in graph and graph[pos] != "void"


dir2direction: Dict[Tuple[int, int], Direction] = {
    (-1, 0): Direction.UP,  # UP
    (0, 1): Direction.RIGHT,  # RIGHT
    (1, 0): Direction.DOWN,  # DOWN
    (0, -1): Direction.LEFT,  # LEFT
}


def get_neighbors(
    pos: Tuple[int, int],
    in_direction: Direction,
    graph: Dict[Tuple[int, int], str],
):
    dir2cost: Dict[Tuple[int, int], int] = {
        (0, -1): 4,  # LEFT
        (1, 0): 3,  # DOWN
        (-1, 0): 2,  # UP
        (0, 1): 1,  # RIGHT
    }
    neighbors: List[Tuple[int, int, int, int]] = []
    for direction, cost in dir2cost.items():
        new_pos = (pos[0] + direction[0], pos[1] + direction[1])
        if is_valid(new_pos, graph):
            cost = 0 if in_direction == direction else cost
            neighbors.append(
                (cost,) + (new_pos,) + (dir2direction[direction],)
            )
    return neighbors


def djistra(current_pos: Tuple[int, int], graph: Dict[Tuple[int, int], str]):
    queue: List[Tuple[int, Tuple[int, int, Direction]]] = []
    costs: Dict[Tuple[int, int], int] = {}
    parents: Dict[Tuple[int, int, Direction], Tuple[int, int, Direction]] = {}

    heapq.heappush(queue, (0, current_pos, Direction.START))
    costs[current_pos] = 0

    while queue:
        cost, current_pos, current_direction = heapq.heappop(queue)

        for neighbor_cost, neighbor_pos, neighbor_direction in get_neighbors(
            current_pos, current_direction, graph
        ):
            alt_neighbor_cost = cost + neighbor_cost
            if (
                neighbor_pos not in costs
                or alt_neighbor_cost < costs[neighbor_pos]
            ):
                costs[neighbor_pos] = alt_neighbor_cost
                parents[neighbor_pos + (neighbor_direction,)] = current_pos + (
                    current_direction,
                )
                heapq.heappush(
                    queue,
                    (alt_neighbor_cost, neighbor_pos, neighbor_direction),
                )
    return parents


def get_path_from_a_to_b(num_a, num_b, parents_a, key2pos):
    path_from_a_to_b = []
    pos_a = key2pos[num_a]
    pos_b = key2pos[num_b]

    for direction in Direction:
        node = pos_b + (direction,)
        if node in parents_a:
            while node[:2] != pos_a:
                path_from_a_to_b.append(direction2arrow[node[2]])
                node = parents_a[node]

    return "".join(reversed(path_from_a_to_b))


def get_all_paths_from_a(num_a, num_bs, parents_a, key2pos):
    paths_from_a = {}
    for num_b in num_bs:
        paths_from_a[num_b] = get_path_from_a_to_b(
            num_a, num_b, parents_a, key2pos
        )
    return paths_from_a


def get_all_paths(num_as, num_bs, graph, key2pos):
    paths: Dict[str, Dict[str, str]] = {}
    for num_a in num_as:
        parents = djistra(key2pos[num_a], graph)
        paths_from_a = get_all_paths_from_a(num_a, num_bs, parents, key2pos)
        paths[num_a] = paths_from_a
    return paths


def p1(lines: List[str]):
    num_as = list(num2pos.keys())
    num_as.remove("void")
    num_bs = [num for num in num_as]
    num_paths = get_all_paths(num_as, num_bs, pos2num, num2pos)
    arrow_as = list(arrow2pos.keys())
    arrow_as.remove("void")
    arrow_bs = [num for num in arrow_as]
    arrow_paths = get_all_paths(arrow_as, arrow_bs, pos2arrow, arrow2pos)
    for key, arrow_path in arrow_paths.items():
        print(key)
        print(arrow_path)
    score = 0
    for original_code in lines:
        original_code = "A" + original_code.strip()
        code = original_code

        expanded_code = "A"
        insert_indexes: List[int] = []
        for i in range(len(code) - 1):
            a = code[i]
            b = code[i + 1]
            expanded_code = expanded_code + num_paths[a][b] + "A"
        code = expanded_code
        print(code[1:])
        for i in range(2):
            expanded_code = "A"
            for i in range(len(code) - 1):
                a = code[i]
                b = code[i + 1]
                expanded_code = expanded_code + arrow_paths[a][b] + "A"
            code = expanded_code
            print(code[1:])
        code_number = int("".join([c for c in original_code if c.isdigit()]))
        code_complexity = len(code[1:]) * code_number
        print(len(code[1:]), code_number)
        score += code_complexity
    return score


def p2(lines: List[str]):
    pass


if __name__ == "__main__":
    testing: bool = True
    with open(
        "input.txt" if not testing else "test.txt", encoding="utf8"
    ) as f:
        input_lines = f.readlines()
        print(f"First part: {p1(input_lines)}")
        print(f"Second part: {p2(input_lines)}")

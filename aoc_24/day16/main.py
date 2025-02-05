# pylint: disable=C0114,C0116
# pylint: disable=C0413,E0611
import sys
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from queue import PriorityQueue
from typing import Dict, List, Set, Tuple

from numpy import inf

utils_path = Path(__file__).resolve().parents[2] / "utils"
sys.path.insert(0, str(utils_path))
from profile import timeit


def parse_maze(lines: List[str]):
    maze: Dict[complex, str] = {}
    str_pos: complex = 0
    end_pos: complex = 0
    for (
        j,
        row,
    ) in enumerate(lines):
        for i, block in enumerate(row):
            pos = complex(i, j)
            maze[pos] = block
            if block == "S":
                str_pos = pos
            elif block == "E":
                end_pos = pos
    return maze, str_pos, end_pos


class Direction(Enum):
    TOP = -1j
    RIGHT = 1
    BOT = 1j
    LEFT = -1


@dataclass(frozen=True)
class Node:
    pos: complex
    direction: Direction

    def __lt__(self, other):
        """Defines comparison for the priority queue (optional)."""
        return (self.pos.real, self.pos.imag) < (
            other.pos.real,
            other.pos.imag,
        )


def get_neighbors_distances(
    node: Node, graph: Dict[complex, str]
) -> List[Tuple[complex, int]]:

    next_nodes: List[Node] = []

    for direction in Direction:
        cost = inf
        next_pos = node.pos + direction.value
        if next_pos in graph and graph[next_pos] != "#":
            if direction == node.direction:
                cost = 1
            else:
                cost = 1001
            next_nodes.append((cost, Node(next_pos, direction)))
    return next_nodes


def djistra_with_weighted_angles(
    graph: Dict[complex, str], start_pos: complex
):
    start_node = Node(start_pos, Direction.RIGHT)
    visited: Set[Node] = set()
    queue = PriorityQueue()
    queue.put((0, start_node))
    backward_path: Dict[Node, Node] = {}

    costs: Dict[Node, int] = {}
    costs[start_node] = 0

    while not queue.empty():
        cost_to_node, node = queue.get()
        visited.add(node)

        for (
            cost_from_node_to_neighbor,
            neighbor_node,
        ) in get_neighbors_distances(node, graph):
            if neighbor_node not in visited:
                cost_to_neighbor = costs.setdefault(neighbor_node, inf)
                cost_to_node = costs[node]
                if (
                    cost_to_neighbor
                    > cost_to_node + cost_from_node_to_neighbor
                ):
                    cost_to_neighbor = (
                        cost_to_node + cost_from_node_to_neighbor
                    )
                    costs[neighbor_node] = cost_to_neighbor
                    backward_path[neighbor_node] = node
                    queue.put((cost_to_neighbor, neighbor_node))
    return backward_path, costs


def p1(lines: List[str]):
    maze, str_pos, end_pos = parse_maze(lines)
    backward_path, costs = djistra_with_weighted_angles(
        maze,
        start_pos=str_pos,
    )
    min_cost_for_each_incoming_direction = inf
    for direction in Direction:
        node = Node(end_pos, direction)
        cost = costs.setdefault(node, inf)
        if cost < min_cost_for_each_incoming_direction:
            min_cost_for_each_incoming_direction = cost
    return min_cost_for_each_incoming_direction


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

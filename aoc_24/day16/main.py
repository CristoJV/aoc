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

    def flip(self):
        opposite = {
            Direction.TOP: Direction.BOT,
            Direction.RIGHT: Direction.LEFT,
            Direction.BOT: Direction.TOP,
            Direction.LEFT: Direction.RIGHT,
        }
        return opposite[self]


@dataclass(frozen=True)
class Node:
    pos: complex
    direction: Direction

    def __lt__(self, other):
        """Defines comparison for the priority queue (optional)."""
        return (
            self.pos.real,
            self.pos.imag,
            self.direction.value.real,
            self.direction.value.imag,
        ) < (
            other.pos.real,
            other.pos.imag,
            other.direction.value.real,
            other.direction.value.imag,
        )


def get_neighbors_distances(
    node: Node, graph: Dict[complex, str]
) -> List[Tuple[int, Node]]:

    next_nodes: List[Node] = []

    for direction in Direction:
        if direction != node.direction:
            next_nodes.append((1000, Node(node.pos, direction)))
        else:
            next_pos = node.pos + direction.value
            if next_pos in graph and graph[next_pos] != "#":
                next_nodes.append((1, Node(next_pos, direction)))
    return next_nodes


import heapq


def djistra_with_weighted_angles(
    graph: Dict[complex, str], start_nodes: complex
):
    queue = []
    backward_path: Dict[Node, Node] = {}
    costs: Dict[Node, int] = {}

    # Initialize all start nodes
    for start_node in start_nodes:
        heapq.heappush(queue, (0, start_node))
        costs[start_node] = 0

    while queue:
        cost_to_node, node = heapq.heappop(queue)
        if costs[node] < cost_to_node:
            continue

        for (
            cost_from_node_to_neighbor,
            neighbor_node,
        ) in get_neighbors_distances(node, graph):
            cost_to_neighbor = costs.get(neighbor_node, inf)
            alternative_cost = cost_to_node + cost_from_node_to_neighbor
            if cost_to_neighbor > alternative_cost:
                costs[neighbor_node] = alternative_cost
                backward_path[neighbor_node] = node
                heapq.heappush(queue, (alternative_cost, neighbor_node))
    return backward_path, costs


def p1(lines: List[str]):
    maze, str_pos, end_pos = parse_maze(lines)
    backward_path, costs = djistra_with_weighted_angles(
        maze,
        start_nodes=[Node(str_pos, Direction.RIGHT)],
    )
    min_cost_for_each_incoming_direction = inf
    for direction in Direction:
        node = Node(end_pos, direction)
        cost = costs.setdefault(node, inf)
        if cost < min_cost_for_each_incoming_direction:
            min_cost_for_each_incoming_direction = cost
    return min_cost_for_each_incoming_direction


def p2(lines: List[str]):
    maze, str_pos, end_pos = parse_maze(lines)

    # Run Dijkstra from start position
    backward_path_from_start, from_start_costs = djistra_with_weighted_angles(
        maze,
        start_nodes=[
            Node(str_pos, Direction.RIGHT)
        ],  # Start Dijkstra from 'S'
    )

    # Run Dijkstra from the end position in all 4 directions
    backward_path_from_end, from_end_costs = djistra_with_weighted_angles(
        maze,
        start_nodes=[Node(end_pos, direction) for direction in Direction],
    )
    min_cost_for_each_incoming_direction = inf
    for direction in Direction:
        node = Node(end_pos, direction)
        cost = from_start_costs.setdefault(node, inf)
        if cost < min_cost_for_each_incoming_direction:
            min_cost_for_each_incoming_direction = cost
    count = 0
    node_set = set()
    for node_in in from_start_costs:
        for direction in Direction:
            node_out = Node(node_in.pos, node_in.direction.flip())

            if node_in in from_start_costs and node_out in from_end_costs:
                total_cost = from_start_costs[node_in] + from_end_costs.get(
                    node_out, inf
                )
                if total_cost == min_cost_for_each_incoming_direction:
                    if node_in.pos not in node_set:
                        node_set.add(node_in.pos)
                        count += 1
    return count


if __name__ == "__main__":
    testing: bool = False
    with open(
        "input.txt" if not testing else "test.txt", encoding="utf8"
    ) as f:
        input_lines = f.readlines()
        print(f"First part: {p1(input_lines)}")
        print(f"Second part: {p2(input_lines)}")

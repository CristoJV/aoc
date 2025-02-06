# pylint: disable=C0114,C0116
# pylint: disable=C0413,E0611
import heapq
import sys
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Dict, List, Tuple

from numpy import inf

utils_path = Path(__file__).resolve().parents[2] / "utils"
sys.path.insert(0, str(utils_path))


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
        return (
            self.pos.real,
            self.pos.imag,
        ) < (
            other.pos.real,
            other.pos.imag,
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


def djistra_with_weighted_angles(
    graph: Dict[complex, str], start_nodes: complex
):
    queue = []
    costs: Dict[Node, int] = {}

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
                heapq.heappush(queue, (alternative_cost, neighbor_node))
    return costs


def p1(lines: List[str]):
    maze, str_pos, end_pos = parse_maze(lines)
    costs = djistra_with_weighted_angles(
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

    from_start_costs = djistra_with_weighted_angles(
        maze,
        start_nodes=[Node(str_pos, Direction.RIGHT)],
    )

    from_end_costs = djistra_with_weighted_angles(
        maze,
        start_nodes=[Node(end_pos, direction) for direction in Direction],
    )
    min_cost_for_each_incoming_direction = inf
    for direction in Direction:
        node = Node(end_pos, direction)
        cost = from_start_costs.setdefault(node, inf)
        if cost < min_cost_for_each_incoming_direction:
            min_cost_for_each_incoming_direction = cost

    pos_set = set()
    for node_in, cost_in in from_start_costs.items():
        for direction in Direction:
            node_out = Node(node_in.pos, node_in.direction.flip())

            if node_out in from_end_costs:
                total_cost = cost_in + from_end_costs.get(node_out, inf)
                if total_cost == min_cost_for_each_incoming_direction:
                    pos_set.add(node_in.pos)
    return len(pos_set)


if __name__ == "__main__":
    testing: bool = False
    with open(
        "input.txt" if not testing else "test.txt", encoding="utf8"
    ) as f:
        input_lines = f.readlines()
        print(f"First part: {p1(input_lines)}")
        print(f"Second part: {p2(input_lines)}")

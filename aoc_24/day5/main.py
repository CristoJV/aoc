# pylint: disable=C0114,C0116
# pylint: disable=C0413,E0611
import sys
from collections import defaultdict
from functools import cmp_to_key
from pathlib import Path
from typing import List

utils_path = Path(__file__).resolve().parents[2] / "utils"
sys.path.insert(0, str(utils_path))
from profile import timeit


# The Kahn Topological Sort was not needed
def kahn_topological_sort(pairs: List[str]) -> List[int]:
    graph = defaultdict(list)
    in_degrees = defaultdict(int)

    for pair in pairs:
        a, b = pair.split("|")
        graph[a].append(b)
        in_degrees[b] += 1
        if a not in in_degrees:
            in_degrees[a] = 0

    # Kahn's algorithm
    sorted_nodes = []  # Contains the sorted elements
    nodes_with_no_incomming_edge = set(
        [node for node, in_degree in in_degrees.items() if in_degree == 0]
    )

    print(in_degrees)

    while nodes_with_no_incomming_edge:
        node = nodes_with_no_incomming_edge.pop()
        sorted_nodes.append(node)
        for down_node in graph[node]:
            in_degrees[down_node] -= 1
            if in_degrees[down_node] == 0:
                nodes_with_no_incomming_edge.add(down_node)

    return sorted_nodes


def get_cmp_fn(instructions):
    a_graph = defaultdict(list)
    b_graph = defaultdict(list)

    for pair in instructions:
        a, b = pair.split("|")
        a_graph[a].append(b)
        b_graph[b].append(a)

    def cmp(a, b):
        if b in a_graph[a]:
            return 1
        return -1

    return cmp


# Note: this works because Eric was kind and provides each relationship
# between numbers avoiding transitivity.


def p1(lines: List[str]):
    instructions, printlist = lines.split("\n\n")
    instructions = instructions.split("\n")
    printlist = printlist.split("\n")[:-1]

    cmp = get_cmp_fn(instructions)

    result = 0
    for printitem in printlist:
        nums = printitem.strip().split(",")
        for a, b in zip(nums[:-1], nums[1:]):
            if cmp(a, b) == -1:
                break
        else:
            result += int(nums[len(nums) // 2])
    return result


def p2(lines: List[str]):
    instructions, printlist = lines.split("\n\n")
    instructions = instructions.split("\n")
    printlist = printlist.split("\n")[:-1]
    cmp = get_cmp_fn(instructions)

    result = 0
    for printitem in printlist:
        nums = printitem.strip().split(",")
        for a, b in zip(nums[:-1], nums[1:]):
            if cmp(a, b) == -1:
                nums = sorted(nums, key=cmp_to_key(cmp), reverse=True)
                result += int(nums[len(nums) // 2])
                break
    return result


if __name__ == "__main__":
    with open("input.txt", encoding="utf8") as f:
        input_lines = f.read()
        print(f"First part: {p1(input_lines)}")
        print(f"Second part: {p2(input_lines)}")
        print(f"Second part: {p2(input_lines)}")

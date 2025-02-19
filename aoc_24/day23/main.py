# pylint: disable=C0114,C0116
# pylint: disable=C0413,E0611
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple

utils_path = Path(__file__).resolve().parents[2] / "utils"
sys.path.insert(0, str(utils_path))

from profile import timeit


def parse_network_map(lines: list[str]):
    network_map: Dict[str, Set[str]] = {}
    for line in lines:
        in_node, out_node = line.strip().split("-")
        network_map.setdefault(in_node, []).append(out_node)
        network_map.setdefault(out_node, []).append(in_node)
    return network_map


def p1(lines: List[str]):
    network_map = parse_network_map(lines)

    triangles: List[Tuple[int, int, int]] = []
    t_triangles: List[Tuple[int, int, int]] = []

    for u in sorted(network_map):
        for v in network_map[u]:
            if v > u:
                for w in network_map[v]:
                    if w > v and w in network_map[u]:
                        triangle = tuple([u, v, w])
                        triangles.append(triangle)
                        if u[0] == "t" or v[0] == "t" or w[0] == "t":
                            t_triangles.append(triangle)
    return len(t_triangles)


@timeit()
def p2(lines: List[str]):
    network_map = parse_network_map(lines)
    combinations = []
    for key, val in network_map.items():
        val.append(key)
        val = set(sorted(val))
        combinations.append(val)

    intersected_combinations = {}
    for j, combination_a in enumerate(combinations):
        for i, combination_b in enumerate(combinations):
            if i > j:
                combination = frozenset(combination_a & combination_b)
                if combination:
                    intersected_combinations.setdefault(combination, 0)
                    intersected_combinations[combination] += 1
    sorted_combinations = dict(
        sorted(
            intersected_combinations.items(),
            key=lambda item: item[1],
            reverse=True,
        )
    )
    best_combination = None
    for combination, count in sorted_combinations.items():
        if len(combination) <= count:
            best_combination = combination
            break
    best_combination = ",".join(sorted(best_combination))
    return best_combination


if __name__ == "__main__":
    testing: bool = False
    with open(
        "input.txt" if not testing else "test.txt", encoding="utf8"
    ) as f:
        input_lines = f.readlines()
        print(f"First part: {p1(input_lines)}")
        print(f"Second part: {p2(input_lines)}")

# pylint: disable=C0114,C0116
# pylint: disable=C0413,E0611
import sys
from pathlib import Path
from typing import Dict, List, Tuple

utils_path = Path(__file__).resolve().parents[2] / "utils"
sys.path.insert(0, str(utils_path))
from copy import deepcopy
from profile import timeit


def parse_network_map(lines: list[str]):
    network_map: Dict[str, List[str]] = {}
    for line in lines:
        in_node, out_node = line.strip().split("-")
        network_map.setdefault(in_node, []).append(out_node)
        network_map.setdefault(out_node, []).append(in_node)
    return network_map


def p1(lines: List[str]):
    network_map = parse_network_map(lines)
    visited_map = deepcopy(network_map)

    trios: List[Tuple[str, str, str]] = []
    for in_node, mid_nodes in network_map.items():
        for idx, mid_node in enumerate(mid_nodes):
            for out_node in visited_map[mid_node]:
                for rein_node in visited_map[out_node]:
                    print(in_node, mid_node, out_node, rein_node)
                    if rein_node == in_node:
                        trios.append((in_node, mid_node, out_node))
                if len(visited_map[mid_node]):
                    visited_map[mid_node].pop()
            if len(visited_map[in_node]):
                visited_map[in_node].pop()

    print(len(trios))


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

# pylint: disable=C0114,C0116
# pylint: disable=C0413,E0611
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple

utils_path = Path(__file__).resolve().parents[2] / "utils"
sys.path.insert(0, str(utils_path))


def parse_network_map(lines: list[str]):
    network_map: Dict[str, Set[str]] = {}
    for line in lines:
        in_node, out_node = line.strip().split("-")
        network_map.setdefault(in_node, set()).add(out_node)
        network_map.setdefault(out_node, set()).add(in_node)
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

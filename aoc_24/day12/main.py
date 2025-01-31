# pylint: disable=C0114,C0116
# pylint: disable=C0413,E0611
import sys
from pathlib import Path
from typing import Dict, List, Tuple

utils_path = Path(__file__).resolve().parents[2] / "utils"
sys.path.insert(0, str(utils_path))
from profile import timeit


def get_same_neighbors(
    pos: complex, plant_type: str, garden_map: Dict[complex, str]
):
    top = +1j
    right = +1
    bot = -1j
    left = -1

    directions = [top, right, bot, left]
    has_same_neighbors = [0] * 4
    for i, direction in enumerate(directions):
        neighbor_pos = pos + direction
        if neighbor_pos in garden_map:
            if garden_map[neighbor_pos] == plant_type:
                has_same_neighbors[i] = 1
    return has_same_neighbors


def parse_garden(lines: List[str]):
    garden_map: Dict[complex, str] = {}
    garden_types: Dict[str, List[complex]] = {}
    for j, line in enumerate(lines):
        for i, plot in enumerate(list(line.strip())):
            pos = i + 1j * j
            garden_map[pos] = plot
            garden_types.setdefault(plot, []).append(pos)

    return garden_map, garden_types


def flood(plant_type, plants):
    flooded_regions = {}
    flooded_index = 0
    while plants:
        flooded_region = {}
        visit_nodes = []
        visit_nodes.append(plants[0])
        flooded_region[visit_nodes[0]] = [0] * 4
        while visit_nodes:
            visit_node = visit_nodes.pop()
            if visit_node in plants:
                for idx, direction in enumerate([-1j, 1, 1j, -1]):
                    new_position = visit_node + direction
                    if new_position in plants:
                        if new_position not in flooded_region:
                            visit_nodes.append(new_position)
                            flooded_region[new_position] = [0] * 4
                        flooded_region[new_position][(idx + 2) % 4] = 1
                        flooded_region[visit_node][idx] = 1
        for plant in flooded_region:
            plants.remove(plant)
        flooded_regions[plant_type + str(flooded_index)] = flooded_region
        flooded_index += 1
    return flooded_regions


def p1(lines: List[str]):
    garden_map, plant_types = parse_garden(lines)
    total_price = 0
    for plant_type, positions in plant_types.items():
        flooded_regions = flood(plant_type, positions)
        for flooded_region in flooded_regions.values():
            area = len(flooded_region)
            perimeter = 0
            for pos, plot in flooded_region.items():
                # print(pos, plot)
                perimeter_contribution = 4 - sum(plot)
                perimeter += perimeter_contribution
            price = area * perimeter
            total_price += price
    return total_price


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

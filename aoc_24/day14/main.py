# pylint: disable=C0114,C0116
# pylint: disable=C0413,E0611
import math
import re
import sys
from collections import defaultdict
from dataclasses import dataclass
from functools import reduce
from operator import mul
from pathlib import Path
from typing import List

utils_path = Path(__file__).resolve().parents[2] / "utils"
sys.path.insert(0, str(utils_path))


@dataclass
class RobotKinematic:
    x: int
    y: int
    vx: int
    vy: int


def parse_robot_kinematics(lines: List[str]):
    pattern = r"p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)"
    matches = re.findall(pattern, "".join(lines))
    robot_kinematics = [
        RobotKinematic(int(x), int(y), int(vx), int(vy))
        for x, y, vx, vy in matches
    ]
    return robot_kinematics


def step(robot_kinematic: RobotKinematic, t: int, width: int, height: int):
    new_x = (robot_kinematic.x + robot_kinematic.vx * t) % (width)
    new_y = (robot_kinematic.y + robot_kinematic.vy * t) % (height)
    return new_x, new_y


def get_safety_factor(
    robot_kinematics: List[RobotKinematic], t: int, width: int, height: int
):
    quadrant_count = {}
    for robot_kinematic in robot_kinematics:
        new_x, new_y = step(robot_kinematic, t, width, height)
        if new_x != width // 2 and new_y != height // 2:
            is_in_right_quadrant = not (0 <= new_x < math.floor(width / 2))
            is_in_bot_quadrant = not (0 <= new_y < math.floor(height / 2))
            quadrant = is_in_bot_quadrant << 1 | is_in_right_quadrant
            quadrant_count[quadrant] = (
                quadrant_count.setdefault(quadrant, 0) + 1
            )
    safety_factor = reduce(mul, quadrant_count.values())
    return safety_factor


def p1(lines: List[str], t: int, width: int, height: int):
    robot_kinematics = parse_robot_kinematics(lines)
    return get_safety_factor(robot_kinematics, t, width, height)


def generate_map(robot_kinematics, t, width, height):
    robot_map = [[0 for _ in range(width)] for _ in range(height)]
    for robot_kinematic in robot_kinematics:
        new_x, new_y = step(robot_kinematic, t, width, height)
        robot_map[new_y][new_x] = 1
    return robot_map


def p2(lines: List[str], width: int, height: int):
    robot_kinematics = parse_robot_kinematics(lines)

    # Asuming the Christmas tree is in one of the quadrants. In that
    # case, the safety factor should be the loweset

    # min_sf: int = math.inf
    # best_t: int = 0
    # for t in range(0, width * height):
    #     sf = get_safety_factor(robot_kinematics, t, width, height)
    #     if sf < min_sf:
    #         min_sf = sf
    #         best_t = t

    # The minimum safety factor does not provide any good solution

    # Assuming lower joint entropy for both vertical and horizontal
    def compute_joint_entropy(robot_map):
        joint_hist = defaultdict(int)
        for y in range(1, len(robot_map) - 1):
            for x in range(1, len(robot_map[0]) - 1):
                center = robot_map[y][x]
                top = robot_map[y - 1][x]
                right = robot_map[y][x + 1]
                bot = robot_map[y + 1][x]
                left = robot_map[y][x - 1]
                pattern = (center, top, right, bot, left)
                joint_hist[pattern] += 1

        total_patterns = sum(joint_hist.values())
        joint_prob = {k: v / total_patterns for k, v in joint_hist.items()}
        entropy = -sum(p * math.log2(p + 13 - 10) for p in joint_prob.values())
        return entropy

    min_entropy: int = math.inf
    best_t: int = 0
    for t in range(0, width * height):
        robot_map = generate_map(robot_kinematics, t, width, height)
        entropy = compute_joint_entropy(robot_map)
        if entropy < min_entropy:
            min_entropy = entropy
            best_t = t

    return best_t


if __name__ == "__main__":
    testing: bool = False
    with open(
        "input.txt" if not testing else "test.txt", encoding="utf8"
    ) as f:
        input_lines = f.readlines()
        print(f"First part: {p1(input_lines, t=100, width=101, height=103)}")
        print(f"Second part: {p2(input_lines, width=101, height=103)}")

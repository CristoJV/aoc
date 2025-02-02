# pylint: disable=C0114,C0116
# pylint: disable=C0413,E0611
import math
import re
import sys
from dataclasses import dataclass
from functools import reduce
from operator import mul
from pathlib import Path
from typing import List

utils_path = Path(__file__).resolve().parents[2] / "utils"
sys.path.insert(0, str(utils_path))
from profile import timeit


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


def p1(lines: List[str], t: int, width: int, height: int):
    robot_kinematics = parse_robot_kinematics(lines)
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
    result = reduce(mul, quadrant_count.values())
    return result


def p2(lines: List[str]):
    pass


if __name__ == "__main__":
    testing: bool = False
    with open(
        "input.txt" if not testing else "test.txt", encoding="utf8"
    ) as f:
        input_lines = f.readlines()
        print(f"First part: {p1(input_lines, t=100, width=101, height=103)}")
        print(f"Second part: {p2(input_lines)}")

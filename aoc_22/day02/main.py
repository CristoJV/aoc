# pylint: disable=C0114,C0116
# pylint: disable=C0413,E0611
import sys
from pathlib import Path
from typing import List

utils_path = Path(__file__).resolve().parents[2] / "utils"
sys.path.insert(0, str(utils_path))


def p1(lines: List[str]):
    combination = [
        " ",
        "BX",  # Losing with Rock
        "CY",
        "AZ",
        "AX",  # Drawing with Rock
        "BY",
        "CZ",
        "CX",  # Winning with Rock
        "AY",
        "BZ",
    ]
    return sum([combination.index(line[0] + line[2]) for line in lines])


def p2(lines: List[str]):
    combination = [
        " ",
        "BX",
        "CX",
        "AX",
        "AY",
        "BY",
        "CY",
        "CZ",
        "AZ",
        "BZ",
    ]
    return sum([combination.index(line[0] + line[2]) for line in lines])


if __name__ == "__main__":
    testing: bool = False
    with open(
        "input.txt" if not testing else "test.txt", encoding="utf8"
    ) as f:
        input_lines = f.readlines()
        print(f"First part: {p1(input_lines)}")
        print(f"Second part: {p2(input_lines)}")

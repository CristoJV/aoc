# pylint: disable=C0114,C0116
# pylint: disable=C0413,E0611
import sys
from pathlib import Path
from typing import List

utils_path = Path(__file__).resolve().parents[2] / "utils"
sys.path.insert(0, str(utils_path))
from profile import timeit
from collections import Counter


def p1(lines):
    pass


def p2(lines):
    pass


if __name__ == "__main__":
    with open("input.txt", encoding="utf8") as f:
        lines = f.readlines()
        print(f"First part: {p1(lines)}")
        print(f"Second part: {p2(lines)}")

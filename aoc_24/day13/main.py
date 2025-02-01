# pylint: disable=C0114,C0116
# pylint: disable=C0413,E0611
import sys
from pathlib import Path
from typing import List

utils_path = Path(__file__).resolve().parents[2] / "utils"
sys.path.insert(0, str(utils_path))
from profile import timeit

import regex as re


def parse_prices(lines: List[str]):
    text = "".join(lines)
    pattern = r"Button A: X\+(\d+), Y\+(\d+)\nButton B: X\+(\d+), Y\+(\d+)\nPrize: X=(\d+), Y=(\d+)"
    matches = re.findall(pattern, text)
    for idx, match in enumerate(matches):
        matches[idx] = list(map(int, match))
    return matches


def check_if_unique_solution(a1, a2, b1, b2, c1, c2):
    det = (a1 * b2) - (a2 * b1)
    if det != 0:  # The sistem has an unique solution
        ax = (c1 * b2) - (c2 * b1)
        ay = (a1 * c2) - (a2 * c1)
        x = ax / det
        y = ay / det
        return True, x, y
    return False, x, y


def check_if_integer(x, tolerance=1e-11):
    return abs(x % 1) < tolerance


def p1(lines: List[str]):
    prices = parse_prices(lines)
    tokens = 0
    for price in prices:
        status, x, y = check_if_unique_solution(*price)
        if status and all(check_if_integer(num) for num in [x, y]):
            tokens_i = x * 3 + y
            tokens += tokens_i
    return int(tokens)


def p2(lines: List[str]):
    prices = parse_prices(lines)
    tokens = 0
    for price in prices:
        price[-2] += 1e13
        price[-1] += 1e13
        status, x, y = check_if_unique_solution(*price)
        if status and all(check_if_integer(num) for num in [x, y]):
            tokens_i = x * 3 + y
            tokens += tokens_i
    return int(tokens)


if __name__ == "__main__":
    testing: bool = False
    with open(
        "input.txt" if not testing else "test.txt", encoding="utf8"
    ) as f:
        input_lines = f.readlines()
        print(f"First part: {p1(input_lines)}")
        print(f"Second part: {p2(input_lines)}")

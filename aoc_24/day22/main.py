# pylint: disable=C0114,C0116
# pylint: disable=C0413,E0611
import math
import sys
from pathlib import Path
from typing import Dict, List

utils_path = Path(__file__).resolve().parents[2] / "utils"
sys.path.insert(0, str(utils_path))


def parse_secrets(lines: List[str]):
    return map(int, lines)


def get_next_secret(secret: int, memo: Dict[int, int]):
    if secret in memo:
        return memo[secret]

    next_secret = ((secret * 64) ^ secret) % 16777216
    next_secret = (math.floor(next_secret / 32) ^ next_secret) % 16777216
    next_secret = ((next_secret * 2048) ^ next_secret) % 16777216
    memo[secret] = next_secret
    return next_secret


def p1(lines: List[str]):
    memo = {}
    count = 0
    for secret in parse_secrets(lines):
        for _ in range(2000):
            secret = get_next_secret(secret, memo)
        count += secret
    return count


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

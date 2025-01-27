# pylint: disable=C0114,C0116
# pylint: disable=C0413,E0611
import sys
from functools import lru_cache
from pathlib import Path
from typing import Dict, List

utils_path = Path(__file__).resolve().parents[2] / "utils"
sys.path.insert(0, str(utils_path))

from profile import timeit


def parse_stones(lines: List[str]) -> List[str]:
    stones = lines[0].strip().split(" ")
    return stones


def expanded_stones(stone: str) -> List[str]:
    stone_int = int(stone)
    if stone_int == 0:
        return ["1"]
    elif len(stone) % 2 == 0:
        half = len(stone) // 2
        return [stone[:half], str(int(stone[half:]))]
    else:
        return [str(stone_int * 2024)]


def blink(
    stone: str, blink_step, memo: Dict[str, List[int]], max_steps=1
) -> int:
    if blink_step >= max_steps:
        return 1

    if stone not in memo:
        memo[stone] = [0] * max_steps

    cached_stone_count = memo[stone][blink_step]
    if memo[stone][blink_step] != 0:
        return cached_stone_count

    stone_count = sum(
        blink(
            expanded_stone,
            blink_step=blink_step + 1,
            memo=memo,
            max_steps=max_steps,
        )
        for expanded_stone in expanded_stones(stone)
    )
    memo[stone][blink_step] = stone_count
    return stone_count


@timeit(repeats=5)
def solve(lines: List[str], max_steps: int):
    stones = parse_stones(lines)
    count = sum(
        blink(stone, blink_step=0, memo={}, max_steps=max_steps)
        for stone in stones
    )
    return count


@timeit(repeats=5)
def solve_with_lru_cache(lines: List[str], max_steps: int):
    @lru_cache(None)
    def blink_with_lru(stone: str, step: int) -> int:
        if step >= max_steps:
            return 1
        return sum(
            blink_with_lru(expanded_stone, step + 1)
            for expanded_stone in expanded_stones(stone)
        )

    stones = parse_stones(lines)
    return sum(blink_with_lru(stone, 0) for stone in stones)


def p1(lines: List[str]):
    return solve(lines, 25), solve_with_lru_cache(lines, 25)


def p2(lines: List[str]):
    return solve(lines, 75), solve_with_lru_cache(lines, 75)


if __name__ == "__main__":
    testing: bool = False
    with open(
        "input.txt" if not testing else "test.txt", encoding="utf8"
    ) as f:
        input_lines = f.readlines()
        print(f"First part: {p1(input_lines)}")
        print(f"Second part: {p2(input_lines)}")

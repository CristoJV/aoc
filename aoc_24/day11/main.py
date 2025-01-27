# pylint: disable=C0114,C0116
# pylint: disable=C0413,E0611
import sys
from pathlib import Path
from typing import List

utils_path = Path(__file__).resolve().parents[2] / "utils"
sys.path.insert(0, str(utils_path))
from profile import timeit


def parse_stones(lines: List[str]) -> List[str]:
    stones = lines[0].strip().split(" ")
    return stones


def blink(stone: str, blink_step, max_steps=1) -> List[str]:
    if blink_step == max_steps:
        return [stone]

    if all(digit == "0" for digit in list(stone)):
        return blink("1", blink_step + 1, max_steps)

    if len(stone) % 2 == 0:
        left_half = len(stone) // 2
        exploted_stone_first_half = stone[:left_half]
        exploded_stone_second_half = str(int(stone[left_half:]))
        stones_first_half = blink(
            exploted_stone_first_half, blink_step + 1, max_steps
        )
        stones_second_half = blink(
            exploded_stone_second_half, blink_step + 1, max_steps
        )
        stones_first_half.extend(stones_second_half)
        return stones_first_half

    exploded_stone = str(int(stone) * 2024)
    return blink(exploded_stone, blink_step + 1, max_steps)


def p1(lines: List[str]):
    stones = parse_stones(lines)
    exploded_stones = [
        element
        for stone in stones
        for element in blink(stone, blink_step=0, max_steps=25)
    ]
    return len(exploded_stones)


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

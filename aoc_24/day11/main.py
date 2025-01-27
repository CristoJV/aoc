# pylint: disable=C0114,C0116
# pylint: disable=C0413,E0611
import sys
from pathlib import Path
from typing import Dict, List

utils_path = Path(__file__).resolve().parents[2] / "utils"
sys.path.insert(0, str(utils_path))


def parse_stones(lines: List[str]) -> List[str]:
    stones = lines[0].strip().split(" ")
    return stones


def blink(
    stone: str, blink_step, memo: Dict[str, List[int]], max_steps=1
) -> int:
    if blink_step >= max_steps:
        memo.setdefault(stone, [0] * max_steps)[blink_step - 1] = 1
        return 1

    if stone in memo:
        stone_count_in_memo = memo[stone][blink_step - 1]
        if stone_count_in_memo != 0:
            return stone_count_in_memo

    if all(digit == "0" for digit in list(stone)):
        exploded_stone = "1"
        stone_count = blink(
            stone=exploded_stone,
            blink_step=blink_step + 1,
            memo=memo,
            max_steps=max_steps,
        )
        memo.setdefault(stone, [0] * max_steps)[blink_step - 1] = stone_count
        return stone_count

    if len(stone) % 2 == 0:
        left_half = len(stone) // 2
        exploted_stone_first_half = stone[:left_half]
        exploded_stone_second_half = str(int(stone[left_half:]))
        stone_count = blink(
            exploted_stone_first_half,
            blink_step + 1,
            memo=memo,
            max_steps=max_steps,
        ) + blink(
            exploded_stone_second_half,
            blink_step + 1,
            memo=memo,
            max_steps=max_steps,
        )
        memo.setdefault(stone, [0] * max_steps)[blink_step - 1] = stone_count
        return stone_count

    exploded_stone = str(int(stone) * 2024)
    stone_count = blink(
        exploded_stone, blink_step + 1, memo=memo, max_steps=max_steps
    )
    memo.setdefault(stone, [0] * max_steps)[blink_step - 1] = stone_count
    return stone_count


def p1(lines: List[str]):
    stones = parse_stones(lines)
    count = sum(
        [blink(stone, blink_step=0, memo={}, max_steps=25) for stone in stones]
    )
    return count


def p2(lines: List[str]):
    stones = parse_stones(lines)
    count = sum(
        [blink(stone, blink_step=0, memo={}, max_steps=75) for stone in stones]
    )
    return count


if __name__ == "__main__":
    testing: bool = False
    with open(
        "input.txt" if not testing else "test.txt", encoding="utf8"
    ) as f:
        input_lines = f.readlines()
        print(f"First part: {p1(input_lines)}")
        print(f"Second part: {p2(input_lines)}")

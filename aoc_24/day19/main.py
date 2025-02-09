# pylint: disable=C0114,C0116
# pylint: disable=C0413,E0611
import sys
from pathlib import Path
from typing import List, Set, Tuple

utils_path = Path(__file__).resolve().parents[2] / "utils"
sys.path.insert(0, str(utils_path))


def parse_patterns(lines: List[str]) -> Tuple[List[str], List[str]]:
    full_str = "".join(lines)
    patterns = full_str.split("\n\n")
    available_patterns = patterns[0].split(", ")
    desired_patterns = patterns[1].split("\n")[:-1]
    return available_patterns, desired_patterns


def is_valid(desired_pattern: str, available_patterns: Set[str]) -> bool:

    if desired_pattern in available_patterns:
        return True, [desired_pattern]

    if len(desired_pattern) in [0, 1]:
        return False, []
    # Check the rest of the pattern

    half = len(desired_pattern) // 2
    chain_left = desired_pattern[:half]
    chain_right = desired_pattern[half:]

    is_valid_left, left_patterns = is_valid(chain_left, available_patterns)
    if is_valid_left:
        is_valid_right, right_patterns = is_valid(
            chain_right, available_patterns
        )

    if is_valid_left and is_valid_right:
        available_patterns.add("".join(left_patterns + right_patterns))
        return True, left_patterns + right_patterns

    half = len(desired_pattern) // 2 - 2
    chain_left = desired_pattern[:half]
    chain_right = desired_pattern[half:]

    is_valid_left, left_patterns = is_valid(chain_left, available_patterns)
    if is_valid_left:
        is_valid_right, right_patterns = is_valid(
            chain_right, available_patterns
        )

    if is_valid_left and is_valid_right:
        available_patterns.add("".join(left_patterns + right_patterns))
        return True, left_patterns + right_patterns

    return False, []


def p1(lines: List[str]):
    available_patterns, desired_patterns = parse_patterns(lines)
    available_patterns = set(available_patterns)

    valid = 0
    for desired_pattern in desired_patterns:
        is_valid_pattern, patterns = is_valid(
            desired_pattern, available_patterns
        )

        if is_valid_pattern:
            valid += 1
    return valid


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

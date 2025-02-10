# pylint: disable=C0114,C0116
# pylint: disable=C0413,E0611
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple

utils_path = Path(__file__).resolve().parents[2] / "utils"
sys.path.insert(0, str(utils_path))


def parse_patterns(lines: List[str]) -> Tuple[List[str], List[str]]:
    full_str = "".join(lines)
    patterns = full_str.split("\n\n")
    available_patterns = patterns[0].split(", ")
    desired_patterns = patterns[1].split("\n")[:-1]
    return available_patterns, desired_patterns


def is_valid(
    desired_pattern: str,
    available_patterns: Set[str],
    memo: Dict[str, Tuple[bool, list]] = None,
) -> Tuple[bool, list]:
    if memo is None:
        memo = {}

    if desired_pattern in memo:
        return memo[desired_pattern]

    if desired_pattern in available_patterns:
        memo[desired_pattern] = (True, [desired_pattern])
        return True, [desired_pattern]

    if len(desired_pattern) <= 1:
        memo[desired_pattern] = (False, [])
        return False, []

    for i in range(1, len(desired_pattern)):
        chain_left = desired_pattern[:i]
        chain_right = desired_pattern[i:]

        is_valid_left, left_patterns = is_valid(
            chain_left, available_patterns, memo
        )
        is_valid_right, right_patterns = is_valid(
            chain_right, available_patterns, memo
        )

        if is_valid_left and is_valid_right:
            full_pattern = "".join(left_patterns + right_patterns)
            available_patterns.add(full_pattern)
            memo[desired_pattern] = (True, left_patterns + right_patterns)
            return True, left_patterns + right_patterns

    memo[desired_pattern] = (False, [])
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


def all_available_solutions(
    desired_pattern: str, available_patterns: Set[str]
):
    n = len(desired_pattern)
    dp = [0] * (n + 1)
    dp[0] = 1

    for i in range(n):
        if dp[i] != 0:
            for pat in available_patterns:
                length = len(pat)
                if i + length <= n and desired_pattern[i : i + length] == pat:
                    dp[i + length] += dp[i]

    return dp[n]


def p2(lines: List[str]):
    valid = 0
    available_patterns, desired_patterns = parse_patterns(lines)
    for desired_pattern in desired_patterns:
        counts = all_available_solutions(desired_pattern, available_patterns)
        valid += counts
    return valid


if __name__ == "__main__":
    testing: bool = False
    with open(
        "input.txt" if not testing else "test.txt", encoding="utf8"
    ) as f:
        input_lines = f.readlines()
        print(f"First part: {p1(input_lines)}")
        print(f"Second part: {p2(input_lines)}")

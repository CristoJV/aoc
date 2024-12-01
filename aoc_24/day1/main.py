# pylint: disable=C0114,C0116
# pylint: disable=C0413,E0611
import sys
from pathlib import Path
from typing import List
utils_path = Path(__file__).resolve().parents[2] / "utils"
sys.path.insert(0, str(utils_path))
from profile import timeit
from collections import Counter


def p1(input_lines: List):
    input_lines = [line.strip().split("  ") for line in input_lines]
    left = sorted([int(line[0]) for line in input_lines])
    right = sorted([int(line[1]) for line in input_lines])
    return sum(abs(l-r) for l,r in zip(left, right))

@timeit(100)
def p2(input_lines: List):
    left = []
    right = {}
    for line in input_lines:
        line = line.strip().split("  ")
        left.append(int(line[0]))
        num = int(line[1])
        if num not in right:
            right[num] = 1
        else:
            right[num] +=1
    return sum(x * right.get(x, 0) for x in left)

@timeit(100)
def p2_efficient(input_lines):
    input_lines = [line.strip().split("  ") for line in input_lines]
    left = [int(line[0]) for line in input_lines]
    right = [int(line[1]) for line in input_lines]

    # list.count() has a time complexity of O(n). When used inside a loop, it
    # leads to O(n^2) time complexity.
    # return sum(x*right.count(x) for x in left)

    # Counter reduces time complexity to O(n)
    right_counts = Counter(right)
    return sum(x * right_counts.get(x, 0) for x in left)

if __name__ == "__main__":
    with open('input.txt', encoding='utf8') as f:
        lines = f.readlines()
        print(f"First part: {p1(lines)}")
        print(f"Second part: {p2(lines)}")
        print(f"Second part (one-line): {p2_efficient(lines)}")

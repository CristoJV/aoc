# pylint: disable=C0114,C0116
# pylint: disable=C0413,E0611
import sys
from pathlib import Path
from typing import List

utils_path = Path(__file__).resolve().parents[2] / "utils"
sys.path.insert(0, str(utils_path))
from profile import timeit


def p1(lines: List[str]):
    window_size = 4
    width = len(lines[0]) - 1  # Remove \n
    height = len(lines)
    result = 0
    patterns = ["XMAS", "SAMX"]

    for jdx in range(height):
        for idx in range(width):
            if idx <= width - window_size:
                horizontal_eval = lines[jdx][idx : idx + window_size]
                if horizontal_eval in patterns:
                    result += 1
            if jdx <= height - window_size:
                vertical_lines = lines[jdx : jdx + window_size]

                verical_eval = "".join(line[idx] for line in vertical_lines)
                if verical_eval in patterns:
                    result += 1

                if idx <= width - window_size:
                    negative_diagonal_eval = "".join(
                        line[idx + i] for i, line in enumerate(vertical_lines)
                    )
                    if negative_diagonal_eval in patterns:
                        result += 1

                    positive_diagonal_eval = "".join(
                        line[idx + i] for i, line in enumerate(vertical_lines[::-1])
                    )
                    if positive_diagonal_eval in patterns:
                        result += 1
    return result


def p2(lines: List[str]):
    width = len(lines[0]) - 1  # \n
    height = len(lines)
    result = 0
    vertices_checks = ["MSSM", "SMMS", "MMSS", "SSMM"]
    for jdx in range(1, height - 1):
        for idx in range(1, width - 1):
            if lines[jdx][idx] == "A":
                vertices = "".join(
                    [
                        lines[jdx - 1][idx - 1],
                        lines[jdx - 1][idx + 1],
                        lines[jdx + 1][idx + 1],
                        lines[jdx + 1][idx - 1],
                    ]
                )
                if vertices in vertices_checks:
                    result += 1
    return result


if __name__ == "__main__":
    with open("input.txt", encoding="utf8") as f:
        input_lines = f.readlines()
        print(f"First part: {p1(input_lines)}")
        print(f"Second part: {p2(input_lines)}")

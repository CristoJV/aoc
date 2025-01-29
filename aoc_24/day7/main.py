# pylint: disable=C0114,C0116
# pylint: disable=C0413,E0611
import sys
from functools import reduce
from operator import add, mul
from pathlib import Path
from typing import Callable, List, Tuple

utils_path = Path(__file__).resolve().parents[2] / "utils"
sys.path.insert(0, str(utils_path))
from profile import timeit


def parse_equations(lines: List[str]) -> Tuple[List[int], List[List[int]]]:
    results = []
    operands = []
    for line in lines:
        result, operands_i, *_ = line.strip().split(": ")
        operands_i = list(map(int, operands_i.split(" ")))
        results.append(int(result))
        operands.append(operands_i)
    return results, operands


def p1(lines: List[str]):
    results, operands = parse_equations(lines)
    total = 0
    for idx, result in enumerate(results):
        operands_i = operands[idx]
        num_operators = len(operands_i) - 1
        first_operand = operands_i[0]
        for i in range(2**num_operators):
            operation_result = first_operand
            for j in range(0, num_operators):
                operator = add if i & (1 << j) else mul

                operation_result = reduce(
                    operator, [operation_result, operands_i[j + 1]]
                )
            if operation_result == result:
                total += result
                break
    return total


def p2(lines: List[str]):
    pass


if __name__ == "__main__":
    testing: bool = True
    with open(
        "input.txt" if not testing else "test.txt", encoding="utf8"
    ) as f:
        input_lines = f.readlines()
        print(f"First part: {p1(input_lines)}")
        print(f"Second part: {p2(input_lines)}")

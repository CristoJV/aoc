# pylint: disable=C0114,C0116
# pylint: disable=C0413,E0611
import sys
from functools import lru_cache
from operator import add, mul
from pathlib import Path
from typing import Callable, List, Tuple

utils_path = Path(__file__).resolve().parents[2] / "utils"
sys.path.insert(0, str(utils_path))

from profile import timeit

from functions import count_digits


def parse_equations(lines: List[str]) -> Tuple[List[int], List[List[int]]]:
    results = []
    operands = []
    for line in lines:
        result, operands_i, *_ = line.strip().split(": ")
        operands_i = list(map(int, operands_i.split(" ")))
        results.append(int(result))
        operands.append(operands_i)
    return results, operands


def dfs_recursive(
    first_operand: int,
    next_operands: List[int],
    expected_result: int,
    available_operators: List[Callable],
) -> Tuple[bool, int]:

    @lru_cache(None)
    def dfs(first_operand, next_operand_index) -> Tuple[bool, int]:
        if next_operand_index == len(next_operands):
            if first_operand == expected_result:
                return True, first_operand
            return False, first_operand

        next_operand = next_operands[next_operand_index]

        for operator_i in available_operators:
            new_operand = operator_i(first_operand, next_operand)

            if new_operand > expected_result:
                # Optimization: If new operand exceeds expected result,
                # stop exploring this path
                continue

            success, result = dfs(new_operand, next_operand_index + 1)
            if success:
                # Return early if a valid path is found
                return True, result

        return False, new_operand

    return dfs(first_operand, 0)


def dfs_iterative(
    first_operand, next_operands, expected_result, available_operators
):
    stack = [(first_operand, 0)]
    # ^ Stack stores (current_value, operand_index)

    while stack:
        current_value, idx = stack.pop()  # Last-added element (LIFO)

        if idx == len(next_operands):
            if current_value == expected_result:
                return True, current_value
            continue

        next_operand = next_operands[idx]

        for operator in available_operators:
            new_value = operator(current_value, next_operand)

            if new_value > expected_result:
                continue  # Prune search

            stack.append((new_value, idx + 1))
            # ^ Push new state to stack

    return False, first_operand


@timeit(repeats=1)
def solve(
    lines: List[str], available_operators: List[Callable], dfs_algo: Callable
):

    results, operands = parse_equations(lines)
    total = 0
    for equation_idx, expected_result in enumerate(results):
        next_operands = operands[equation_idx]
        first_operand = next_operands.pop(0)
        success, result = dfs_algo(
            first_operand,
            next_operands,
            expected_result=expected_result,
            available_operators=available_operators,
        )
        if success:
            total += result

    return total


def concatenation(first_operand: int, second_operand: int):

    return (
        first_operand * 10 ** (count_digits(second_operand)) + second_operand
    )


def p1(lines: List[str]):
    recursive_result = solve(
        lines, available_operators=[add, mul], dfs_algo=dfs_recursive
    )
    iterative_result = solve(
        lines, available_operators=[add, mul], dfs_algo=dfs_iterative
    )
    assert recursive_result == iterative_result
    return recursive_result


def p2(lines: List[str]):
    recursive_result = solve(
        lines,
        available_operators=[add, mul, concatenation],
        dfs_algo=dfs_recursive,
    )
    iterative_result = solve(
        lines,
        available_operators=[add, mul, concatenation],
        dfs_algo=dfs_iterative,
    )
    assert recursive_result == iterative_result
    return recursive_result


if __name__ == "__main__":
    testing: bool = False
    with open(
        "input.txt" if not testing else "test.txt", encoding="utf8"
    ) as f:
        input_lines = f.readlines()
        print(f"First part: {p1(input_lines)}")
        print(f"Second part: {p2(input_lines)}")

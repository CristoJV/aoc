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


def depth_first_search(
    first_operand: int,
    next_operands: List[int],
    operator: Callable,
    expected_result: int,
    available_operators: List[Callable],
) -> Tuple[bool, int]:
    if len(next_operands) == 0:
        if first_operand == expected_result:
            return True, first_operand
        return False, first_operand
    # saved_first_operand = first_operand
    next_operands_copy = next_operands.copy()
    next_operand = next_operands_copy.pop(0)
    first_operand = operator(first_operand, next_operand)
    # print(
    #     f"{saved_first_operand} {'x' if operator==mul else '+'} {next_operand} = {first_operand}"
    # )
    for operator_i in available_operators:
        success, result = depth_first_search(
            first_operand,
            next_operands_copy,
            operator_i,
            expected_result,
            available_operators,
        )
        if success:
            return success, result

    return False, result


def p2(lines: List[str]):
    results, operands = parse_equations(lines)
    total = 0

    def concatenation(first_operand: int, second_operand: int):
        return int(str(first_operand) + str(second_operand))

    for equation_idx, expected_result in enumerate(results):
        next_operands = operands[equation_idx]
        first_operand = next_operands.pop(0)
        available_operators = [add, mul, concatenation]
        # print(f"Evaluating: {expected_result}")
        for operator in available_operators:
            success, result = depth_first_search(
                first_operand,
                next_operands,
                operator=operator,
                expected_result=expected_result,
                available_operators=available_operators,
            )
            if success:
                total += result
                break
    return total


if __name__ == "__main__":
    testing: bool = False
    with open(
        "input.txt" if not testing else "test.txt", encoding="utf8"
    ) as f:
        input_lines = f.readlines()
        print(f"First part: {p1(input_lines)}")
        print(f"Second part: {p2(input_lines)}")

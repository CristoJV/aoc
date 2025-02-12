# pylint: disable=C0114,C0116
# pylint: disable=C0413,E0611
import re
import sys
from pathlib import Path
from typing import List

utils_path = Path(__file__).resolve().parents[2] / "utils"
sys.path.insert(0, str(utils_path))


def parse_debugger(lines: List[str]):
    full_str = "".join(lines)
    pattern = r"A: (\d+)\n.* B: (\d)+\n.* C: (\d)+\n\n.*: (.*)"
    matches = re.findall(pattern, full_str)
    a, b, c, program = matches[0]
    program = list(map(int, program.split(",")))
    return int(a), int(b), int(c), program


def p1(lines: List[str]):
    a, b, c, program = parse_debugger(lines)
    output = []

    # Using mutable operands
    operands: List[int] = [0, 1, 2, 3, a, b, c, -1]
    pointer: int = 0

    while pointer < len(program):
        operator = program[pointer]
        x = program[pointer + 1]
        match operator:
            case 0:  # adv
                operands[4] = int(operands[4] / (2 ** (operands[x])))
            case 1:  # bxl
                operands[5] = operands[5] ^ x
            case 2:  # bst
                operands[5] = operands[x] % 8
            case 3:  # jnz
                if operands[4] != 0:
                    pointer = x - 2
            case 4:  # bxc
                operands[5] = operands[5] ^ operands[6]
            case 5:  # out
                output.append(operands[x] % 8)
            case 6:  # bdv
                operands[5] = int(operands[4] / (2 ** (operands[x])))
            case 7:  # cdv
                operands[6] = int(operands[4] / (2 ** (operands[x])))
        pointer += 2
    return ",".join(map(str, output))


def get_output(a, program):
    output = []
    operands: List[int] = [0, 1, 2, 3, a, 0, 0, -1]
    pointer: int = 0
    while pointer < len(program):
        operator = program[pointer]
        x = program[pointer + 1]
        match operator:
            case 0:  # adv
                operands[4] = int(operands[4] / (2 ** (operands[x])))
            case 1:  # bxl
                operands[5] = operands[5] ^ x
            case 2:  # bst
                operands[5] = operands[x] % 8
            case 3:  # jnz
                if operands[4] != 0:
                    pointer = x - 2
            case 4:  # bxc
                operands[5] = operands[5] ^ operands[6]
            case 5:  # out
                output.append(operands[x] % 8)
            case 6:  # bdv
                operands[5] = int(operands[4] / (2 ** (operands[x])))
            case 7:  # cdv
                operands[6] = int(operands[4] / (2 ** (operands[x])))
        pointer += 2
    return output


def dfs_exploration(a: int, depth: int, program: List[int]):
    output = get_output(
        a,
        program,
    )

    if depth == len(program):
        if output == program:
            return True, a
        else:
            return False, 0
    if output == program[-depth:]:  # Continue one depth
        a *= 8
        for i in range(8):
            status, total_a = dfs_exploration(a + i, depth + 1, program)
            if status:
                return True, total_a
    return False, 0


def p2(lines: List[str]):
    a, _, _, program = parse_debugger(lines)
    for a in range(8):
        status, resulting_a = dfs_exploration(a, 1, program)
        if status:
            print(resulting_a)


if __name__ == "__main__":
    testing: bool = False
    with open(
        "input.txt" if not testing else "test.txt", encoding="utf8"
    ) as f:
        input_lines = f.readlines()
        print(f"First part: {p1(input_lines)}")
        print(f"Second part: {p2(input_lines)}")

# pylint: disable=C0114,C0116
# pylint: disable=C0413,E0611
import re
import sys
from pathlib import Path
from typing import Dict, List

utils_path = Path(__file__).resolve().parents[2] / "utils"
sys.path.insert(0, str(utils_path))


def parse_debugger(lines: List[str]):
    full_str = "".join(lines)
    pattern = r"A: (\d+)\n.* B: (\d)+\n.* C: (\d)+\n\n.*: (.*)"
    matches = re.findall(pattern, full_str)
    a, b, c, program = matches[0]
    program = list(map(int, program.split(",")))
    return a, b, c, program


def p1(lines: List[str]):
    a, b, c, program = parse_debugger(lines)
    pointer_ref = [0]
    output = []

    a_ref = [int(a)]
    b_ref = [int(b)]
    c_ref = [int(c)]

    # Using mutable operands
    operands: Dict[int, List[int]] = {
        0: [0],
        1: [1],
        2: [2],
        3: [3],
        4: a_ref,
        5: b_ref,
        6: c_ref,
        7: [0],
    }

    def adv(x: int):
        x = operands[x][0]
        a_ref[0] = int(a_ref[0] / (2 ** (x)))

    def bxl(x: int):
        b_ref[0] = b_ref[0] ^ x

    def bst(x: int):
        x = operands[x][0]
        b_ref[0] = x % 8

    def jnz(x: int):
        if a_ref[0] != 0:
            pointer_ref[0] = x - 2

    def bxc(x: int):
        b_ref[0] = b_ref[0] ^ c_ref[0]

    def out(x: int):
        x = operands[x][0]
        output.append(x % 8)

    def bdv(x: int):
        x = operands[x][0]
        b_ref[0] = int(a_ref[0] / (2 ** (x)))

    def cdv(x: int):
        x = operands[x][0]
        c_ref[0] = int(a_ref[0] / (2 ** (x)))

    opcodes: Dict[int, callable] = {
        0: adv,
        1: bxl,
        2: bst,
        3: jnz,
        4: bxc,
        5: out,
        6: bdv,
        7: cdv,
    }

    while pointer_ref[0] < len(program):
        opcodes[program[pointer_ref[0]]](program[pointer_ref[0] + 1])
        pointer_ref[0] += 2

    return ",".join(map(str, output))


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

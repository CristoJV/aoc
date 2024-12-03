# pylint: disable=C0114,C0116
# pylint: disable=C0413,E0611
import sys
from pathlib import Path
from typing import List

utils_path = Path(__file__).resolve().parents[2] / "utils"
sys.path.insert(0, str(utils_path))
from profile import timeit

import re


def p1(lines: List[str]) -> int:
    pattern = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)")

    result = 0
    for line in lines:
        search = re.findall(pattern, line)
        result += sum(int(mul[0]) * int(mul[1]) for mul in search)

    return result


@timeit(1000)  # 0.000477 seconds
def p2(lines: List[str]) -> int:
    pattern = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)")
    do_pattern = re.compile(r"do(n't)?\(\)")

    program = "".join(lines)

    result = 0
    do_search = re.finditer(do_pattern, program)
    search = re.finditer(pattern, program)

    limits = [0]
    enabled = True
    for m in do_search:
        if m[1] and enabled:
            limits.append(m.span(0)[1])
            enabled = False
        if not m[1] and not enabled:
            limits.append(m.span(0)[1])
            enabled = True
    limits.append(len(program))
    current_block = 0
    for m in search:
        index = m.span(0)[1]
        if index > limits[current_block + 1]:
            current_block += 1
        if (current_block + 1) % 2 == 1:
            result += ((current_block + 1) % 2) * int(m.group(1)) * int(m.group(2))
    return result


@timeit(1000)  # 0.000736 seconds
def p2_only_one_regex(lines: List[str]) -> int:
    program = "".join(lines)
    regex = r"(do|don't)\(\)|mul\((\d*),(\d*)\)"
    search = re.finditer(regex, program)
    enabled = True
    result = 0
    for match in search:
        enable_condition, num1, num2 = match.groups()
        if enable_condition == "do":
            enabled = True
        elif enable_condition == "don't":
            enabled = False
        else:
            result += enabled * int(num1) * int(num2)
    return result


if __name__ == "__main__":
    with open("input.txt", encoding="utf8") as f:
        input_lines = f.readlines()
        print(f"First part: {p1(input_lines)}")
        print(f"Second part: {p2(input_lines)}")
        print(f"Second part: {p2_only_one_regex(input_lines)}")

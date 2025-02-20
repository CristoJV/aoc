# pylint: disable=C0114,C0116
# pylint: disable=C0413,E0611
import sys
from pathlib import Path
from typing import List

utils_path = Path(__file__).resolve().parents[2] / "utils"
sys.path.insert(0, str(utils_path))


def parse_calories(lines: List[str]):
    elfs: List[int] = []
    elf_calories: int = 0

    for line in lines:
        if len(line.strip()) == 0:
            elfs.append(elf_calories)
            elf_calories = 0
            continue
        elf_calories += int(line)
    elfs.append(elf_calories)
    return elfs


def p1(lines: List[str]):
    elfs = parse_calories(lines)
    return sorted(elfs, reverse=True)[0]


def p2(lines: List[str]):
    elfs = parse_calories(lines)
    sorted_elfs = sorted(elfs, reverse=True)
    return sorted_elfs[0] + sorted_elfs[1] + sorted_elfs[2]


if __name__ == "__main__":
    testing: bool = False
    with open(
        "input.txt" if not testing else "test.txt", encoding="utf8"
    ) as f:
        input_lines = f.readlines()
        print(f"First part: {p1(input_lines)}")
        print(f"Second part: {p2(input_lines)}")

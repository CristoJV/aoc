# pylint: disable=C0114,C0116
# pylint: disable=C0413,E0611
import sys
from pathlib import Path
from typing import List, Tuple

utils_path = Path(__file__).resolve().parents[2] / "utils"
sys.path.insert(0, str(utils_path))


def parse_locks_and_keys(lines: List[str]):
    item: List[int, int, int, int, int] = [-1 for _ in range(5)]
    item_idx: int = 0
    is_lock: bool = True
    locks: List[Tuple[int, int, int, int, int]] = []
    keys: List[Tuple[int, int, int, int, int]] = []

    for _, line in enumerate(lines):
        if line == "\n":
            if is_lock:
                locks.append(item)
            else:
                keys.append(item)
            item = [-1 for _ in range(5)]
            item_idx = 0
            continue
        if item_idx == 0:
            is_lock = (
                True if all([col == "#" for col in line.strip()]) else False
            )
        for idx, col in enumerate(line.strip()):
            if col == "#":
                item[idx] += 1
    return keys, locks


def p1(lines: List[str]):
    keys, locks = parse_locks_and_keys(lines)
    match_counts = 0
    for key in keys:
        for lock in locks:
            if all(col <= 5 for col in [a + b for a, b in zip(key, lock)]):
                match_counts += 1
    return match_counts


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

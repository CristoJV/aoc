# pylint: disable=C0114,C0116
# pylint: disable=C0413,E0611
import math
import sys
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np

utils_path = Path(__file__).resolve().parents[2] / "utils"
sys.path.insert(0, str(utils_path))


def parse_secrets(lines: List[str]):
    return map(int, lines)


def get_next_secret(secret: int, memo: Dict[int, int]):
    if secret in memo:
        return memo[secret]

    next_secret = ((secret * 64) ^ secret) % 16777216
    next_secret = (math.floor(next_secret / 32) ^ next_secret) % 16777216
    next_secret = ((next_secret * 2048) ^ next_secret) % 16777216
    memo[secret] = next_secret
    return next_secret


def p1(lines: List[str]):
    memo = {}
    count = 0
    for secret in parse_secrets(lines):
        for _ in range(2000):
            secret = get_next_secret(secret, memo)
        count += secret
    return count


def p2(lines: List[str]):
    memo = {}
    price_changes: Dict[int, List[int]] = {}
    for buyer in parse_secrets(lines):
        secret = buyer
        price_changes.setdefault(buyer, []).append(buyer % 10)
        for _ in range(2000):
            secret = get_next_secret(secret, memo)
            price_changes[buyer].append(secret % 10)

    sequences: List[Dict[Tuple[int, int, int, int], int]] = []

    for buyer, buyer_price_changes in price_changes.items():
        buyer_price_changes = np.asarray(buyer_price_changes)
        buyer_sequences: Dict[Tuple[int, int, int, int], int] = {}
        diff = buyer_price_changes[1:] - buyer_price_changes[:-1]

        for i in range(4, len(buyer_price_changes)):
            sequence = tuple(diff[i - 4 : i].tolist())
            if sequence not in buyer_sequences:
                buyer_sequences[sequence] = int(buyer_price_changes[i])

        sequences.append(buyer_sequences)

    merge_sequences: Dict[Tuple[int, int, int, int], int] = {}
    for buyer_sequences in sequences:
        for sequence, price in buyer_sequences.items():
            merge_sequences.setdefault(sequence, 0)
            merge_sequences[sequence] += price
    best_sequence = next(
        iter(
            sorted(
                merge_sequences.items(),
                key=lambda item: item[1],
                reverse=True,
            ),
        )
    )
    return best_sequence


if __name__ == "__main__":
    testing: bool = False
    with open(
        "input.txt" if not testing else "test.txt", encoding="utf8"
    ) as f:
        input_lines = f.readlines()
        print(f"First part: {p1(input_lines)}")
        print(f"Second part: {p2(input_lines)}")

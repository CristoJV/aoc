from functools import reduce
from itertools import groupby

import numpy as np
from scipy import signal


def parse_line(line):
    winning_numbers, own_numbers = line.split("|")
    card, winning_numbers = winning_numbers.split(":")
    winning_numbers = [
        int(winning_number)
        for winning_number in winning_numbers.replace("  ", " ")
        .strip()
        .split(" ")
    ]

    own_numbers = [
        int(own_number)
        for own_number in own_numbers.replace("  ", " ").strip().split(" ")
    ]

    _, card_number = card.replace("   ", " ").replace("  ", " ").split(" ")
    card_number = int(card_number)
    return int(card_number), winning_numbers, own_numbers


def part_1(lines):
    total_price = 0
    for line in lines:
        _, winning_numbers, own_numbers = parse_line(line)
        price = 0
        for number in own_numbers:
            if number in winning_numbers:
                if price == 0:
                    price += 1
                else:
                    price *= 2
        total_price += price

    return total_price


def part_2(lines):
    games = [(game_id, 1) for game_id in range(1, len(lines) + 1)]
    games = dict(games)
    for line in lines:
        card_number, winning_numbers, own_numbers = parse_line(line)
        card_count = 0
        for number in own_numbers:
            if number in winning_numbers:
                card_count += 1
        for _ in range(games[card_number]):
            for i in range(1, card_count + 1):
                if card_number + i in games:
                    games[card_number + i] += 1
    return sum(games.values())


if __name__ == "__main__":
    with open("input.txt") as f:
        lines = f.readlines()

    print(f"Part 1: {part_1(lines)}")
    print(f"Part 2: {part_2(lines)}")

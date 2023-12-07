import logging
from collections import Counter
from functools import partial


def parse_lines(lines):
    bets = [line.strip().split(" ") for line in lines]
    bets_dict = {}
    for bet in bets:
        bets_dict[bet[0]] = bet[1]
    return bets_dict


def get_score(hand, part=1):
    """
    Returns a score based on the type of hand and the cards in the hand.
    The score is an integer that is used to sort the hands.
    The first digit is the type of hand, the rest of the digits are
    composed on the cards in the hand based on the score_map.

    For example, the hand "32T3K" has a score of 20302090312 where:
    - 2 is the type of hand (1 pair)
    - 03 is the score of the card (3)
    - 02 is the score of the card (2)
    - 09 is the score of the card (T)
    - 03 is the score of the card (3)
    - 12 is the score of the card (K)
    """

    if part == 1:
        score_map = {
            "2": "01",
            "3": "02",
            "4": "03",
            "5": "04",
            "6": "05",
            "7": "06",
            "8": "07",
            "9": "08",
            "T": "09",
            "J": "10",
            "Q": "11",
            "K": "12",
            "A": "13",
        }
    else:
        score_map = {
            "J": "01",
            "2": "02",
            "3": "03",
            "4": "04",
            "5": "05",
            "6": "06",
            "7": "07",
            "8": "08",
            "9": "09",
            "T": "10",
            "Q": "11",
            "K": "12",
            "A": "13",
        }

    hand_counter = Counter(hand)

    if part == 2 and "J" in hand and hand_counter["J"] != 5:
        hand_counter_cp = hand_counter.copy()
        j_freq = hand_counter_cp.pop("J")

        freq = sorted(hand_counter_cp.values(), reverse=True)
        freq[0] += j_freq
    else:
        freq = sorted(hand_counter.values(), reverse=True)

    score = str(get_score_based_on_type(freq))
    for card in hand:
        score += score_map[card]
    return int(score)


def get_score_based_on_type(freq):
    """
    Returns a score based on the type of hand.

    7 - Five of a kind, where all five cards have the same label: AAAAA
    6 - Four of a kind, where four cards have the same label and one
        card has a different label: AA8AA
    5 - Full house, where three cards have the same label, and the
        remaining two cards share a different label: 23332
    4 - Three of a kind, where three cards have the same label, and the
        remaining two cards are each different from any other card in
        the hand: TTT98
    3 - Two pair, where two cards share one label, two other cards share
        a second label, and the remaining card has a third label: 23432
    2 - One pair, where two cards share one label, and the other three
        cards have a different label from the pair and each other: A23A4
    1 - High card, where all cards' labels are distinct: 23456

    """
    score = 0
    if len(freq) == 1:  # Five of a kind
        score = 7
    elif len(freq) == 2:  # Four of a kind or Full house
        if freq[0] == 4:  # Four of a kind
            score = 6
        elif freq[0] == 3:  # Full house
            score = 5
    elif len(freq) == 3:  # Three of a kind or Two pairs
        if freq[0] == 3:  # Three of a kind
            score = 4
        elif freq[0] == 2:  # Two pairs
            score = 3
    elif len(freq) == 4:  # One pair
        score = 2
    else:  # High card
        score = 1
    return score


def get_winnings(bets, bets_sorted):
    winnings = 0
    for i, bet in enumerate(bets_sorted):
        winnings += (i + 1) * int(bets[bet])
    return winnings


def part_1(lines):
    bets = parse_lines(lines)
    bets_sorted = sorted(bets, key=partial(get_score, part=1), reverse=False)
    winnings = get_winnings(bets, bets_sorted)
    return winnings


def part_2(lines):
    bets = parse_lines(lines)
    bets_sorted = sorted(bets, key=partial(get_score, part=2), reverse=False)
    winnings = get_winnings(bets, bets_sorted)
    return winnings


if __name__ == "__main__":
    with open("input.txt") as f:
        lines = f.readlines()

    logging.basicConfig(level=logging.INFO)

    logging.info(f"Part 1: {part_1(lines)}")
    logging.info(f"Part 2: {part_2(lines)}")

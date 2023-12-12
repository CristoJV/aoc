import logging
from collections import Counter
from itertools import groupby, product


def parse_lines(lines):
    records = [line.strip().split(" ") for line in lines]
    records = [
        [record[0], list(map(lambda x: int(x), record[1].split(",")))]
        for record in records
    ]
    return records


def check_if_record_is_valid(record, broken_springs):
    record_broken_springs = [
        len(list(g)) for k, g in groupby(record) if k == "#"
    ]
    if record_broken_springs == broken_springs:
        return True
    return False


def group_continuos_broken_hotsprings(record):
    spring_record = record[0]
    broken_spring_groups = record[1]

    unknown_count = Counter(record[0])["?"]
    unknown_combinations = list(product(list(".#"), repeat=unknown_count))
    unknown_combinations = set(unknown_combinations)

    valid_records = 0
    print(f"Number of combinations: {len(unknown_combinations)}")
    for unknown_combination in unknown_combinations:
        # replace each ? with each element of the combination
        spring_record = record[0]
        for i in range(unknown_count):
            spring_record = spring_record.replace(
                "?", unknown_combination[i], 1
            )
        # check if the record is valid
        if check_if_record_is_valid(spring_record, broken_spring_groups):
            valid_records += 1
    return valid_records


def part(lines):
    records = parse_lines(lines)
    total_valid_records = 0
    for record in records:
        valid_records = group_continuos_broken_hotsprings(record)
        total_valid_records += valid_records
    return total_valid_records


if __name__ == "__main__":
    with open("input.txt") as f:
        lines = f.readlines()

    logging.basicConfig(level=logging.INFO)

    logging.info(f"Part 1: {part(lines)}")
    # logging.info(f"Part 2: {part(lines)}")

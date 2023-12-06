import logging
from functools import reduce
from math import ceil, floor


def parse_lines(lines):
    times = lines[0].strip().split(":")[1:]
    distances = lines[1].strip().split(":")[1:]
    times = times[0].strip().split(" ")
    times = list(filter(lambda x: x != "", times))
    distances = distances[0].strip().split(" ")
    distances = list(filter(lambda x: x != "", distances))
    return times, distances


def distance_time(hold_time, time_record):
    return (time_record - hold_time) * hold_time


def count_ways_to_beat_record_using_brute_force(times, distances):
    hold_times = []
    for time_record, distance_record in zip(times, distances):
        time_record = int(time_record)
        distance_record = int(distance_record)
        solutions = []
        for hold_time in range(1, time_record):
            if distance_time(hold_time, time_record) > distance_record:
                solutions.append(hold_time)
        hold_times.append(len(solutions))
    return hold_times


def count_ways_to_beat_record(times, distances):
    """
    This method is more efficient than the brute force one.
    It uses the formula for the quadratic equation to find the
    roots of the equation:
    x^2 - time_record * x + distance_record = 0

    The roots are the hold times that will match the distance record.
     - Higher hold times than the higher root will not match the
    distance record.
    - Lower hold times than the lower root will not match the distance
    record.

    Hold times between the higher and the lower root will result in
    higher distances than the distance record.

    Therefore, the number of hold times that will match the distance
    record is the difference between the floor of the higher root and
    the ceil of the lower root.
    """
    hold_times = []
    for time_record, distance_record in zip(times, distances):
        time_record = int(time_record)
        distance_record = int(distance_record)

        higger_root = 0.5 * (
            time_record + (time_record**2 - 4 * distance_record) ** 0.5
        )
        lower_root = 0.5 * (
            time_record - (time_record**2 - 4 * distance_record) ** 0.5
        )

        if int(higger_root) == higger_root:
            # if the higger root is an integer, we need to subtract 1
            # to get the hold time that will beat the ditance record
            higger_root -= 1
        if int(lower_root) == lower_root:
            # if the lower root is an integer, we need to add 1 to get
            # the hold time that will beat the ditance record
            lower_root += 1

        count = floor(higger_root) - ceil(lower_root) + 1
        hold_times.append(count)
    return hold_times


def part_1(lines, brute_force=False):
    times, distances = parse_lines(lines)
    if brute_force:
        n_solutions = count_ways_to_beat_record_using_brute_force(
            times, distances
        )
    else:
        n_solutions = count_ways_to_beat_record(times, distances)
    return reduce(lambda x, y: x * y, n_solutions)


def part_2(lines, brute_force=False):
    times, distances = parse_lines(lines)
    time_record = [int("".join(times))]
    distance_record = [int("".join(distances))]

    logging.debug(
        f"Total time: {time_record}, Total distance: {distance_record}"
    )
    if brute_force:
        n_solutions = count_ways_to_beat_record_using_brute_force(
            time_record, distance_record
        )
    else:
        n_solutions = count_ways_to_beat_record(time_record, distance_record)
    return n_solutions[0]


if __name__ == "__main__":
    with open("input.txt") as f:
        lines = f.readlines()

    logging.basicConfig(level=logging.INFO)

    logging.info(f"Part 1: {part_1(lines, brute_force=False)}")
    logging.info(f"Part 2: {part_2(lines, brute_force=False)}")

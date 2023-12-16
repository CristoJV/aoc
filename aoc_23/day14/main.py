import logging


def parse_lines(lines):
    platform_map = [list(line.strip()) for line in lines]
    return platform_map


def cycle_tilt(platform_map, direction="north"):
    if direction == "north" or direction == "south":
        platform_map = list(map(list, zip(*platform_map)))

    # Sort each row
    platform_map_sorted = []
    for line in platform_map:
        block_list = []
        for block in "".join(line).split("#"):
            block_list.append(
                "".join(
                    sorted(
                        list(block),
                        reverse=True
                        if (direction == "north" or direction == "west")
                        else False,
                    )
                )
            )
        platform_map_sorted.append(block_list)
    platform_map = []
    for line in platform_map_sorted:
        platform_map.append("#".join(line))

    if direction == "north" or direction == "south":
        platform_map = list(map(list, zip(*platform_map)))
    return platform_map


def cycle(platform_map):
    platform_map = cycle_tilt(platform_map, "north")
    platform_map = cycle_tilt(platform_map, "west")
    platform_map = cycle_tilt(platform_map, "south")
    platform_map = cycle_tilt(platform_map, "east")
    return platform_map


def count_rolling_rocks(platform_map):
    score = 0
    for i, line in enumerate(platform_map):
        for c in line:
            if c == "O":
                score += 1 * len(platform_map) - i
    return score


def print_map(platform_map):
    print("".join(["".join(line) + "\n" for line in platform_map]))


def part_1(lines):
    platform_map = parse_lines(lines)
    platform_map = cycle_tilt(platform_map)
    score = count_rolling_rocks(platform_map)
    return score


def part_2(lines, num_cycles=1000000000, warmup_cycles=400):
    platform_map = parse_lines(lines)
    scores = {}
    last_seen = {}
    differences = []
    sequence = []

    for i in range(1, warmup_cycles + 1):
        platform_map = cycle(platform_map)
        score = count_rolling_rocks(platform_map)
        platform_map_hash = hash(
            "".join(["".join(line) for line in platform_map])
        )
        if platform_map_hash not in scores:
            scores[platform_map_hash] = score

        sequence.append(platform_map_hash)

        if platform_map_hash in last_seen:
            difference = i - last_seen[platform_map_hash]
            if difference not in differences:
                differences.append(i - last_seen[platform_map_hash])
                if len(differences) > 2:
                    loop_size = differences[-1] - differences[-2]
                    sequence = sequence[-loop_size:]
        else:
            last_seen[platform_map_hash] = i

    sequence = sequence[-loop_size:]
    index = (num_cycles - i - 1) % loop_size
    return scores[sequence[index]]


if __name__ == "__main__":
    with open("input.txt") as f:
        lines = f.readlines()

    logging.basicConfig(level=logging.INFO)

    logging.info(f"Part 1: {part_1(lines)}")
    logging.info(f"Part 2: {part_2(lines)}")

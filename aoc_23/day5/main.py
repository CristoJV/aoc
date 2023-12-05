import logging


def parse_lines(lines):
    _, seeds = lines[0].split(":")
    seeds = seeds.strip().split(" ")
    maps = "".join(lines[1:]).split("\n\n")
    maps = [m.strip().split("\n") for m in maps]
    maps = [(m[0], m[1:]) for m in maps]
    maps = dict(maps)
    for key, mappings in maps.items():
        dest = []
        src = []
        for line in mappings:
            items = line.split(" ")
            len_i = int(items[2])
            desc_i = [int(items[0]), int(items[0]) + len_i - 1]
            src_i = [int(items[1]), int(items[1]) + len_i - 1]
            dest.append(desc_i)
            src.append(src_i)
        maps[key] = {"dest": dest, "src": src}

    return seeds, maps


def part_1(lines):
    seeds, maps = parse_lines(lines)

    locations = []
    for seed in seeds:
        value = int(seed)
        for _, mapping in maps.items():
            for dest, src in zip(mapping["dest"], mapping["src"]):
                if value in range(src[0], src[1] + 1):
                    value = dest[0] + (value - src[0])
                    break
        locations.append(value)
    return min(locations)


def ranges_overlap(x, y):
    if x[0] == x[1] or y[0] == y[1]:
        return False
    return x[0] <= y[1] and y[0] <= x[1]


def overlap(x, y):
    if not ranges_overlap(x, y):
        return []
    return max(x[0], y[0]), min(x[1], y[1])


def part_2(lines):
    seeds, maps = parse_lines(lines)

    seeds_ranges = []
    for i in range(0, len(seeds), 2):
        seeds_ranges.append(
            [int(seeds[i]), int(seeds[i]) + int(seeds[i + 1]) - 1]
        )

    logging.debug(f"Seeds ranges: {seeds_ranges}")

    locations = []
    for seed_range in seeds_ranges:
        logging.debug(f"-------------------------")
        logging.debug(f"Seed range: {seed_range}")

        src_ranges = [seed_range]
        dst_ranges = []

        for key, mapping in maps.items():
            logging.debug("Key: %s", key)

            is_appended = False

            for src_range in src_ranges:
                for dest, src in zip(mapping["dest"], mapping["src"]):
                    logging.debug(f" - src: {src}")
                    logging.debug(f" - src_range: {src_range}")

                    if ranges_overlap(src_range, src):
                        logging.debug(f"Overlap: {overlap(src_range, src)}")
                        range_overlap = overlap(src_range, src)
                        dst_overlap = [
                            dest[0] + (range_overlap[0] - src[0]),
                            dest[0] + (range_overlap[1] - src[0]),
                        ]
                        logging.debug(
                            f"appending overlap mapped: {dst_overlap}"
                        )
                        dst_ranges.append(dst_overlap)
                        if src_range[0] < src[0]:
                            append_range = [src_range[0], range_overlap[0]]
                            logging.debug(
                                "Seed range starts before than the map range"
                            )
                            logging.debug(f"appending: {append_range}")
                            dst_ranges.append(append_range)

                        if src_range[1] > src[1]:
                            append_range = [range_overlap[1], src_range[1]]
                            logging.debug(
                                "Seed range ends after than the map range"
                            )
                            logging.debug(f"appending: {append_range}")
                            dst_ranges.append(
                                [range_overlap[1] + 1, src_range[1]]
                            )
                        # If the seed range is overlapped then we break
                        is_appended = True
                        break
                if not is_appended:
                    dst_ranges.append(src_range)
            src_ranges = dst_ranges
            dst_ranges = []
        locations.extend(src_ranges)
    locations_min = min([l[0] for l in locations])
    return locations_min


if __name__ == "__main__":
    with open("input.txt") as f:
        lines = f.readlines()

    logging.basicConfig(level=logging.INFO)

    logging.info(f"Part 1: {part_1(lines)}")
    logging.info(f"Part 2: {part_2(lines)}")

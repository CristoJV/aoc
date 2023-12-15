import logging


def parse_lines(lines):
    words = [word.strip() for word in lines[0].split(",")]
    return words


def to_ascii(word):
    return [ord(c) for c in word]


def hashmap(word):
    current_value = 0
    ascii_codes = to_ascii(word)
    for code in ascii_codes:
        current_value += code
        current_value *= 17
        current_value %= 256
    return current_value


def part_1(
    lines,
):
    words = parse_lines(lines)
    score = 0
    for word in words:
        score += hashmap(word)
    return score


def part_2(lines):
    words = parse_lines(lines)
    boxes = {}
    for word in words:
        label, focal = word.replace("=", "-").split("-")
        label_enc = hashmap(label)
        if len(focal) == 0:  # Remove operation
            if label_enc in boxes:
                if label in boxes[label_enc]:
                    boxes[label_enc].pop(label)
        else:  # Add operation
            if label_enc in boxes:
                boxes[label_enc][label] = focal
            else:
                boxes[label_enc] = {label: focal}
    score = 0
    for box in boxes:
        for jdx, label in enumerate(boxes[box]):
            score += (box + 1) * (jdx + 1) * int(boxes[box][label])

    return score


if __name__ == "__main__":
    with open("input.txt") as f:
        lines = f.readlines()

    logging.basicConfig(level=logging.INFO)

    logging.info(f"Part 1: {part_1(lines)}")
    logging.info(f"Part 2: {part_2(lines)}")

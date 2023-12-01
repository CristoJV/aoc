import regex as re


def sum_extreme_digits(lines, part=1):
    def map_part2(string, ind):
        mapping = {
            "one": "1",
            "two": "2",
            "three": "3",
            "four": "4",
            "five": "5",
            "six": "6",
            "seven": "7",
            "eight": "8",
            "nine": "9",
        }
        if len(string) > ind + 2 and string[ind : ind + 3] in mapping:
            return mapping[string[ind : ind + 3]]
        elif len(string) > ind + 3 and string[ind : ind + 4] in mapping:
            return mapping[string[ind : ind + 4]]
        elif len(string) > ind + 4 and string[ind : ind + 5] in mapping:
            return mapping[string[ind : ind + 5]]
        else:
            return string[ind] if string[ind].isdigit() else ""

    def map_part1(string, ind):
        return string[ind] if string[ind].isdigit() else ""

    map = map_part2 if part == 2 else map_part1
    addition = 0
    for line in lines:
        line = "".join([map(line, i) for i in range(len(line))])
        two_digits = [line[0], line[-1]]
        addition += int("".join(two_digits))
    return addition


def sum_extreme_digits_with_regex(lines, part=1):
    mapping = {
        "one": "1",
        "two": "2",
        "three": "3",
        "four": "4",
        "five": "5",
        "six": "6",
        "seven": "7",
        "eight": "8",
        "nine": "9",
    }

    if part == 1:
        pattern = "[0-9]"
    else:
        pattern = "|".join(mapping.keys()) + "|[0-9]"

    regex_pattern = re.compile(pattern)

    # Find all digits in each line
    digits = list(
        map(
            lambda line: re.findall(regex_pattern, line, overlapped=True),
            lines,
        )
    )

    # Get extreme digits
    two_digits_str = list(map(lambda digits: [digits[0], digits[-1]], digits))

    # Parse digits to int
    two_digits_int = list(
        map(
            lambda digits: int(
                "".join(
                    [
                        digit
                        if digit.isdigit()
                        else str(mapping[digit])
                        if part == 2
                        else ""
                        for digit in digits
                    ]
                )
            ),
            two_digits_str,
        )
    )

    addition = sum(two_digits_int)
    return addition


if __name__ == "__main__":
    with open("input.txt") as f:
        lines = f.readlines()
        print(f"Part 1: {sum_extreme_digits(lines, part=1)}")
        print(f"Part 2: {sum_extreme_digits(lines, part=2)}")

        print(
            f"Part 1 (with regex): {sum_extreme_digits_with_regex(lines, part=1)}"
        )
        print(
            f"Part 1 (with regex): {sum_extreme_digits_with_regex(lines, part=2)}"
        )

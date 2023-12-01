import random
import string
import unittest

import regex as re
from main import sum_extreme_digits, sum_extreme_digits_with_regex


class TestSumExtremeDigits(unittest.TestCase):
    def setUp(self) -> None:
        self.sum_extreme_digits = sum_extreme_digits

    def test_sigle_digit(self):
        self.assertEqual(self.sum_extreme_digits(["1"], part=2), 11)

    def test_combined_strings(self):
        self.assertEqual(self.sum_extreme_digits(["twone"], part=2), 21)
        self.assertEqual(self.sum_extreme_digits(["eighthree"], part=2), 83)
        self.assertEqual(self.sum_extreme_digits(["sevenine"], part=2), 79)
        self.assertEqual(self.sum_extreme_digits(["oneight"], part=2), 18)

    def test_random_generation(self):
        for i in range(10000):
            n_digits = random.randint(1, 20)
            digits = [random.randint(1, 9) for i in range(n_digits)]

            # Keep track of first and last digit
            first_digit = digits[0]
            last_digit = digits[-1]

            if n_digits > 1:
                last_digit = digits[-1]

            # Map randomly 50% of digits to string
            mapped_digits = []
            mapping = [
                "zero",
                "one",
                "two",
                "three",
                "four",
                "five",
                "six",
                "seven",
                "eight",
                "nine",
            ]

            mapped_digits = [
                str(digit) if random.random() < 0.5 else mapping[digit]
                for digit in digits
            ]

            # Insert random string between digits

            mapped_digits_with_strings = mapped_digits.copy()
            for i in range(len(mapped_digits), 0, -1):
                random_string = "".join(
                    random.choices(
                        string.ascii_lowercase, k=random.randint(0, 10)
                    )
                )

                # Check that inserting a random string does not match any digit
                # Insert a placeholder string
                mapped_digits_with_strings.insert(i, "")

                pattern = "|".join(mapping)
                while True:
                    # Generate a new random string
                    random_string = "".join(
                        random.choices(
                            string.ascii_lowercase, k=random.randint(0, 10)
                        )
                    )
                    # Check if the random string matches any digit
                    # If it does, generate a new random string
                    if re.search(pattern, random_string) is not None:
                        continue

                    # Insert the random string in the placeholder
                    mapped_digits_with_strings[i] = random_string
                    surrounded_digits = "".join(
                        mapped_digits_with_strings[i - 1 : i + 2]
                    )

                    # Check if inserting the random string generates a match
                    # between the previous and next digit
                    # If it does, generate a new random string
                    if re.search(pattern, surrounded_digits[1:-1]) is None:
                        break

            final_string = "".join(mapped_digits_with_strings)

            addition = self.sum_extreme_digits([final_string], part=2)

            self.assertEqual(
                addition,
                int("".join([str(first_digit), str(last_digit)]))
                if last_digit != -1
                else first_digit,
                msg=f"value: {final_string} ({digits}) | addition: {addition}",
            )


class TestSumExtremeDigitsWithRegex(TestSumExtremeDigits):
    def setUp(self) -> None:
        self.sum_extreme_digits = sum_extreme_digits_with_regex


if __name__ == "__main__":
    unittest.main()

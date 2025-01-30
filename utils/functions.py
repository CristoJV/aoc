import math


def count_digits(n: int):
    """
    Computes the number of digits in an integer efficiently.

    Uses logarithms when possible but falls back to string
    conversion for very large numbers due to floating-point
    precision limitations.
    (See https://stackoverflow.com/a/28883802)

    Args:
        n: The input number.

    Returns:
        int: The number of digits in `n`.
    """
    if -999999999999997 <= n <= 999999999999997:
        if n > 0:
            return int(math.log10(n)) + 1
        elif n == 0:
            return 1
        else:
            return int(math.log10(n)) + 2
    else:
        return len(str(n))

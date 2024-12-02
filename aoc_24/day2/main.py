# pylint: disable=C0114,C0116
# pylint: disable=C0413,E0611
import sys
from pathlib import Path
from typing import List

utils_path = Path(__file__).resolve().parents[2] / "utils"
sys.path.insert(0, str(utils_path))
from profile import timeit


def is_report_safe(levels: List[int]) -> bool:
    differences = [y - x for x, y in zip(levels[:-1], levels[1:])]
    if (
        all(diff >= 1 for diff in differences)
        or all(diff <= -1 for diff in differences)
    ) & (max(map(abs, differences)) <= 3):
        return True
    return False


def p1(reports: List):
    num_safe_reports = 0
    for report in reports:
        levels = list(map(int, report.split()))
        num_safe_reports += int(is_report_safe(levels))
    return num_safe_reports


#  (0.005760 seconds) This solution is more efficient as it does
#  not tries every removal
@timeit(repeats=100)
def p2(reports: List):

    def is_report_safe_with_removal(levels: List[int], removals_left: int) -> bool:

        def can_report_be_safe_by_removing_adjancent(index: int) -> bool:
            """
            Check if the report can be tolerable by removing the level
            at `index` or its neighbor.
            """
            if removals_left - 1 < 0:
                return False

            is_safe_without_current_index = is_report_safe_with_removal(
                levels[:index] + levels[index + 1 :], removals_left - 1
            )
            neigbour_index = index + 1
            is_safe_without_neighbour_index = False
            if neigbour_index < len(levels):  # This check should not fail
                is_safe_without_neighbour_index = is_report_safe_with_removal(
                    levels[:neigbour_index] + levels[neigbour_index + 1 :],
                    removals_left - 1,
                )
            return is_safe_without_current_index or is_safe_without_neighbour_index

        if removals_left < 0:
            return False

        differences = [y - x for x, y in zip(levels[:-1], levels[1:])]

        # Step 1: Check for zero differences (adjacent levels are equal)
        zero_diff_indices = [idx for idx, diff in enumerate(differences) if diff == 0]

        if len(zero_diff_indices) > 1:
            # More than one zero difference cannot be fixed with one removal
            return False
        elif len(zero_diff_indices) == 1:
            # Try removing the problematic level
            index = zero_diff_indices[0]
            return is_report_safe_with_removal(
                levels[:index] + levels[index + 1 :], removals_left - 1
            )
        # Step 2: Check if the sequence is monotonic.
        # By now, all zeroes should be removed.
        is_monotonic = all(diff >= 0 for diff in differences) or all(
            diff <= 0 for diff in differences
        )
        if not is_monotonic:
            # The sequence is not monotonic; check if it can be made monotonic
            # by removing one level
            increasing_indices = [
                index for index, value in enumerate(differences) if value > 0
            ]
            decreasing_indices = [
                index for index, value in enumerate(differences) if value < 0
            ]
            if (len(increasing_indices) > 1) and (len(decreasing_indices) > 1):
                result = False
            elif len(increasing_indices) == 1:
                result = can_report_be_safe_by_removing_adjancent(increasing_indices[0])
            elif len(decreasing_indices) == 1:
                result = can_report_be_safe_by_removing_adjancent(decreasing_indices[0])
            else:
                result = False
            return result

        # Step 3: Check for differences outside the allowed range
        invalid_diff_indices = [
            idx for idx, diff in enumerate(differences) if abs(diff) > 3
        ]
        if len(invalid_diff_indices) > 1:
            result = False
        elif len(invalid_diff_indices) == 0:
            result = True
        else:
            # Exactly one invalid difference
            result = can_report_be_safe_by_removing_adjancent(invalid_diff_indices[0])
        return result

    num_safe_reports = 0
    for report in reports:
        levels = list(map(int, report.split()))
        num_safe_reports += is_report_safe_with_removal(levels, removals_left=1)
    return num_safe_reports


@timeit(repeats=100)  # (0.014792 seconds)
def p2_brute(reports: List):
    """
    Count the number of safe reports for Part 2 using a brute-force approach.
    """
    num_safes = 0
    for report in reports:
        levels = list(map(int, report.split()))
        if is_report_safe(levels):
            num_safes += 1
        else:
            for idx, _ in enumerate(levels):
                new_levels = levels[:idx] + levels[idx + 1 :]
                if is_report_safe(new_levels):
                    num_safes += 1
                    break
    return num_safes


if __name__ == "__main__":
    with open("input.txt", encoding="utf8") as f:
        input_reports = f.readlines()
        print(f"First part: {p1(input_reports)}")
        print(f"Second part: {p2(input_reports)}")
        print(f"Second part: {p2_brute(input_reports)}")

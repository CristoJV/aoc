# pylint: disable=C0114,C0116
# pylint: disable=C0413,E0611
import sys
from pathlib import Path
from typing import List

utils_path = Path(__file__).resolve().parents[2] / "utils"
sys.path.insert(0, str(utils_path))


def p1(lines: List[str]):
    disc_map = lines[0].strip()
    map_length = len(disc_map)
    final_is_empty = (map_length % 2) == 0

    data_blocks = {}
    empty_slots = {}
    for i, block_info in enumerate(disc_map):
        if (i % 2) == 0:
            data_blocks[i] = int(block_info)
        if (i % 2) == 1:
            empty_slots[i] = int(block_info)
    j = map_length - (2 if final_is_empty else 1)
    checksum = 0
    block_index = 0
    for i in range(map_length):
        if (i % 2) == 0:
            value = sum(
                map(
                    (i // 2).__mul__,
                    range(block_index, block_index + data_blocks[i]),
                )
            )
            checksum += value
            block_index = block_index + data_blocks[i]
        if (i % 2) == 1 and j > i:
            break_flag_is_empty = False
            while empty_slots[i] > 0:
                while data_blocks[j] > 0:
                    checksum += j // 2 * block_index
                    block_index += 1
                    data_blocks[j] -= 1
                    empty_slots[i] -= 1
                    if empty_slots[i] < 1:
                        break_flag_is_empty = True
                        break
                if break_flag_is_empty:
                    break
                j -= 2
                if j == i:
                    break
    return checksum


def get_slots_info(disc_map):
    data_slots = {}
    empty_slots = {}
    block_index = 0
    for i, block_slots in enumerate(disc_map):
        block_slots = int(block_slots)
        if (i % 2) == 0:
            data_slots[i // 2] = [block_index, block_slots]
            block_index += block_slots
        if (i % 2) == 1:
            empty_slots[i // 2] = [block_index, block_slots]
            block_index += block_slots
    return data_slots, empty_slots


def p2(lines: List[str]):

    data_slots, empty_slots = get_slots_info(lines[0].strip())
    for data_id, data_slot in sorted(data_slots.items(), reverse=True):
        # pylint: disable=C0201,C0206
        for empty_slot_idx in empty_slots.keys():
            empty_slot = empty_slots[empty_slot_idx]
            if data_slot[0] < empty_slot[0]:
                break
            if data_slot[1] <= empty_slot[1]:
                # Update the data indexes
                data_slot[0] = empty_slot[0]
                # Update the empty_slot indexes and len
                rest_slots = empty_slot[1] - data_slot[1]
                if rest_slots <= 0:
                    # print(f"Deleting empty slot {empty_slot_idx}")
                    empty_slots.pop(empty_slot_idx)
                else:
                    new_block_index = empty_slot[0] + data_slot[1]
                    empty_slots[empty_slot_idx] = (
                        new_block_index,
                        rest_slots,
                    )
                break
    checksum = 0
    for data_id, data_slot in data_slots.items():
        value = sum(
            map(
                (data_id).__mul__,
                range(data_slot[0], data_slot[0] + data_slot[1]),
            )
        )
        checksum += value
    return checksum


if __name__ == "__main__":
    with open("input.txt", encoding="utf8") as f:
        input_lines = f.readlines()
        print(f"First part: {p1(input_lines)}")
        print(f"Second part: {p2(input_lines)}")

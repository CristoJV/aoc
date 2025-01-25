# pylint: disable=C0114,C0116
# pylint: disable=C0413,E0611
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple

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
    slot_index = 0
    for i in range(map_length):
        if (i % 2) == 0:
            value = sum(
                map(
                    (i // 2).__mul__,
                    range(slot_index, slot_index + data_blocks[i]),
                )
            )
            checksum += value
            slot_index = slot_index + data_blocks[i]
        if (i % 2) == 1 and j > i:
            break_flag_is_empty = False
            while empty_slots[i] > 0:
                while data_blocks[j] > 0:
                    checksum += j // 2 * slot_index
                    slot_index += 1
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


@dataclass
class BlockInfo:
    id: int
    slot_index: int
    length: int


def get_slots_info(
    disc_map,
) -> Tuple[List[BlockInfo], List[BlockInfo]]:
    data_slots = []
    empty_slots = []
    slot_index = 0
    for i, length in enumerate(disc_map):
        length = int(length)
        if (i % 2) == 0:
            data_slots.append(BlockInfo(i // 2, slot_index, length))
        if (i % 2) == 1:
            empty_slots.append(BlockInfo(0, slot_index, length))
        slot_index += length
    return data_slots, empty_slots


def p2(lines: List[str]):
    data_slots, empty_slots = get_slots_info(lines[0].strip())

    for _, data_slot in reversed(list(enumerate(data_slots))):
        for empty_slot_idx, empty_slot in enumerate(empty_slots):
            if data_slot.slot_index < empty_slot.slot_index:
                break

            if data_slot.length <= empty_slot.length:
                # Update the data indexes
                data_slot.slot_index = empty_slot.slot_index
                # Update the empty_slot indexes and len
                remaining_length = empty_slot.length - data_slot.length
                if remaining_length <= 0:
                    empty_slots.pop(empty_slot_idx)
                else:
                    new_slot_index = empty_slot.slot_index + data_slot.length
                    empty_slots[empty_slot_idx] = BlockInfo(
                        0,
                        new_slot_index,
                        remaining_length,
                    )
                break
    checksum = 0

    for data_slot in data_slots:
        value = sum(
            map(
                (data_slot.id).__mul__,
                range(
                    data_slot.slot_index,
                    data_slot.slot_index + data_slot.length,
                ),
            )
        )
        checksum += value
    return checksum


if __name__ == "__main__":
    with open("input.txt", encoding="utf8") as f:
        input_lines = f.readlines()
        print(f"First part: {p1(input_lines)}")
        print(f"Second part: {p2(input_lines)}")

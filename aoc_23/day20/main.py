import functools
import logging
import math
from collections import deque
from dataclasses import dataclass
from typing import List


def parse_circuit(lines):
    modules = [line.strip().split(" -> ") for line in lines]
    modules_ = {}
    for module in modules:
        modules_[module[0]] = module[1].split(", ")
    modules = modules_

    def custom_key(key):
        if key[0].isalpha():
            return (0, key)
        else:
            return (1, key)

    modules = dict(sorted(modules.items(), key=lambda x: custom_key(x[0])))
    modules_dict = {}

    broadcasted_modules = []

    for module_name, out_modules in modules.items():
        module_type, module_name = module_name[0], module_name[1:]

        if module_type == "%":
            modules_dict[module_name] = Flipflop(module_name, out_modules)

        elif module_type == "&":
            modules_dict[module_name] = Conjuntion(module_name, out_modules)

            for module_name_i, out_modules_i in modules.items():
                for out_module in out_modules_i:
                    if out_module == module_name:
                        modules_dict[module_name].add_in_module(
                            module_name_i[1:]
                        )
        else:
            broadcasted_modules = out_modules
    return modules_dict, broadcasted_modules


class SignalState:
    LOW = 0
    HIGH = 1


@dataclass
class Signal:
    sender: str
    receiver: str
    state: SignalState


class Flipflop:
    def __init__(self, name: str, out_modules: List[str]):
        self.name = name
        self.state = "off"
        self.out_modules = out_modules

    def update(self, signal: Signal):
        signals = []
        if signal.state == SignalState.LOW:
            self.state = "off" if self.state == "on" else "on"
            signal_state = (
                SignalState.HIGH if self.state == "on" else SignalState.LOW
            )
            for out_module in self.out_modules:
                signals.append(Signal(self.name, out_module, signal_state))
        return signals


class Conjuntion:
    def __init__(self, name: str, out_modules: List[str]):
        self.name = name
        self.in_modules = {}
        self.out_modules = out_modules

    def add_in_module(self, in_module: str):
        self.in_modules[in_module] = SignalState.LOW

    def update(self, signal: Signal):
        signals = []
        self.in_modules[signal.sender] = signal.state
        if all(
            value == SignalState.HIGH for value in self.in_modules.values()
        ):
            signal_state = SignalState.LOW
        else:
            signal_state = SignalState.HIGH
        for out_module in self.out_modules:
            signals.append(Signal(self.name, out_module, signal_state))
        return signals


def part_1(lines):
    modules, broascast = parse_circuit(lines)
    queue = deque()
    low_pulses = 0
    high_pulses = 0
    for _ in range(1000):
        low_pulses += 1
        for init in broascast:
            queue.append(Signal("broadcast", init, SignalState.LOW))

        while queue:
            signal = queue.popleft()
            if signal.state == SignalState.HIGH:
                high_pulses += 1
            else:
                low_pulses += 1
            if signal.receiver in modules:
                signals = modules[signal.receiver].update(signal)
                for sig in signals:
                    queue.append(sig)
    return low_pulses * high_pulses


def part_2(lines):
    pass


if __name__ == "__main__":
    with open("input.txt") as f:
        lines = f.readlines()

    logging.basicConfig(level=logging.INFO)

    logging.info(f"Part 1: {part_1(lines)}")
    logging.info(f"Part 2: {part_2(lines)}")

import functools
import logging
from enum import Enum


class Signal(Enum):
    LOW = 0
    HIGH = 1


class Broadcast:
    def __init__(self):
        self.count_low_pulses = 0
        self.count_high_pulses = 0

        self.outputs = []

    def connect_output(self, output):
        self.outputs.append(output)

    def update(self, input, pulse):
        if pulse == 0:
            self.count_low_pulses += 1
        else:
            self.count_high_pulses += 1
        return [
            functools.partial(output.update, self, Signal.LOW)
            for output in self.outputs
        ]


class FlipFlop:
    def __init__(self):
        self.outputs = []
        self._state = False
        self.count_low_pulses = 0
        self.count_high_pulses = 0
        self.outputs = []

    def connect_output(self, output):
        self.outputs.append(output)

    def update(self, input, pulse):
        if pulse == Signal.HIGH:  # Don't update the state if the pulse is HIGH
            self.count_high_pulses += 1
        elif pulse == Signal.LOW:  # Update the state if the pulse is LOW
            self._state = not self._state
            self.count_low_pulses += 1
            return [
                functools.partial(output.update, self, self._state)
                for output in self.outputs
            ]


class Conjuction:
    def __init__(self):
        self.outputs = {}
        self.count_low_pulses = 0
        self.count_high_pulses = 0

    def connect_output(self, output):
        self.outputs[output] = Signal.LOW

    def update(self, input, pulse):
        self.outputs[input] = pulse
        if pulse == 0:
            self.count_low_pulses += 1
        else:
            self.count_high_pulses += 1

        return [
            functools.partial(output.update, self, self.send())
            for output in self.outputs
        ]

    def send(self):
        return int(not all(self.outputs.values()))


def parse_lines(lines):
    modules = [line.strip().split(" -> ") for line in lines]
    modules_ = {}
    for module in modules:
        modules_[module[0]] = module[1].split(", ")
    modules = modules_
    return modules


def part_1(lines):
    modules = parse_lines(lines)
    modules_dict = {}
    aliases = {}

    for input_module, _ in modules.items():
        if input_module[0] == "%":
            modules_dict[input_module] = FlipFlop()
        elif input_module[0] == "&":
            modules_dict[input_module] = Conjuction()
        else:
            modules_dict[input_module] = Broadcast()
        aliases[input_module[1:]] = input_module
        aliases[input_module] = input_module

    for input_module, outputs in modules.items():
        for output in outputs:
            if output not in aliases:
                aliases[output] = output
                modules_dict[output] = Broadcast()

            modules_dict[input_module].connect_output(
                modules_dict[aliases[output]]
            )
            aliases[output] = aliases[input_module]

    start_module = "broadcaster"
    pending_signals = modules_dict[start_module].update(
        start_module, Signal.HIGH
    )

    print(pending_signals)

    while len(pending_signals) > 0:
        for signal in pending_signals:
            followed_signals = signal()
            pending_signals.remove(signal)
            if followed_signals is not None:
                pending_signals.extend(followed_signals)

    # for input, outputs in modules.items():
    #     print(f"module {input}")
    #     for output in outputs:
    #         if output not in aliases:
    #             aliases[output] = output
    #             modules_dict[output] = Broadcast()

    #         print(output)
    #         print(aliases[output], aliases[input])
    #         modules_dict[aliases[output]].update(
    #             input, modules_dict[aliases[input]].send()
    #         )

    total_low_pulses = 0
    total_high_pulses = 0
    for module in modules_dict.values():
        total_low_pulses += module.count_low_pulses
        total_high_pulses += module.count_high_pulses
    print(total_low_pulses, total_high_pulses)


def part_2(lines):
    pass


if __name__ == "__main__":
    with open("example_input.txt") as f:
        lines = f.readlines()

    logging.basicConfig(level=logging.INFO)

    logging.info(f"Part 1: {part_1(lines)}")
    logging.info(f"Part 2: {part_2(lines)}")

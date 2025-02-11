# pylint: disable=C0114,C0116
# pylint: disable=C0413,E0611
import sys
from pathlib import Path
from typing import List

utils_path = Path(__file__).resolve().parents[2] / "utils"
sys.path.insert(0, str(utils_path))
from collections import deque


def parse_gates(lines: List[str]):
    full_str = "".join(lines)
    registers, gates, *_ = full_str.split("\n\n")
    registers = registers.split("\n")
    registers = {
        input: int(value)
        for input_wire in registers
        for input, value in [input_wire.split(":")]
    }
    gates = gates.split("\n")
    gates.pop(-1)
    input_wires = [gate.split("->")[0].strip() for gate in gates]
    output_wire = [gate.split("->")[1].strip() for gate in gates]
    gates_graph = {}
    for idx, input_wire in enumerate(input_wires):
        output_i = output_wire[idx]
        input_left, operator, input_right = input_wire.split(" ")
        gates_graph[output_i] = ([input_left, input_right], operator)

    for input_wire, value in registers.items():
        gates_graph[input_wire] = ([], value)

    return gates_graph, registers


def topological_sort_kahn(graph):
    indegree = {node: 0 for node in graph}
    for node in graph:
        for neighbor in graph[node][0]:
            indegree[neighbor] += 1
    queue = deque([node for node in graph if indegree[node] == 0])
    topo_order = []
    while queue:
        node = queue.popleft()
        topo_order.append(node)

        for neighbor in graph[node][0]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                queue.append(neighbor)

    if len(topo_order) == len(graph):
        topo_order.reverse()
        return topo_order
    else:
        print("Graph has a cycle")
        return []


def p1(lines: List[str]):
    gates, registers = parse_gates(lines)
    topo_order = topological_sort_kahn(gates)
    for register in topo_order:
        if register not in registers:
            inputs, operand = gates[register]
            match operand:
                case "XOR":
                    register_value = (
                        registers[inputs[0]] ^ registers[inputs[1]]
                    )
                case "AND":
                    register_value = (
                        registers[inputs[0]] & registers[inputs[1]]
                    )
                case "OR":
                    register_value = (
                        registers[inputs[0]] | registers[inputs[1]]
                    )
                case _:
                    register_value = 2
            registers[register] = register_value
    sorted_registers = {
        key: registers[key]
        for key in sorted(registers, reverse=True)
        if key[0] == "z"
    }

    number = "".join(map(str, sorted_registers.values()))
    number = int(number, base=2)
    return number


def p2(lines: List[str]):
    pass


if __name__ == "__main__":
    testing: bool = False
    with open(
        "input.txt" if not testing else "test.txt", encoding="utf8"
    ) as f:
        input_lines = f.readlines()
        print(f"First part: {p1(input_lines)}")
        print(f"Second part: {p2(input_lines)}")
        print(f"Second part: {p2(input_lines)}")

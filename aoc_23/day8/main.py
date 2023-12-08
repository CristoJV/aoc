import logging
from math import lcm


def parse_lines(lines):
    instructions, nodes = "".join(lines).strip().split("\n\n")
    nodes = dict([node.split(" = ") for node in nodes.split("\n")])
    nodes = {key: value[1:-1].split(", ") for key, value in nodes.items()}
    instructions = list(
        map(int, instructions.replace("L", "0").replace("R", "1"))
    )
    return instructions, nodes


def count_steps_to_next_z(src_node, dst_nodes, nodes, instructions):
    next_node = nodes[src_node][instructions[0]]
    idx = 1
    steps_to_next_z = 1

    while next_node not in dst_nodes:
        if next_node in nodes:
            next_node = nodes[next_node][instructions[idx]]
        else:
            warning_msg = (
                f"Node {next_node} does not have a connection to {next_node}"
            )
            logging.warning(warning_msg)
            break
        steps_to_next_z += 1
        idx = (idx + 1) % len(instructions)

    return steps_to_next_z, next_node


def part_1(lines):
    instructions, nodes = parse_lines(lines)
    src_node = "AAA"
    dst_nodes = ["ZZZ"]
    steps, _ = count_steps_to_next_z(src_node, dst_nodes, nodes, instructions)
    return steps


def part_2(lines):
    """
    The goal is to find the shortest path from each starting node 'A' to
    any end node "Z", ensuring that all "Z" nodes are reached with the
    same amount of steps. If a "Z" node is visited bot other remain
    unvisited, the journey continues to the next "Z" node.

    The task involves counting the steps from "A" to "Z", and then, the
    steps from "Z" to its next "Z".

    Then, we can iterate over the "A" starting noded, until we find the
    steps needed for all the journeys to end in Z at the same time.

    Interestingly, certain constraints in the connections between nodes
    simplifies the challende greatly.

    First, the routes from each "Z" endes up in the same "Z" node
    recursively.

    Second, number of steps from "A" to "Z" is the same that from the
    reached "Z" to itself.

    Therefore, we can simply count the steps from "A" to "Z", and find
    the least common multiple of these steps. That's it.

    For verification, we are compunting and comparing the steps from "A"
    to "Z", and from "Z" to its next "Z". While this is not necessary
    for solving the challenge it provides valuable insights into its
    nature.
    """

    instructions, nodes = parse_lines(lines)
    src_nodes = [node for node in nodes if node[-1] == "A"]
    dst_nodes = [node for node in nodes if node[-1] == "Z"]

    steps_z_to_z = {}
    next_z_from_z = {}

    for src_node in dst_nodes:
        steps_to_next_z, next_node = count_steps_to_next_z(
            src_node, dst_nodes, nodes, instructions
        )
        steps_z_to_z[src_node] = steps_to_next_z
        next_z_from_z[src_node] = next_node

    steps_a_to_z = {}
    next_z_from_a = {}

    for src_node in src_nodes:
        steps_to_next_z, next_node = count_steps_to_next_z(
            src_node, dst_nodes, nodes, instructions
        )

        steps_a_to_z[src_node] = steps_to_next_z
        next_z_from_a[src_node] = next_node

    # Found out next_z_from_z is always the same, so it is recursive
    logging.debug(f"next_z_from_z: {next_z_from_z}")

    steps_to_z = {}
    for src_node in next_z_from_a:
        next_z = next_z_from_a[src_node]
        steps_from_a = steps_a_to_z[src_node]
        steps_from_z = steps_z_to_z[next_z]

        steps_to_z[next_z] = {"from_a": steps_from_a, "from_z": steps_from_z}

    # Found out from_a and from_z are the same
    logging.debug(f"steps_to_z: {steps_to_z}")

    steps = [steps_to_z[next_z]["from_a"] for next_z in steps_to_z]
    steps = lcm(*steps)
    return steps


if __name__ == "__main__":
    with open("input.txt") as f:
        lines = f.readlines()

    logging.basicConfig(level=logging.INFO)

    logging.info(f"Part 1: {part_1(lines)}")
    logging.info(f"Part 2: {part_2(lines)}")

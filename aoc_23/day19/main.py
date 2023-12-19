import logging


def greater_than(dictionary, key, value):
    if key not in dictionary:
        return False
    return dictionary[key] > value


def lower_than(dictionary, key, value):
    if key not in dictionary:
        return False
    return dictionary[key] < value


def parse_lines(lines):
    workflows, parts = "".join(lines).split("\n\n")
    workflows = workflows.split("\n")
    workflows = [workflow.split("{") for workflow in workflows]
    workflows_ = {}

    for i, workflow in enumerate(workflows):
        workflow_name = workflow[0]
        workflow_instructions = []
        instructions = workflow[1][:-1]

        for instruction in instructions.split(","):
            split_instruction = instruction.split(":")

            if len(split_instruction) == 1:
                next_workflow = split_instruction[0]
                key = None
                value = None
                condition = None
            else:
                next_workflow = split_instruction[1]
                key = split_instruction[0][0]
                value = int(split_instruction[0][2:])
                condition = split_instruction[0][1]
            workflow_instructions.append(
                {
                    "next": next_workflow,
                    "key": key,
                    "value": value,
                    "condition": condition,
                }
            )
        workflows_[workflow_name] = workflow_instructions
    workflows = workflows_
    parts = parts.split("\n")
    parts = [part[1:-1].split(",") for part in parts]

    parts_ = []
    for part in parts:
        part_ = {}
        for p in part:
            a, b = p.split("=")
            part_[a] = int(b)
        parts_.append(part_)
    parts = parts_

    return workflows, parts


def part_1(
    lines,
    part,
):
    workflows, parts = parse_lines(lines)
    total_score = 0

    for part in parts:
        is_rated = False
        current_workflows = workflows["in"]
        while not is_rated:
            for workflow in current_workflows:
                is_condition_met = False
                if workflow["condition"] == "<":
                    is_condition_met = lower_than(
                        part, workflow["key"], workflow["value"]
                    )
                elif workflow["condition"] == ">":
                    is_condition_met = greater_than(
                        part, workflow["key"], workflow["value"]
                    )
                else:
                    is_condition_met = True

                if is_condition_met:
                    if workflow["next"] == "A":
                        is_rated = True
                        score = sum(part.values())
                        total_score += score
                        break
                    elif workflow["next"] == "R":
                        is_rated = True
                        break
                    else:
                        current_workflows = workflows[workflow["next"]]
                        break
                else:
                    continue

    return total_score


if __name__ == "__main__":
    with open("input.txt") as f:
        lines = f.readlines()

    logging.basicConfig(level=logging.INFO)

    logging.info(f"Part 1: {part_1(lines, part=1)}")
    # logging.info(f"Part 2: {part_2(lines)}")

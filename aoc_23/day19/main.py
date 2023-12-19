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


def part_1(lines):
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


def create_graph(workflows):
    previous_nodes = {}
    cost = {}
    open_set = set()
    open_set.add("in")

    a_count = 0
    while len(open_set) > 0:
        node = open_set.pop()
        # Get the conditions for the current node
        accumulated_conditions = []
        for conditions in workflows[node]:
            key = conditions["key"]
            condition = conditions["condition"]
            oposite_condition = "<=" if condition == ">" else ">="
            value = conditions["value"]
            next_node = conditions["next"]

            if next_node == "A":
                a_count += 1
                next_node = f"{a_count}"
                previous_nodes[next_node] = node
                cost[next_node] = (
                    accumulated_conditions + [(key, condition, value)]
                    if condition is not None
                    else accumulated_conditions
                )
                accumulated_conditions.append((key, oposite_condition, value))
                continue

            elif next_node == "R":
                accumulated_conditions.append((key, oposite_condition, value))
                continue

            previous_nodes[next_node] = node
            if value is None:
                cost[next_node] = accumulated_conditions
            else:
                cost[next_node] = accumulated_conditions + [
                    (key, condition, value)
                ]
                accumulated_conditions.append((key, oposite_condition, value))
            open_set.add(next_node)
    return previous_nodes, cost


def part_2(lines):
    workflows, parts = parse_lines(lines)
    previous_nodes, cost = create_graph(workflows)
    a_count = 1
    total_valid = 0
    while str(a_count) in previous_nodes:
        a_id = str(a_count)
        accumulated_cost = cost[a_id]
        node = a_id
        while previous_nodes[node] != "in":
            node = previous_nodes[node]
            accumulated_cost.extend(cost[node])
        a_range = [1, 4000]
        x_range = [1, 4000]
        s_range = [1, 4000]
        m_range = [1, 4000]

        for a_cost in accumulated_cost:
            key = a_cost[0]
            if key is None:
                continue
            condition = a_cost[1]
            value = a_cost[2]
            if condition == ">":
                if key == "a":
                    a_range[0] = max(a_range[0], value + 1)
                elif key == "x":
                    x_range[0] = max(x_range[0], value + 1)
                elif key == "s":
                    s_range[0] = max(s_range[0], value + 1)
                elif key == "m":
                    m_range[0] = max(m_range[0], value + 1)
            elif condition == ">=":
                if key == "a":
                    a_range[0] = max(a_range[0], value)
                elif key == "x":
                    x_range[0] = max(x_range[0], value)
                elif key == "s":
                    s_range[0] = max(s_range[0], value)
                elif key == "m":
                    m_range[0] = max(m_range[0], value)
            elif condition == "<":
                if key == "a":
                    a_range[1] = min(a_range[1], value - 1)
                elif key == "x":
                    x_range[1] = min(x_range[1], value - 1)
                elif key == "s":
                    s_range[1] = min(s_range[1], value - 1)
                elif key == "m":
                    m_range[1] = min(m_range[1], value - 1)
            elif condition == "<=":
                if key == "a":
                    a_range[1] = min(a_range[1], value)
                elif key == "x":
                    x_range[1] = min(x_range[1], value)
                elif key == "s":
                    s_range[1] = min(s_range[1], value)
                elif key == "m":
                    m_range[1] = min(m_range[1], value)

        valid = (
            (a_range[1] - a_range[0] + 1)
            * (x_range[1] - x_range[0] + 1)
            * (s_range[1] - s_range[0] + 1)
            * (m_range[1] - m_range[0] + 1)
        )
        a_count += 1
        total_valid += valid
    return total_valid


if __name__ == "__main__":
    with open("input.txt") as f:
        lines = f.readlines()

    logging.basicConfig(level=logging.INFO)

    logging.info(f"Part 1: {part_1(lines)}")
    logging.info(f"Part 2: {part_2(lines)}")

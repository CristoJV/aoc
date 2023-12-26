import logging
from queue import PriorityQueue

import numpy as np


def parse_lines(lines):
    graph = [list(map(int, list(line.strip()))) for line in lines]
    return graph


def dijkstra(graph, start, min_consecutive_steps=4, max_consecutive_steps=10):
    def get_neighbors(
        node, graph, min_consecutive_steps=4, max_consecutive_steps=10
    ):
        def is_within_bounds(x, y, graph):
            return x >= 0 and x < len(graph[0]) and y >= 0 and y < len(graph)

        """
        Returns a list of neighbors of the form
        (x, y, direction, consecutive_steps_in_direction, cost)

        The returned neighbors will follow the following rules:
        - If consecutive_steps_in_direction is less than min_consecutive_steps, the
            neighbor will continue in the same direction until min_consecutive_steps is
            reached.
        - If consecutive_steps_in_direction is greater than max_consecutive_steps, the
            neighbor will change direction forcefully.
        - If consecutive_steps_in_direction is between min_consecutive_steps and max_consecutive_steps,
            the neighbor can either continue in the same direction or change
            direction.

        """
        neighbors = []
        x, y, direction, consecutive_steps_in_direction = node

        for idx, dir in enumerate(directions):
            if idx == direction:
                if (
                    min_consecutive_steps
                    <= consecutive_steps_in_direction
                    < max_consecutive_steps
                ):
                    # You can either continue in the same direction
                    new_x = x + dir[0]
                    new_y = y + dir[1]
                    if is_within_bounds(new_x, new_y, graph):
                        cost = graph[new_x, new_y]
                        neighbors.append(
                            (
                                new_x,
                                new_y,
                                idx,
                                consecutive_steps_in_direction + 1,
                                cost,
                            )
                        )

                elif consecutive_steps_in_direction < min_consecutive_steps:
                    # Forcefully continue in the same direction until
                    # min_consecutive_steps is reached
                    consecutive_steps = consecutive_steps_in_direction
                    cost = 0
                    while consecutive_steps <= min_consecutive_steps:
                        new_x = x + dir[0] * (consecutive_steps)
                        new_y = y + dir[1] * (consecutive_steps)

                        if not is_within_bounds(new_x, new_y, graph):
                            break
                        consecutive_steps += 1
                        cost = cost + graph[new_x, new_y]

                    if is_within_bounds(new_x, new_y, graph):
                        neighbors.append(
                            (new_x, new_y, idx, consecutive_steps, cost)
                        )

                elif consecutive_steps_in_direction >= max_consecutive_steps:
                    # Forcefully change direction. This means that the
                    # consecutive_steps_in_direction is reset to 1
                    continue
                else:
                    logging.error("NOT contemplated case")

            elif idx != direction:
                if consecutive_steps_in_direction < min_consecutive_steps:
                    # Forcefully continue in the same direction until
                    # min_consecutive_steps is reached
                    continue

                # Allow changing direction and continue in the same
                # direction for min_consecutive_steps steps

                # Don't allow going back in the same direction
                if direction == 0 and idx == 2:
                    continue
                elif direction == 1 and idx == 3:
                    continue
                elif direction == 2 and idx == 0:
                    continue
                elif direction == 3 and idx == 1:
                    continue

                cost = 0
                consecutive_steps = 0
                while consecutive_steps < min_consecutive_steps:
                    consecutive_steps += 1
                    new_x = x + dir[0] * consecutive_steps
                    new_y = y + dir[1] * consecutive_steps
                    if not is_within_bounds(new_x, new_y, graph):
                        break
                    cost = cost + graph[new_x, new_y]
                if is_within_bounds(new_x, new_y, graph):
                    neighbors.append(
                        (new_x, new_y, idx, min_consecutive_steps, cost)
                    )
        return neighbors

    # Directions are 0: up, 1: right, 2: down, 3: left
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]

    # Dijkstra's algorithm
    visited = set()
    prev = {}
    queue = PriorityQueue()
    queue.put((0, start))

    costs = np.full((*graph.shape, 4, max_consecutive_steps + 1), np.inf)

    while not queue.empty():
        d, node = queue.get()
        visited.add(node)

        for neighbor in get_neighbors(
            node, graph, min_consecutive_steps, max_consecutive_steps
        ):
            (
                x_neig,
                y_neig,
                direction_neig,
                consecutive_steps_in_direction_neig,
                cost,
            ) = neighbor

            neighbor = neighbor[:-1]

            path_dist = d + cost

            if neighbor in visited:
                continue

            if (
                path_dist
                < costs[
                    x_neig,
                    y_neig,
                    direction_neig,
                    consecutive_steps_in_direction_neig,
                ]
            ):
                costs[
                    x_neig,
                    y_neig,
                    direction_neig,
                    consecutive_steps_in_direction_neig,
                ] = path_dist
                prev[neighbor] = node
                queue.put((path_dist, neighbor))
    return costs, prev


def part(lines, min_consecutive_steps=4, max_consecutive_steps=10):
    graph = np.asarray(parse_lines(lines))

    # The nodes are of the form
    # (x, y, direction, consecutive_steps_in_direction)
    start_node = (0, 0, 1, 1)

    # Find the shortest path
    dist, prev = dijkstra(
        graph,
        start=start_node,
        min_consecutive_steps=min_consecutive_steps,
        max_consecutive_steps=max_consecutive_steps,
    )

    # Find the shortest path to the end node from all possible
    # directions
    min_dist = None
    for dir in range(4):
        for steps in range(max_consecutive_steps + 1):
            end_node = (len(graph) - 1, len(graph[0]) - 1, dir, steps)
            if min_dist is None:
                min_dist = end_node
            else:
                min_dist = (
                    end_node if dist[end_node] < dist[min_dist] else min_dist
                )
            print(f"Direction: {dir}, steps: {steps} cost: {dist[end_node]}")

    # Plot the shortest path
    path = []
    u = min_dist
    while u != (0, 0, 1, 1):
        x, y, _, _ = u
        path.append((x, y))
        u = prev[u]
    for i in range(len(graph)):
        for j in range(len(graph[0])):
            if (i, j) in path:
                print("X", end="")
            else:
                print("_", end="")
        print()

    return int(dist[min_dist])


if __name__ == "__main__":
    with open("input.txt") as f:
        lines = f.readlines()

    logging.basicConfig(level=logging.INFO)

    logging.info(
        f"Part 1: {part(lines, min_consecutive_steps=1, max_consecutive_steps=3)}"
    )
    logging.info(
        f"Part 2: {part(lines, min_consecutive_steps=4, max_consecutive_steps=10)}"
    )

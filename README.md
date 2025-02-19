
# 🎄 Advent of Code Solutions (AoC)

Welcome to my collection of solutions for the **Advent of Code** challenges! 🌟
Here you'll find my solutions to the yearly programming puzzles published at [adventofcode.com](https://adventofcode.com/).

Happy coding! 💻✨

---
## 🚀 Progress

This table tracks my progress for each year, showing:
- **Day**: The challenge number (1–25).
- **Status**: Completion status, where:
  - ⭐⭐ → Both parts solved
  - ⭐▶️ → Part 1 solved, Part 2 in progress
  - ⭐ → Only Part 1 solved
  - ⬜ → Not attempted yet
- **Strategy**: The key approach used for solving each part of the challenge.

---

### 📆 2024

| Day  | Status | Strategy (Part 1) | Strategy (Part 2) |
|------|--------|------------------|------------------|
| 1️⃣  | ⭐⭐ |  |  |
| 2️⃣  | ⭐⭐ |  |  |
| 3️⃣  | ⭐⭐ |  |  |
| 4️⃣  | ⭐⭐ |  |  |
| 5️⃣  | ⭐⭐ |  |  |
| 6️⃣  | ⭐⭐ |  |  |
| 7️⃣  | ⭐⭐ |  |  |
| 8️⃣  | ⭐⭐ |  |  |
| 9️⃣  | ⭐⭐ |  |  |
| 1️⃣0️⃣ | ⭐⭐ |  |  |
| 1️⃣1️⃣ | ⭐⭐ |  |  |
| 1️⃣2️⃣ | ⭐▶️ |  |  |
| 1️⃣3️⃣ | ⭐⭐ |  |  |
| 1️⃣4️⃣ | ⭐⭐ | **Modular Arithmetic** | **2D Entropy using Kernel-based Joint Histogram** <br> *Like it!* 👍 <br><br> This approach evaluates local spatial dependencies using a 5-pixel cross-shaped kernel: {(center, top, right, bottom, left)}. The joint histogram is built from these patterns, forming a probability distribution. The key insight was detecting the image with minimum entropy to reveal the hidden Christmas tree. |
| 1️⃣5️⃣ | ⭐⭐ | **Recursion** |  |
| 1️⃣6️⃣ | ⭐⭐ |  |  |
| 1️⃣7️⃣ | ⭐⭐ |  |  |
| 1️⃣8️⃣ | ⭐⭐ |  |  |
| 1️⃣9️⃣ | ⭐⭐ |  |  |
| 2️⃣0️⃣ | ⭐▶️| **Djistra** <br> Using array indexing instead of complex dictionaries. The algorithm precomputes two cost maps: one tracking the shortest path from the start to all points and another from the end to all points. To handle potential shortcuts, the total cost for each one is determined by summing the cost from the start to the shortcut's entry and the cost from the end to the shorcut's exit, considering both possible directions.|  |
| 2️⃣1️⃣ | ⬜ |  |  |
| 2️⃣2️⃣ | ⭐⭐ | **Memoization** | ⚡ Could by optimized by skipping redundant price iterations |
| 2️⃣3️⃣ | ⭐⭐ | **Lexicographic ordering** <br> Processing nodes in a fixed order (i.e. alphabetically) to avoid redundant computations when detecting triangle cycles. | **Set Intersection** <br> *Like it!* 👍 <br><br> This algorithm creates a list of sets, where each set includes a node and all its connected nodes. <br><br> Example: If node `a` is indirectly connected to `b`, `c`, and `d`, the resulting set would be { `a`, `b`, `c`, `d` }. <br><br> The algorithm then computes pairwise intersections between these sets, avoiding redundant computations. It counts the number of unique intersections and selects the intersection with the highest occurrence. Finally, if the number of occurrences is greater than or equal to the size of the set, we have a winner. 🎯 <br><br> ⚡ Could be optimized by using the [Bron-Kerbosch](https://en.wikipedia.org/wiki/Bron%E2%80%93Kerbosch_algorithm) algorithm|
| 2️⃣4️⃣ | ⭐ | **Topological sorting - [Kahn's algorithm](https://en.wikipedia.org/wiki/Topological_sorting)** |  |
| 2️⃣5️⃣ | ⭐ | ⚡ Parsing the input into locks and keys could by optimized |  |

---

### 📆 2023

| Day  | Status | Strategy (Part 1) | Strategy (Part 2) |
|------|--------|------------------|------------------|
| 1️⃣  | ⬜ |  |  |
| 2️⃣  | ⬜ |  |  |
| 3️⃣  | ⬜ |  |  |
| 4️⃣  | ⬜ |  |  |
| 5️⃣  | ⬜ |  |  |
| 6️⃣  | ⬜ |  |  |
| 7️⃣  | ⬜ |  |  |
| 8️⃣  | ⬜ |  |  |
| 9️⃣  | ⬜ |  |  |
| 1️⃣0️⃣  | ⬜ |  |  |
| 1️⃣1️⃣ | ⬜ |  |  |
| 1️⃣2️⃣ | ⬜ |  |  |
| 1️⃣3️⃣ | ⬜ |  |  |
| 1️⃣4️⃣ | ⬜ |  |  |
| 1️⃣5️⃣ | ⬜ |  |  |
| 1️⃣6️⃣ | ⬜ |  |  |
| 1️⃣7️⃣ | ⬜ |  |  |
| 1️⃣8️⃣ | ⬜ |  |  |
| 1️⃣9️⃣ | ⬜ |  |  |
| 2️⃣0️⃣ | ⬜ |  |  |
| 2️⃣1️⃣ | ⬜ |  |  |
| 2️⃣2️⃣ | ⬜ |  |  |
| 2️⃣3️⃣ | ⬜ |  |  |
| 2️⃣4️⃣ | ⬜ |  |  |
| 2️⃣5️⃣ | ⬜ |  |  |

---

## 🎯 Contributions

If you have suggestions or improvements, feel free to **fork** this repository and submit a **pull request**.

I hope this repository is helpful and that you enjoy solving the **Advent of Code** challenges as much as I do! 🚀🎄

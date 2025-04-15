# 📄 Input File Format: `astar.txt`

This file defines the graph structure and heuristics for use with the `astar.py` implementation of the A* search algorithm.

## 🧠 File Overview

Each line in `astar.txt` represents a **single node** in the graph. The format includes:
- The node's name (identifier)
- Its heuristic value (`h(n)`)
- Followed by **zero or more** pairs of:
  - A neighboring node
  - The cost (weight) of the edge to that neighbor

---

## 📌 File Format
<node> <heuristic> <neighbor1> <weight1> <neighbor2> <weight2> ...

- `<node>`: The unique identifier for the node (e.g., `A`, `B`, `City1`)
- `<heuristic>`: An integer representing the estimated cost from this node to the goal (used by A* search)
- `<neighborX>`: The name of a node connected to `<node>`
- `<weightX>`: The cost to travel from `<node>` to `<neighborX>`

---

## 📘 Example
A 10 B 4 C 2 B 6 C 1 D 5 C 4 D 8 E 10 D 2 E 2 E 0


This defines:
- Node `A` with heuristic 10 and edges:
  - to `B` with weight 4
  - to `C` with weight 2
- Node `B` with heuristic 6 and edges to `C` and `D`, etc.

---

## 🛠 Notes

- The graph is assumed to be **undirected**, so if `A` connects to `B`, and `B` does not explicitly list `A`, the edge still exists.
- Heuristic values should be **non-negative integers**.
- Ensure there are **no duplicate node definitions**.
- All nodes used as neighbors should be defined **somewhere** in the file with their own line and heuristic value.

---

## 🚀 Usage
This file is read automatically by `astar.py`. Just make sure it is in the **same directory** as the script, and formatted correctly.

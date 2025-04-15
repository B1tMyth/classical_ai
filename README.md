# Input File Format: `astar.txt`

This file defines the graph structure and heuristics for use with the `astar.py` implementation of the A* search algorithm.

## File Overview

Each line in `astar.txt` represents a **single node** in the graph. The format includes:
- The node's name (identifier)
- Its heuristic value (`h(n)`)
- Followed by **zero or more** pairs of:
  - A neighboring node
  - The cost (weight) of the edge to that neighbor

---

## File Format
`<node>` `<heuristic>` `<neighbor1>` `<weight1>` `<neighbor2>` `<weight2>` ...

- `<node>`: The unique identifier for the node (e.g., `A`, `B`, `City1`)
- `<heuristic>`: An integer representing the estimated cost from this node to the goal (used by A* search)
- `<neighborX>`: The name of a node connected to `<node>`
- `<weightX>`: The cost to travel from `<node>` to `<neighborX>`

---

## Example
A 10 B 4 C 2  
B 6 C 1 D 5  
C 4 D 8 E 10 D 2  
E 2 E 0  

This defines:
- Node `A` with heuristic 10 and edges:
  - to `B` with weight 4
  - to `C` with weight 2
- Node `B` with heuristic 6 and edges to `C` and `D`, etc.

---

## Notes
- The graph is assumed to be **undirected**, so if `A` connects to `B`, and `B` does not explicitly list `A`, the edge still exists.
- Heuristic values should be **non-negative integers**.
- Ensure there are **no duplicate node definitions**.
- All nodes used as neighbors should be defined **somewhere** in the file with their own line and heuristic value.

---

## Usage
This file is read automatically by `astar.py`. Just make sure it is in the **same directory** as the script, and formatted correctly.


# Turn-Based Combat Simulation with Minimax & Alpha-Beta Pruning
This project simulates a **strategic turn-based combat game** between an attacker and a defender. The attacker attempts to inflict maximum damage, while the defender tries to minimize it. The simulation uses the **Minimax algorithm** with **Alpha-Beta pruning** to find the optimal attack strategy in a simplified combat scenario.

---

## Concept
- **Two Players**: Attacker (Maximizer) and Defender (Minimizer).
- **Turns**: Each turn has two plies (one move for each player).
- **Tree Depth**: Computed as `2 * number_of_turns`.
- **Branching Factor**: Equal to the number of bullets or choices per move.
- **Terminal Nodes**: Represent total damage inflicted after all moves.
- **Goal**: Determine the maximum possible damage attacker can deal assuming optimal play.

---

## Input Format
The program prompts the user for the following:  
ENTER NUMBER OF TURNS: # e.g., 3  
ENTER INITIAL HP: # e.g., 75 (if 0, a random value between 50-100 is used)  
ENTER NUMBER OF BULLETS: # e.g., 2  
ENTER SPACE SEPARATED UPPER AND LOWER BOUND FOR THE NEGATIVE HP: 5 15  

- **Turns**: Number of full turns (each has 2 plies).
- **Initial HP**: Starting health of the defender.
- **Bullets**: Number of choices (branches) available per move.
- **Damage Range**: Tuple of integers representing min and max damage.

---

## How It Works
- A game tree is constructed from the given depth and branching factor.
- Each leaf (terminal node) represents a possible total damage value.
- The attacker aims to **maximize** this damage.
- The defender attempts to **minimize** it.
- The simulation uses **alpha-beta pruning** to avoid evaluating unnecessary branches.

---

## Output
Sample console output:  
DEPTH AND BRANCHES RATIO IS 6:2  
TERMINAL STATES (LEAF NODE VALUES) ARE 6, 13, 7, 8, ...  
LEFT LIFE(HP) OF THE DEFENDER AFTER MAXIMUM DAMAGE CAUSED BY THE ATTACKER IS 59  
AFTER ALPHA-BETA PRUNING LEAF NODE COMPARISONS 20  

- **Depth and Branching Ratio**: Shows how the game tree is structured.
- **Terminal States**: All leaf node values representing damage.
- **Remaining HP**: Defender's final HP after optimal attacker strategy.
- **Leaf Node Comparisons**: How many terminal nodes were visited due to pruning.

---

## Code Structure
- `GameTreeNode`: Node in the game tree.
- `GameTree`: Builds a tree based on input parameters.
- `AlphaBetaSearchAgent`: Performs alpha-beta search on the tree.
- `InputValue`, `NodeValue`: Helper classes for structured data handling.
- `get_input()`: Collects and validates user input.
- `print_to_console()`: Outputs the results in a readable format.

---

## Run the Simulation
Make sure you have Python 3.6+ installed. Then run:

```bash
python alpha_beta.py
```


# Genetic Algorithm Simulation for Transaction Optimization
This project simulates a **Genetic Algorithm (GA)** applied to a series of financial transactions. The objective is to evolve a binary solution (genotype) that selects a subset of transactions whose net balance (deposits minus withdrawals) is as close to zero as possible.

---

## Problem Description
You're given a list of transactions, each being either a deposit (`d`) or a withdrawal (`w`) with an associated amount. The goal is to select a subset of these transactions such that the total balance is near zero. The Genetic Algorithm evolves a population of binary strings (chromosomes), where each bit represents whether a transaction is included (1) or excluded (0).

---

## Input Format
The input is read from a file named `input.txt`.
Example `input.txt`:
5 d 200 w 150 d 300 w 100 d 50

- The first line (`5`) indicates the number of transactions (also the size of each binary string).
- Each subsequent line is a transaction with type `d` (deposit) or `w` (withdrawal) and an integer amount.

---

## Genetic Algorithm Components
### Genotype
- A binary string (e.g., `11001`) representing inclusion/exclusion of transactions.

### Fitness Function
- A normalized inverse function of the absolute balance:
  fitness = 1 / (1 + |net_balance|) normalized = (fitness - offset) / normalization_constant

### Selection
- Picks the top-N fittest individuals based on fitness scores.

### Crossover
- Two parents produce offspring by swapping parts of their genes at a defined crossover point.

### Mutation
- Randomly flips a bit in the binary string with a certain probability (`mutation_factor`).

### Evolution
- Repeats selection → crossover → mutation over multiple generations.
- Stops early if an individual with perfect fitness (`1`) is found.

---

## Parameters
Set within the script:

```python
ga.selection_per_generation = 5
ga.num_of_combination_for_crossover = 3
ga.crossover_point = random.choice(range(1, int(reg_size)))
ga.mutation_factor = 0.4
```

You can adjust these to explore the GA's behavior.
Make sure you have Python 3.7+ installed and a valid input.txt in the same directory.

```bash
python genetic_algorithm_simulation.py
```

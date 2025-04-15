import math, random
from collections import deque
from typing import NamedTuple, Tuple, List


class GameTreeNode:
    def __init__(self, parent=None, value=None, alpha=-math.inf, beta=math.inf):
        self.value = value
        self.alpha = alpha
        self.beta = beta
        self.parent = parent
        self.children = []
        self.is_terminal = False

    def __str__(self) -> str:
        return f"Value: {self.value}, alpha: {self.alpha} beta: {self.beta}"

    def __repr__(self) -> str:
        return str(self)

    def add_child(self, node: "GameTreeNode") -> None:
        self.children.append(node)


class GameTree:
    def __init__(
        self, root: "GameTreeNode", depth: int, branches: int, terminals: List
    ):
        self.root = root
        self.depth = depth
        self.branches = branches
        self.terminals = deque(terminals)
        self._build_tree()

    def _build_tree(self, node=None, depth=None):
        node = node or self.root
        depth = self.depth if depth is None else depth

        if depth == 0:
            node.value = self.terminals.popleft()
            node.is_terminal = True
            return

        for _ in range(self.branches):
            child = GameTreeNode(node)
            node.add_child(child)
            self._build_tree(child, depth - 1)

    def print_children(self, node=None):
        node = node or self.root
        if node is self.root:
            print(node)
        if not node.children:
            return
        for child in node.children:
            print(child)
            self.print_children(child)

    def __str__(self) -> str:
        return f"BRANCHES {self.branches}, DEPTH {self.depth}, TERMINAL NODES {math.pow(self.branches, self.depth)}"

    def __repr__(self) -> str:
        return str(self)


class Result(NamedTuple):
    optimal_value: int
    comparisons: int


class AlphaBetaSearchAgent:
    def __init__(self, game_state: GameTree):
        self._game_state = game_state
        self._visited_terminals = 0

    def alpha_beta(
        self, node: "GameTreeNode", depth: int, alpha=-math.inf, beta=math.inf
    ):
        node = node or self._game_state.root

        if depth == 0:
            return node.value

        if not depth % 2:
            node_attr = self._search_max(node, depth, alpha, beta)
        else:
            node_attr = self._search_min(node, depth, alpha, beta)

        node.value, node.alpha, node.beta = node_attr
        return node_attr.value

    def _search_max(self, state, depth, alpha, beta):
        value = -math.inf
        for successor in state.children:
            if successor.is_terminal:
                self._visited_terminals += 1
            value = max(value, self.alpha_beta(successor, depth - 1, alpha, beta))
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return NodeValue(value, alpha, beta)

    def _search_min(self, state, depth, alpha, beta):
        value = math.inf
        for successor in state.children:
            if successor.is_terminal:
                self._visited_terminals += 1
            value = min(value, self.alpha_beta(successor, depth - 1, alpha, beta))
            beta = min(beta, value)
            if alpha >= beta:
                break
        return NodeValue(value, alpha, beta)


class NodeValue(NamedTuple):
    value: int
    alpha: int
    beta: int


class InputValue(NamedTuple):
    num_of_turns: int
    initial_hp: int
    num_of_bullets: int
    damage_range: Tuple[int, int]


def get_input() -> InputValue:
    turns = int(input("ENTER NUMBER OF TURNS:"))
    hp = int(input("ENETER INITIAL HP:"))
    bullets = int(input("ENTER NUMBER OF BULLETS:"))
    tup = tuple(
        map(
            int,
            input(
                "ENTER SPACE SEPARATED UPPER AND LOWER BOUND FOR THE NEGATIVE HP: "
            ).split(),
        )
    )
    hp = random.randint(50, 100) if not hp else hp
    return InputValue(turns, hp, bullets, tup)


def print_to_console(inputs: InputValue, terminals: List, agent: AlphaBetaSearchAgent):
    remaining_hp = inputs.initial_hp - agent._game_state.root.value
    print(
        f"DEPTH AND BRANCHES RATIO IS {2 * inputs.num_of_turns}:{inputs.num_of_bullets}"
    )
    print(
        f"TERMINAL STATES (LEAF NODE VALUES) ARE {', '.join(str(x) for x in terminals)}"
    )
    print(
        f"LEFT LIFE(HP) OF THE DEFENDER AFTER MAXIMUM DAMAGE CAUSED BY THE ATTACKER IS {remaining_hp}"
    )
    print(f"AFTER ALPHA-BETA PRUNING LEAF NODE COMPARISONS {agent._visited_terminals}")


if __name__ == "__main__":
    inp = get_input()
    depth = 2 * inp.num_of_turns
    branches = inp.num_of_bullets
    lower, upper = inp.damage_range
    terminals = [
        random.randint(*inp.damage_range) for _ in range(int(math.pow(branches, depth)))
    ]
    game_tree = GameTree(GameTreeNode(), depth, branches, terminals)
    agent = AlphaBetaSearchAgent(game_tree)
    agent.alpha_beta(game_tree.root, depth)
    print_to_console(inp, terminals, agent)

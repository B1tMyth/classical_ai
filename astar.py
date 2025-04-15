import networkx as nx
from queue import PriorityQueue


G = nx.Graph()
with open("Input file.txt", "r") as f:
    for line in f:
        a, b, *c = line.strip().split()
        elist = [(a, c[i], int(c[i + 1])) for i in range(0, len(c), 2)]
        G.add_node(a, h=int(b))
        G.add_weighted_edges_from(elist)


def astar(start_node, goal_node, G):
    pqueue = PriorityQueue()
    pqueue.put((0, start_node))

    cost_so_far = {start_node: 0}
    parent = {start_node: None}

    while not pqueue.empty():
        _, current_node = pqueue.get()

        if current_node == goal_node:
            path = []
            while current_node is not None:
                path.append(current_node)
                current_node = parent[current_node]
            return " -> ".join(path[::-1])

        for next_node, node_attr in G[current_node].items():
            if next_node == parent[current_node]:
                continue
            new_cost = cost_so_far[current_node] + node_attr["weight"]

            if next_node in cost_so_far and new_cost >= cost_so_far[next_node]:
                continue

            cost_so_far[next_node] = new_cost
            priority = new_cost + G.nodes[next_node]["h"]
            pqueue.put((priority, next_node))
            parent[next_node] = current_node

    print("NO PATH FOUND")


if __name__ == "__main__":
    start = input("Start node: ")
    destination = input("Destination: ")
    print(astar(start, destination, G))

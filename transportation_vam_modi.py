import numpy as np
from collections import deque


def transportation_cost(allocation, cost):
    return np.sum(allocation * cost)


def vogel_approximation(cost, supply, demand):
    """Construct an initial basic feasible solution using VAM."""
    cost = np.array(cost, dtype=float)
    supply = list(supply)
    demand = list(demand)
    m, n = cost.shape
    allocation = np.zeros((m, n), dtype=float)
    active_rows = set(range(m))
    active_cols = set(range(n))

    while active_rows and active_cols:
        candidates = []

        for i in active_rows:
            values = sorted(cost[i, j] for j in active_cols)
            penalty = values[1] - values[0] if len(values) >= 2 else values[0]
            candidates.append((penalty, values[0], "row", i))

        for j in active_cols:
            values = sorted(cost[i, j] for i in active_rows)
            penalty = values[1] - values[0] if len(values) >= 2 else values[0]
            candidates.append((penalty, values[0], "col", j))

        _, _, kind, index = max(candidates, key=lambda x: (x[0], -x[1]))

        if kind == "row":
            i = index
            j = min(active_cols, key=lambda col: (cost[i, col], col))
        else:
            j = index
            i = min(active_rows, key=lambda row: (cost[row, j], row))

        quantity = min(supply[i], demand[j])
        allocation[i, j] = quantity
        supply[i] -= quantity
        demand[j] -= quantity

        if supply[i] == 0:
            active_rows.remove(i)
        if demand[j] == 0:
            active_cols.remove(j)

    return allocation


def find_cycle(basic_cells, entering):
    """Find the closed loop needed for a MODI improvement."""
    graph = {}
    for i, j in basic_cells:
        r, c = ("r", i), ("c", j)
        graph.setdefault(r, []).append(c)
        graph.setdefault(c, []).append(r)

    start = ("r", entering[0])
    target = ("c", entering[1])
    parent = {start: None}
    queue = deque([start])

    while queue:
        node = queue.popleft()
        if node == target:
            break
        for nxt in graph.get(node, []):
            if nxt not in parent:
                parent[nxt] = node
                queue.append(nxt)

    if target not in parent:
        raise RuntimeError("Could not construct a closed transportation cycle.")

    nodes = []
    node = target
    while node is not None:
        nodes.append(node)
        node = parent[node]
    nodes.reverse()

    path_cells = []
    for a, b in zip(nodes[:-1], nodes[1:]):
        if a[0] == "r" and b[0] == "c":
            path_cells.append((a[1], b[1]))
        else:
            path_cells.append((b[1], a[1]))

    plus_cells = [entering]
    minus_cells = []
    plus = False
    for cell in path_cells:
        (plus_cells if plus else minus_cells).append(cell)
        plus = not plus

    return plus_cells, minus_cells


def modi(cost, initial_allocation):
    """Optimize the VAM BFS using the MODI (u-v) method."""
    cost = np.array(cost, dtype=float)
    allocation = np.array(initial_allocation, dtype=float).copy()
    m, n = cost.shape

    for iteration in range(50):
        basic = [(i, j) for i in range(m) for j in range(n)
                 if allocation[i, j] > 1e-9]

        if len(basic) != m + n - 1:
            raise RuntimeError("Degenerate basis encountered; epsilon handling is required.")

        u = [None] * m
        v = [None] * n
        u[0] = 0.0

        changed = True
        while changed:
            changed = False
            for i, j in basic:
                if u[i] is not None and v[j] is None:
                    v[j] = cost[i, j] - u[i]
                    changed = True
                elif v[j] is not None and u[i] is None:
                    u[i] = cost[i, j] - v[j]
                    changed = True

        if any(x is None for x in u + v):
            raise RuntimeError("Could not determine all MODI potentials.")

        delta = np.full((m, n), np.nan)
        for i in range(m):
            for j in range(n):
                if (i, j) not in basic:
                    delta[i, j] = cost[i, j] - u[i] - v[j]

        min_delta = np.nanmin(delta)
        print(f"\n--- MODI Iteration {iteration} ---")
        print("u =", [round(x, 2) for x in u])
        print("v =", [round(x, 2) for x in v])
        print("Minimum reduced cost =", round(min_delta, 2))

        if min_delta >= -1e-9:
            return allocation

        entering = np.unravel_index(np.nanargmin(delta), delta.shape)
        print(f"Entering cell = (S{entering[0] + 1}, D{entering[1] + 1})")

        plus_cells, minus_cells = find_cycle(basic, entering)
        theta = min(allocation[i, j] for i, j in minus_cells)
        print("Theta =", int(theta))

        for i, j in plus_cells:
            allocation[i, j] += theta
        for i, j in minus_cells:
            allocation[i, j] -= theta

        allocation[np.abs(allocation) < 1e-9] = 0
        print("New allocation:")
        print(allocation.astype(int))
        print("New cost =", int(transportation_cost(allocation, cost)))

    raise RuntimeError("MODI exceeded the iteration limit.")


# Sources: S1=40, S2=30, S3=50, S4=20
# Destinations: D1=20, D2=30, D3=25, D4=35, D5=30
# Cost matrix:
#        D1 D2 D3 D4 D5
# S1      6  8 10  9  7
# S2      9 11  8  7 12
# S3     10  7 12  8  9
# S4      8  9  6 10 11

cost = np.array([
    [6, 8, 10, 9, 7],
    [9, 11, 8, 7, 12],
    [10, 7, 12, 8, 9],
    [8, 9, 6, 10, 11]
])

supply = [40, 30, 50, 20]
demand = [20, 30, 25, 35, 30]

print("\n--- Initial BFS (Vogel's Approximation Method) ---")
initial = vogel_approximation(cost, supply, demand)
print(initial.astype(int))
print("Initial transportation cost =", int(transportation_cost(initial, cost)))

allocation = modi(cost, initial)

print("\n--- Final Optimal Shipment Plan ---")
print(allocation.astype(int))
print("\nMinimum transportation cost =", int(transportation_cost(allocation, cost)))

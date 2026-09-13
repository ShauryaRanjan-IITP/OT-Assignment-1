import numpy as np
from collections import deque


def northwest_corner(supply, demand):
    """Create an initial basic feasible solution using NW Corner."""
    supply = supply.copy()
    demand = demand.copy()

    m = len(supply)
    n = len(demand)
    allocation = np.zeros((m, n), dtype=float)

    i = 0
    j = 0

    while i < m and j < n:
        q = min(supply[i], demand[j])
        allocation[i, j] = q
        supply[i] -= q
        demand[j] -= q

        if supply[i] == 0 and demand[j] == 0:
            i += 1
            j += 1
        elif supply[i] == 0:
            i += 1
        else:
            j += 1

    return allocation


def transportation_cost(allocation, cost):
    return np.sum(allocation * cost)


def find_cycle(basic_cells, entering, m, n):
    """Find the closed loop created by adding the entering cell."""
    graph = {}

    for i, j in basic_cells:
        r = ("r", i)
        c = ("c", j)
        graph.setdefault(r, []).append(c)
        graph.setdefault(c, []).append(r)

    start = ("r", entering[0])
    target = ("c", entering[1])

    parent = {start: None}
    q = deque([start])

    while q:
        node = q.popleft()
        if node == target:
            break
        for nxt in graph.get(node, []):
            if nxt not in parent:
                parent[nxt] = node
                q.append(nxt)

    path_nodes = []
    node = target
    while node is not None:
        path_nodes.append(node)
        node = parent[node]
    path_nodes.reverse()

    path_cells = []
    for a, b in zip(path_nodes[:-1], path_nodes[1:]):
        if a[0] == "r" and b[0] == "c":
            path_cells.append((a[1], b[1]))
        else:
            path_cells.append((b[1], a[1]))

    plus_cells = [entering]
    minus_cells = []
    plus = False

    for cell in path_cells:
        if not plus:
            minus_cells.append(cell)
        else:
            plus_cells.append(cell)
        plus = not plus

    return plus_cells, minus_cells


def modi(cost, supply, demand):
    """Solve a balanced transportation problem using NW Corner + MODI."""
    cost = np.array(cost, dtype=float)
    m, n = cost.shape
    allocation = northwest_corner(supply, demand)

    print("\n--- Initial BFS (Northwest Corner) ---")
    print(allocation.astype(int))
    print("Initial cost =", int(transportation_cost(allocation, cost)))

    for iteration in range(50):
        basic = [
            (i, j)
            for i in range(m)
            for j in range(n)
            if allocation[i, j] > 0
        ]

        if len(basic) != m + n - 1:
            raise RuntimeError("Degenerate basis encountered. Add epsilon handling.")

        u = [None] * m
        v = [None] * n
        u[0] = 0

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

        delta = np.full((m, n), np.nan)
        for i in range(m):
            for j in range(n):
                if (i, j) not in basic:
                    delta[i, j] = cost[i, j] - (u[i] + v[j])

        print(f"\n--- MODI Iteration {iteration} ---")
        print("u =", [round(x, 2) for x in u])
        print("v =", [round(x, 2) for x in v])
        print("Minimum reduced cost =", round(np.nanmin(delta), 2))

        min_delta = np.nanmin(delta)
        if min_delta >= -1e-9:
            return allocation

        entering = np.unravel_index(np.nanargmin(delta), delta.shape)
        print(f"Entering cell = (S{entering[0] + 1}, D{entering[1] + 1})")

        plus_cells, minus_cells = find_cycle(basic, entering, m, n)
        theta = min(allocation[i, j] for i, j in minus_cells)
        print("Theta =", int(theta))

        for i, j in plus_cells:
            allocation[i, j] += theta
        for i, j in minus_cells:
            allocation[i, j] -= theta

        print("New allocation:")
        print(allocation.astype(int))
        print("New cost =", int(transportation_cost(allocation, cost)))

    raise RuntimeError("MODI exceeded the iteration limit.")


# ---------------------------------------------------------
# Problem data
# ---------------------------------------------------------
# Sources: S1=40, S2=30, S3=50, S4=20
# Destinations: D1=20, D2=30, D3=25, D4=35, D5=30
# Cost matrix (per unit):
#        D1 D2 D3 D4 D5
# S1      6  8 10  9  7
# S2      9 11  8  7 12
# S3     10  7 12  8  9
# S4      8  9  6 10 11
# ---------------------------------------------------------

cost = np.array([
    [6, 8, 10, 9, 7],
    [9, 11, 8, 7, 12],
    [10, 7, 12, 8, 9],
    [8, 9, 6, 10, 11]
])

supply = [40, 30, 50, 20]
demand = [20, 30, 25, 35, 30]

allocation = modi(cost, supply, demand)

print("\n--- Final Optimal Shipment Plan ---")
print(allocation.astype(int))
print("\nMinimum transportation cost =", int(transportation_cost(allocation, cost)))

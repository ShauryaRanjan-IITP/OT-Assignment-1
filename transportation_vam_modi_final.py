import numpy as np
from collections import deque


def transportation_cost(allocation, cost):
    return np.sum(allocation * cost)


def vogel(cost, supply, demand):
    # Find an initial basic feasible solution using VAM.
    cost = np.array(cost, dtype=float)
    supply = list(map(float, supply))
    demand = list(map(float, demand))

    m, n = cost.shape
    allocation = np.zeros((m, n))
    rows = set(range(m))
    cols = set(range(n))

    while rows and cols:
        choices = []

        # Calculate penalties for all active rows.
        for i in rows:
            values = sorted(cost[i, j] for j in cols)
            penalty = values[1] - values[0] if len(values) > 1 else values[0]
            choices.append((penalty, values[0], 0, i))

        # Calculate penalties for all active columns.
        for j in cols:
            values = sorted(cost[i, j] for i in rows)
            penalty = values[1] - values[0] if len(values) > 1 else values[0]
            choices.append((penalty, values[0], 1, j))

        # Highest penalty is selected. In a tie, use the lower minimum cost.
        penalty, _, kind, index = max(
            choices,
            key=lambda x: (x[0], -x[1])
        )

        if kind == 0:
            i = index
            j = min(cols, key=lambda x: (cost[i, x], x))
        else:
            j = index
            i = min(rows, key=lambda x: (cost[x, j], x))

        quantity = min(supply[i], demand[j])
        allocation[i, j] = quantity
        supply[i] -= quantity
        demand[j] -= quantity

        if supply[i] == 0:
            rows.remove(i)

        if demand[j] == 0:
            cols.remove(j)

    return allocation


def find_cycle(basic_cells, entering):
    # Find the closed loop used to improve the transportation plan.
    graph = {}

    for i, j in basic_cells:
        r = ("r", i)
        c = ("c", j)
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
        raise ValueError("Could not find a transportation cycle.")

    nodes = []
    node = target

    while node is not None:
        nodes.append(node)
        node = parent[node]

    nodes.reverse()

    cells = []
    for a, b in zip(nodes[:-1], nodes[1:]):
        if a[0] == "r":
            cells.append((a[1], b[1]))
        else:
            cells.append((b[1], a[1]))

    # Entering cell gets '+'. The signs then alternate around the loop.
    cycle = [(entering, 1)]
    sign = -1

    for cell in cells:
        cycle.append((cell, sign))
        sign *= -1

    return cycle


def modi(cost, allocation):
    # Improve the VAM solution using the MODI (u-v) method.
    cost = np.array(cost, dtype=float)
    allocation = allocation.copy()
    m, n = cost.shape

    for iteration in range(50):
        basic = [
            (i, j)
            for i in range(m)
            for j in range(n)
            if allocation[i, j] > 1e-9
        ]

        if len(basic) != m + n - 1:
            raise ValueError(
                "Degenerate basis encountered. "
                "This example expects a non-degenerate BFS."
            )

        # Find u_i and v_j from u_i + v_j = c_ij
        # for every occupied cell.
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

        if any(x is None for x in u + v):
            raise ValueError("Could not determine all MODI potentials.")

        # For a minimization problem:
        # delta_ij = c_ij - u_i - v_j
        delta = np.full((m, n), np.nan)

        for i in range(m):
            for j in range(n):
                if (i, j) not in basic:
                    delta[i, j] = cost[i, j] - u[i] - v[j]

        minimum = np.nanmin(delta)

        print(f"\nMODI iteration {iteration}")
        print("u =", [round(x, 2) for x in u])
        print("v =", [round(x, 2) for x in v])
        print("Most negative delta =", round(minimum, 2))

        # If every reduced cost is non-negative, the solution is optimal.
        if minimum >= -1e-9:
            return allocation

        entering = np.unravel_index(
            np.nanargmin(delta),
            delta.shape
        )

        print(
            "Entering cell =",
            f"S{entering[0] + 1}, D{entering[1] + 1}"
        )

        cycle = find_cycle(basic, entering)

        minus_cells = [
            cell
            for cell, sign in cycle
            if sign == -1
        ]

        theta = min(
            allocation[i, j]
            for i, j in minus_cells
        )

        print("Theta =", int(theta))

        for cell, sign in cycle:
            i, j = cell
            allocation[i, j] += sign * theta

        allocation[np.abs(allocation) < 1e-9] = 0

        print("New allocation:")
        print(allocation.astype(int))
        print(
            "New transportation cost =",
            int(transportation_cost(allocation, cost))
        )

    raise ValueError("MODI did not converge.")


# ----------------------------------------------------------
# CLASSICAL HITCHCOCK TRANSPORTATION MODEL
#
# Three plants supply a common product to four warehouses.
# This is a balanced transportation problem.
#
# Supply:
#     S1 = 40
#     S2 = 30
#     S3 = 50
#
# Demand:
#     D1 = 25
#     D2 = 30
#     D3 = 20
#     D4 = 45
#
# Total supply = total demand = 120.
#
# Unit transportation cost:
#
#        D1  D2  D3  D4
# S1     14  11   6  14
# S2     14   8   6   4
# S3     14   1   4   7
# ----------------------------------------------------------

cost = np.array([
    [14, 11, 6, 14],
    [14, 8, 6, 4],
    [14, 1, 4, 7]
])

supply = [40, 30, 50]
demand = [25, 30, 20, 45]

print("\n========== VAM ==========")

allocation = vogel(cost, supply, demand)

print("\nInitial VAM allocation:")
print(allocation.astype(int))

print(
    "Initial transportation cost =",
    int(transportation_cost(allocation, cost))
)

print("\n========== MODI ==========")

allocation = modi(cost, allocation)

print("\nFinal optimal shipment plan:")
print(allocation.astype(int))

print(
    "\nMinimum transportation cost =",
    int(transportation_cost(allocation, cost))
)

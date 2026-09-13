import numpy as np

def big_m_max(c, A, b, signs, M=100000):
    """
    Solve a maximization LPP using the Big-M simplex method.

    signs:
        "<="  -> add slack variable
        ">="  -> add surplus + artificial variable
        "="   -> add artificial variable
    """
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)
    c = np.array(c, dtype=float)

    m, n = A.shape

    T = A.copy()
    names = [f"x{i+1}" for i in range(n)]
    objective = list(c)

    basis = []
    cb = []

    for i, sign in enumerate(signs):
        if sign == "<=":
            col = np.zeros(m)
            col[i] = 1

            T = np.column_stack((T, col))
            names.append(f"s{i+1}")
            objective.append(0)

            basis.append(len(names) - 1)
            cb.append(0)

        elif sign == ">=":
            col = np.zeros(m)
            col[i] = -1

            T = np.column_stack((T, col))
            names.append(f"e{i+1}")
            objective.append(0)

            col = np.zeros(m)
            col[i] = 1

            T = np.column_stack((T, col))
            names.append(f"a{i+1}")
            objective.append(-M)

            basis.append(len(names) - 1)
            cb.append(-M)

        elif sign == "=":
            col = np.zeros(m)
            col[i] = 1

            T = np.column_stack((T, col))
            names.append(f"a{i+1}")
            objective.append(-M)

            basis.append(len(names) - 1)
            cb.append(-M)

        else:
            raise ValueError("Constraint sign must be <=, >= or =.")

    objective = np.array(objective, dtype=float)
    cb = np.array(cb, dtype=float)

    print("\n--- Big-M Simplex Iterations ---")

    for iteration in range(100):
        B = T[:, basis]
        B_inv = np.linalg.inv(B)

        xB = B_inv @ b
        Zj = cb @ B_inv @ T
        reduced_cost = objective - Zj
        current_Z = cb @ xB

        print(f"\nIteration {iteration}")
        print("Basis:", [names[i] for i in basis])
        print("Basic values:", np.round(xB, 4))
        print("Z =", round(current_Z, 4))

        entering = int(np.argmax(reduced_cost))

        if reduced_cost[entering] <= 1e-9:
            solution = np.zeros(len(names))
            solution[basis] = xB
            return names, solution, current_Z

        direction = B_inv @ T[:, entering]

        ratios = np.where(
            direction > 1e-9,
            xB / direction,
            np.inf
        )

        leaving_row = int(np.argmin(ratios))

        if not np.isfinite(ratios[leaving_row]):
            raise RuntimeError("The LPP is unbounded.")

        print("Entering variable:", names[entering])
        print("Leaving variable:", names[basis[leaving_row]])

        basis[leaving_row] = entering
        cb[leaving_row] = objective[entering]

    raise RuntimeError("Simplex exceeded the iteration limit.")


# ---------------------------------------------------------
# Problem:
# Maximize Z = 66x1 + 25x2 + 38x3
#
# Subject to:
# 2x1 + x2 + 3x3 <= 64
# x1 + 2x2 + 2x3 >= 50
# 3x1 + 2x2 + x3  = 58
# x1, x2, x3 >= 0
# ---------------------------------------------------------

c = [66, 25, 38]

A = [
    [2, 1, 3],
    [1, 2, 2],
    [3, 2, 1]
]

b = [64, 50, 58]
signs = ["<=", ">=", "="]

names, solution, Z = big_m_max(c, A, b, signs)

print("\n--- Final Big-M Solution ---")
for i in range(3):
    print(f"x{i+1} = {solution[i]:.0f}")

print(f"Maximum profit Z = {Z:.0f}")

print("\nConstraint check:")
print("2x1 + x2 + 3x3 =", 2*solution[0] + solution[1] + 3*solution[2])
print("x1 + 2x2 + 2x3 =", solution[0] + 2*solution[1] + 2*solution[2])
print("3x1 + 2x2 + x3  =", 3*solution[0] + 2*solution[1] + solution[2])

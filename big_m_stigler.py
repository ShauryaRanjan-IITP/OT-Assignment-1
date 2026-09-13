import numpy as np


def big_m_max(c, A, b, M=100000):
    # Big-M is usually written for a maximization problem.
    # For the diet problem the original objective is minimization,
    # so I send the negative of the cost coefficients.
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)
    c = np.array(c, dtype=float)

    m, n = A.shape

    table = A.copy()
    names = [f"x{i + 1}" for i in range(n)]
    obj = list(c)

    basis = []
    cb = []

    # All the diet constraints are >= constraints.
    # Therefore each one needs a surplus variable and an artificial variable.
    for i in range(m):
        surplus = np.zeros(m)
        surplus[i] = -1
        table = np.column_stack((table, surplus))
        names.append(f"e{i + 1}")
        obj.append(0)

        artificial = np.zeros(m)
        artificial[i] = 1
        table = np.column_stack((table, artificial))
        names.append(f"a{i + 1}")
        obj.append(-M)

        basis.append(len(names) - 1)
        cb.append(-M)

    obj = np.array(obj, dtype=float)
    cb = np.array(cb, dtype=float)

    for iteration in range(100):
        B = table[:, basis]
        B_inv = np.linalg.inv(B)

        xB = B_inv @ b
        Zj = cb @ B_inv @ table
        Cj_Zj = obj - Zj

        entering = int(np.argmax(Cj_Zj))

        print(f"\nIteration {iteration}")
        print("Basis:", [names[i] for i in basis])
        print("Basic values:", np.round(xB, 6))

        # No positive reduced cost means the current BFS is optimal.
        if Cj_Zj[entering] <= 1e-9:
            solution = np.zeros(len(names))
            solution[basis] = xB
            Z = cb @ xB
            return names, solution, Z

        direction = B_inv @ table[:, entering]

        ratios = np.full(m, np.inf)
        for i in range(m):
            if direction[i] > 1e-9:
                ratios[i] = xB[i] / direction[i]

        leaving_row = int(np.argmin(ratios))

        if np.isinf(ratios[leaving_row]):
            raise ValueError("The problem is unbounded.")

        print("Entering:", names[entering])
        print("Leaving:", names[basis[leaving_row]])

        basis[leaving_row] = entering
        cb[leaving_row] = obj[entering]

    raise ValueError("Too many simplex iterations.")


# ----------------------------------------------------------
# STIGLER DIET PROBLEM
#
# The Stigler diet problem is a classical linear-programming
# problem. The aim is to satisfy nine daily nutrient requirements
# at minimum cost.
#
# The reduced data set below uses nine foods and the standard
# nutrient values per dollar of food expenditure.
# ----------------------------------------------------------

food_names = [
    "Wheat Flour",
    "Evaporated Milk",
    "Cheddar Cheese",
    "Beef Liver",
    "Cabbage",
    "Spinach",
    "Sweet Potatoes",
    "Lima Beans",
    "Navy Beans"
]

# Rows are foods.
# Columns are: calories, protein, calcium, iron, vitamin A,
# vitamin B1, vitamin B2, niacin, vitamin C.
A = np.array([
    [44.7, 1411, 2.0, 365, 0, 55.4, 33.3, 441, 0],
    [8.4, 422, 15.1, 9, 26, 3.0, 23.5, 11, 60],
    [7.4, 448, 16.4, 19, 28.1, 0.8, 10.3, 4, 0],
    [2.2, 333, 0.2, 139, 169.2, 6.4, 50.8, 316, 525],
    [2.6, 125, 4.0, 36, 7.2, 9.0, 4.5, 26, 5369],
    [1.1, 106, 0.0, 138, 918.4, 5.7, 13.8, 33, 2755],
    [9.6, 138, 2.7, 54, 290.7, 8.4, 5.4, 83, 1912],
    [17.4, 1055, 3.7, 459, 5.1, 26.9, 38.2, 93, 0],
    [26.9, 1691, 11.4, 792, 0, 38.4, 24.6, 217, 0]
], dtype=float).T

# Daily minimum requirements.
b = [3, 70, 0.8, 12, 5, 1.8, 2.7, 18, 75]

# Original problem: minimize total food expenditure.
# Big-M routine below is written for maximization, so we maximize
# the negative of the cost.
c = [-1] * len(food_names)

names, solution, Z = big_m_max(c, A, b)

daily_cost = -Z
annual_cost = 365 * daily_cost

print("\n---------------- FINAL ANSWER ----------------")

print("\nFood expenditure per day:")
for i in range(len(food_names)):
    if solution[i] > 1e-8:
        print(f"{food_names[i]:20s}: ${solution[i]:.8f}")

print(f"\nMinimum daily cost  = ${daily_cost:.8f}")
print(f"Minimum annual cost = ${annual_cost:.4f}")

nutrients = [
    "Calories (1000 kcal)",
    "Protein (g)",
    "Calcium (g)",
    "Iron (mg)",
    "Vitamin A (1000 IU)",
    "Vitamin B1 (mg)",
    "Vitamin B2 (mg)",
    "Niacin (mg)",
    "Vitamin C (mg)"
]

actual = A @ solution[:len(food_names)]

print("\nNutrient check:")
for i in range(len(nutrients)):
    print(
        f"{nutrients[i]:22s}: "
        f"{actual[i]:.4f}  (minimum = {b[i]})"
    )

# Artificial variables should be zero in the final feasible solution.
artificial_values = []
for i in range(len(food_names)):
    artificial_values.append(
        solution[len(food_names) + 2 * i + 1]
    )

print(
    "\nMaximum artificial-variable value:",
    max(abs(x) for x in artificial_values)
)

"""Independent LP verification for the two assignment models."""

import numpy as np
from scipy.optimize import linprog


def verify_stigler():
    # Same reduced 9-food data used by the Big-M program, solved independently.
    A = np.array([
        [44.7, 1411, 2.0, 365, 0, 55.4, 33.3, 441, 0],
        [8.4, 422, 15.1, 9, 26, 3.0, 23.5, 11, 60],
        [7.4, 448, 16.4, 19, 28.1, 0.8, 10.3, 4, 0],
        [2.2, 333, 0.2, 139, 169.2, 6.4, 50.8, 316, 525],
        [2.6, 125, 4.0, 36, 7.2, 9.0, 4.5, 26, 5369],
        [1.1, 106, 0.0, 138, 918.4, 5.7, 13.8, 33, 2755],
        [9.6, 138, 2.7, 54, 290.7, 8.4, 5.4, 83, 1912],
        [17.4, 1055, 3.7, 459, 5.1, 26.9, 38.2, 93, 0],
        [26.9, 1691, 11.4, 792, 0, 38.4, 24.6, 217, 0],
    ]).T
    b = np.array([3, 70, 0.8, 12, 5, 1.8, 2.7, 18, 75], dtype=float)

    result = linprog(
        c=np.ones(9),
        A_ub=-A,
        b_ub=-b,
        bounds=[(0, None)] * 9,
        method="highs",
    )
    if not result.success:
        raise RuntimeError(result.message)
    return float(result.fun), result.x


def verify_transportation():
    cost = np.array([
        [14, 11, 6, 14],
        [14, 8, 6, 4],
        [14, 1, 4, 7],
    ], dtype=float)
    supply = np.array([40, 30, 50], dtype=float)
    demand = np.array([25, 30, 20, 45], dtype=float)

    c = cost.ravel()
    A_eq = []
    b_eq = []

    for i in range(3):
        row = np.zeros(12)
        row[i * 4:(i + 1) * 4] = 1
        A_eq.append(row)
        b_eq.append(supply[i])

    for j in range(4):
        row = np.zeros(12)
        row[j::4] = 1
        A_eq.append(row)
        b_eq.append(demand[j])

    result = linprog(
        c=c,
        A_eq=np.array(A_eq),
        b_eq=np.array(b_eq),
        bounds=[(0, None)] * 12,
        method="highs",
    )
    if not result.success:
        raise RuntimeError(result.message)
    return float(result.fun), result.x.reshape(3, 4)


def main():
    diet_cost, diet_x = verify_stigler()
    trans_cost, trans_x = verify_transportation()

    print("Independent verification using SciPy linprog")
    print("=" * 52)
    print(f"Stigler minimum daily cost : ${diet_cost:.8f}")
    print("Positive food variables    :")
    names = [
        "Wheat Flour", "Evaporated Milk", "Cheddar Cheese",
        "Beef Liver", "Cabbage", "Spinach", "Sweet Potatoes",
        "Lima Beans", "Navy Beans"
    ]
    for name, value in zip(names, diet_x):
        if value > 1e-8:
            print(f"  {name:20s} ${value:.8f}")

    print(f"\nTransportation minimum cost: {trans_cost:.0f}")
    print("Optimal shipment plan:")
    print(np.rint(trans_x).astype(int))

    # Expected values from the custom implementations.
    assert abs(diet_cost - 0.10866228) < 1e-6
    assert abs(trans_cost - 715.0) < 1e-9
    print("\nVerification status: PASS")


if __name__ == "__main__":
    main()

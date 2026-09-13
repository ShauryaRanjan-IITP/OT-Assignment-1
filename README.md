# Operations Research — Assignment 1

This repository contains the Python implementations for Assignment 1.

## 1. Big-M Method

**File:** `big_m_assignment.py`

The program solves a constrained linear programming maximization problem using the **Big-M Simplex Method**.

### Model

Maximize

`Z = 66x1 + 25x2 + 38x3`

Subject to:

- `2x1 + x2 + 3x3 <= 64`
- `x1 + 2x2 + 2x3 >= 50`
- `3x1 + 2x2 + x3 = 58`
- `x1, x2, x3 >= 0`

The program prints the simplex iterations, entering/leaving variables, final decision variables, objective value, and constraint checks.

**Optimal solution:** `x1 = 10, x2 = 8, x3 = 12`

**Maximum profit:** `1316`

## 2. Transportation Problem — VAM + MODI

**File:** `transportation_vam_modi.py`

The transportation problem has four sources and five destinations. The program first constructs an initial basic feasible solution using **Vogel's Approximation Method (VAM)** and then applies the **MODI (u-v) method** to test optimality and improve the allocation when necessary.

### Supply

`S1=40, S2=30, S3=50, S4=20`

### Demand

`D1=20, D2=30, D3=25, D4=35, D5=30`

### Unit transportation costs

|     | D1 | D2 | D3 | D4 | D5 |
|-----|---:|---:|---:|---:|---:|
| S1  | 6 | 8 | 10 | 9 | 7 |
| S2  | 9 | 11 | 8 | 7 | 12 |
| S3  | 10 | 7 | 12 | 8 | 9 |
| S4  | 8 | 9 | 6 | 10 | 11 |

The program prints the VAM initial allocation, MODI potentials/reduced costs, improvement iterations when required, and the final shipment plan.

**Final transportation cost:** `975`

## Requirements

- Python 3
- NumPy

Install NumPy with:

```bash
pip install numpy
```

## Running

```bash
python big_m_assignment.py
python transportation_vam_modi.py
```

The assignment report/PDF should contain the problem formulation, relevant algorithm steps, source code, and corresponding program output as required by the course instructions.

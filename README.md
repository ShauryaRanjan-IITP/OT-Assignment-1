# Operations Research – Assignment 1

This repository contains the two Python programs prepared for Operations Research Assignment 1.

## 1. Big-M Method — Stigler Diet Problem

The first case study is the **Stigler Diet Problem**, a classical linear-programming problem first formulated by George Stigler. The objective is to choose a minimum-cost combination of foods that satisfies the required daily amounts of nine nutrients.

This version uses the standard reduced 9-food data set:

- Wheat Flour
- Evaporated Milk
- Cheddar Cheese
- Beef Liver
- Cabbage
- Spinach
- Sweet Potatoes
- Lima Beans
- Navy Beans

All nine nutrient requirements are `>=` constraints. Therefore the standard-form model contains a **surplus variable and an artificial variable for every constraint**. The program solves the model using the **Big-M Simplex Method**.

### Main result

Minimum daily cost:

`$0.10866228`

Minimum annual cost:

`$39.6617`

The non-zero food expenditure variables are:

| Food | Daily expenditure |
|---|---:|
| Wheat Flour | 0.02951906 |
| Beef Liver | 0.00189256 |
| Cabbage | 0.01121444 |
| Spinach | 0.00500766 |
| Navy Beans | 0.06102856 |

The final artificial variables are zero and all nine nutrient requirements are satisfied.

## 2. Transportation Problem — VAM + MODI

The second case study is the **classical Hitchcock transportation model**: a balanced minimum-cost transportation problem in which supply points have to send a common product to demand points.

### Supply

| Source | Supply |
|---|---:|
| S1 | 40 |
| S2 | 30 |
| S3 | 50 |

### Demand

| Destination | Demand |
|---|---:|
| D1 | 25 |
| D2 | 30 |
| D3 | 20 |
| D4 | 45 |

Total supply = total demand = `120`.

### Unit transportation cost

| Source / Destination | D1 | D2 | D3 | D4 |
|---|---:|---:|---:|---:|
| S1 | 14 | 11 | 6 | 14 |
| S2 | 14 | 8 | 6 | 4 |
| S3 | 14 | 1 | 4 | 7 |

The program first finds an initial basic feasible solution using **Vogel's Approximation Method (VAM)**. The resulting solution is then tested using the **MODI (u-v) method**. Negative reduced costs are used to select an entering cell, a closed loop is constructed, and the allocation is improved until every reduced cost is non-negative.

### Main result

Initial VAM transportation cost:

`725`

Final optimal transportation cost:

`715`

Final shipment plan:

```text
[[25,  0, 15,  0],
 [ 0,  0,  0, 30],
 [ 0, 30,  5, 15]]
```

## Files

- `big_m_stigler.py` — Big-M implementation for the Stigler Diet Problem
- `transportation_vam_modi.py` — VAM + MODI implementation for the transportation problem

## Requirements

Python 3 and NumPy.

Install NumPy:

```bash
pip install numpy
```

Run the programs:

```bash
python big_m_stigler.py
python transportation_vam_modi.py
```

The assignment PDF should contain the problem statement, mathematical formulation, standard-form conversion, relevant method calculations, source code, and the corresponding program output.

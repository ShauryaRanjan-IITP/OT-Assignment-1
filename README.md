# Operations Research – Assignment 1

This repository contains the Python implementations and computational checks for **Operations Research Assignment 1**.

The assignment covers two standard Operations Research models:

1. **Big-M Simplex Method** applied to the reduced 9-food **Stigler Diet Problem**.
2. **Vogel's Approximation Method (VAM)** followed by **MODI** for a balanced transportation problem.

The main algorithms are implemented directly with NumPy rather than through a ready-made optimization model. Additional scripts are included only for **independent verification, regression testing, visualization, and reproducible notebook-based execution**.

---

## 1. Big-M Method — Stigler Diet Problem

The Stigler Diet Problem is a classical linear-programming problem in which the objective is to satisfy minimum daily nutrient requirements at minimum food expenditure.

This repository uses the reduced 9-food data set used in the assignment:

- Wheat Flour
- Evaporated Milk
- Cheddar Cheese
- Beef Liver
- Cabbage
- Spinach
- Sweet Potatoes
- Lima Beans
- Navy Beans

All nine constraints are `>=` constraints, so the standard-form model introduces a **surplus variable and an artificial variable for each constraint**. The custom implementation uses the **Big-M Simplex Method** and explicitly works with the current basis and reduced costs.

### Result

- Minimum daily cost: **$0.10866228**
- Minimum annual cost: **$39.6617**
- Maximum artificial-variable value: **0.0**

Positive food expenditures:

| Food | Daily expenditure |
|---|---:|
| Wheat Flour | 0.02951906 |
| Beef Liver | 0.00189256 |
| Cabbage | 0.01121444 |
| Spinach | 0.00500766 |
| Navy Beans | 0.06102856 |

---

## 2. Transportation Problem — VAM + MODI

The transportation case is a balanced Hitchcock-type model with three sources and four destinations.

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

Total supply = total demand = **120**.

### Unit transportation cost

| Source / Destination | D1 | D2 | D3 | D4 |
|---|---:|---:|---:|---:|
| S1 | 14 | 11 | 6 | 14 |
| S2 | 14 | 8 | 6 | 4 |
| S3 | 14 | 1 | 4 | 7 |

VAM constructs the initial basic feasible solution. MODI then calculates the potentials and reduced costs, finds an improving entering cell, forms the adjustment cycle, and continues until all reduced costs are non-negative.

### Result

- Initial VAM cost: **725**
- Final MODI cost: **715**
- Improvement: **10 cost units**

Final shipment plan:

```text
[[25,  0, 15,  0],
 [ 0,  0,  0, 30],
 [ 0, 30,  5, 15]]
```

---

## 3. Independent Verification

`verify_results.py` formulates both models independently using **SciPy `linprog`**. It is not used by the Big-M or VAM-MODI algorithms themselves; it is included as a separate numerical check.

The independent LP solve returns:

| Model | Custom implementation | Independent LP check |
|---|---:|---:|
| Stigler Diet | $0.10866228/day | $0.10866228/day |
| Transportation | 715 | 715 |

The verification script also checks the final transportation shipment matrix and the positive Stigler food variables.

---

## 4. Regression Tests

`test_cases.py` runs both assignment programs as complete Python processes and checks the key reported results:

- Big-M daily cost
- Big-M annual cost
- zero artificial-variable value
- VAM initial cost
- MODI final cost

A successful run prints:

```text
Big-M implementation : PASS
VAM + MODI           : PASS
All regression tests : PASS
```

---

## 5. Visualizations

`visualize_results.py` creates two figures using Matplotlib:

- `outputs/stigler_diet.svg` — optimal daily food expenditure
- `outputs/transportation_plan.svg` — final shipment plan after MODI

PNG versions are also produced locally when the script is run.

Run the visualization script locally to generate the figures in `outputs/`:

```bash
python visualize_results.py
```

The generated figures are intentionally kept out of version control so the repository stays focused on the source code and reproducible analysis.

---

## 6. Jupyter Notebook Demonstration

`OR_Assignment_1_Demo.ipynb` provides a single reproducible workflow for the project. It runs the existing Big-M and VAM-MODI programs, performs the independent SciPy verification, runs the regression tests, and generates/displays the Matplotlib figures.

The notebook calls the existing Python programs rather than copying their algorithms, so the main implementations remain the single source of truth.

### Run the notebook

After installing the requirements, start Jupyter with:

```bash
jupyter notebook OR_Assignment_1_Demo.ipynb
```

The notebook can also be opened in JupyterLab or another compatible Jupyter environment. Its execution cells contain checked textual results, and the visualization cells regenerate the figures from the repository scripts when the notebook is run.

---

## 7. Files

| File | Purpose |
|---|---|
| `big_m_stigler.py` | Direct Big-M Simplex implementation for the Stigler Diet Problem |
| `transportation_vam_modi_final.py` | VAM initial solution and MODI improvement/optimality check |
| `verify_results.py` | Independent LP verification using SciPy |
| `test_cases.py` | Regression tests for the two main programs |
| `visualize_results.py` | Matplotlib result visualizations |
| `OR_Assignment_1_Demo.ipynb` | Reproducible Jupyter workflow combining execution, verification, testing, and visualization |
| `requirements.txt` | Python package requirements |
| `outputs/` | Local generated figures (created by `visualize_results.py`) |

---

## 8. Requirements

Python 3.10+ is recommended.

Install the required packages:

```bash
pip install -r requirements.txt
```

This installs NumPy for numerical operations, SciPy for independent LP verification, Matplotlib for figures, and Jupyter Notebook for the reproducible notebook workflow.

---

## 9. Running the Project

Run the two assignment implementations:

```bash
python big_m_stigler.py
python transportation_vam_modi_final.py
```

Run the independent verification:

```bash
python verify_results.py
```

Run the regression tests:

```bash
python test_cases.py
```

Create the visualizations:

```bash
python visualize_results.py
```

Or run the complete demonstration through:

```bash
jupyter notebook OR_Assignment_1_Demo.ipynb
```

The algorithms remain independent of SciPy; SciPy is used only for the additional verification step.

"""Create simple result figures for the assignment repository."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).resolve().parent / "outputs"
OUT.mkdir(exist_ok=True)


def stigler_plot():
    names = ["Wheat Flour", "Beef Liver", "Cabbage", "Spinach", "Navy Beans"]
    values = np.array([0.02951906, 0.00189256, 0.01121444, 0.00500766, 0.06102856])

    fig, ax = plt.subplots(figsize=(8, 4.6))
    bars = ax.bar(names, values)
    ax.set_title("Optimal Daily Food Expenditure — Stigler Diet")
    ax.set_ylabel("Dollars per day")
    ax.tick_params(axis="x", rotation=20)
    ax.grid(axis="y", alpha=0.25)
    for bar, value in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width() / 2, value, f"{value:.5f}",
                ha="center", va="bottom", fontsize=9)
    fig.tight_layout()
    fig.savefig(OUT / "stigler_diet.png", dpi=180)
    fig.savefig(OUT / "stigler_diet.svg")
    plt.close(fig)


def transportation_plot():
    allocation = np.array([
        [25, 0, 15, 0],
        [0, 0, 0, 30],
        [0, 30, 5, 15],
    ])

    fig, ax = plt.subplots(figsize=(6.5, 4.4))
    image = ax.imshow(allocation, aspect="auto")
    ax.set_xticks(range(4), ["D1", "D2", "D3", "D4"])
    ax.set_yticks(range(3), ["S1", "S2", "S3"])
    ax.set_xlabel("Destination")
    ax.set_ylabel("Source")
    ax.set_title("Optimal Transportation Plan after MODI")
    for i in range(3):
        for j in range(4):
            ax.text(j, i, str(allocation[i, j]), ha="center", va="center")
    fig.colorbar(image, ax=ax, label="Units shipped")
    fig.tight_layout()
    fig.savefig(OUT / "transportation_plan.png", dpi=180)
    fig.savefig(OUT / "transportation_plan.svg")
    plt.close(fig)


def main():
    stigler_plot()
    transportation_plot()
    print("Created:")
    print("  outputs/stigler_diet.png")
    print("  outputs/stigler_diet.svg")
    print("  outputs/transportation_plan.png")
    print("  outputs/transportation_plan.svg")


if __name__ == "__main__":
    main()

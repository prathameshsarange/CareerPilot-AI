import os

import matplotlib.pyplot as plt
import pandas as pd


def generate_histogram(csv_path):

    try:

        df = pd.read_csv(csv_path)

    except Exception:

        return None

    numeric = df.select_dtypes(include="number")

    if numeric.empty:

        return None

    column = numeric.columns[0]

    os.makedirs("data", exist_ok=True)

    chart_path = os.path.join(
        "data",
        "chart.png"
    )

    plt.figure(figsize=(10, 5))

    plt.hist(
        df[column].dropna(),
        bins=20,
        edgecolor="black"
    )

    plt.title(f"Distribution of {column}")

    plt.xlabel(column)

    plt.ylabel("Frequency")

    plt.grid(alpha=0.3)

    plt.tight_layout()

    plt.savefig(chart_path)

    plt.close()

    return chart_path
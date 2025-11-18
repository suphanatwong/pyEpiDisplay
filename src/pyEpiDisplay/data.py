import os
import pandas as pd

def data(name: str = None):
    base_dir = os.path.join(os.path.dirname(__file__), "datasets")

    if name is None:
        # List all CSV files
        files = [f.replace(".csv", "") for f in os.listdir(base_dir) if f.endswith(".csv")]
        files
        #print("Available datasets:", ", ".join(files))
        return files

    # Load dataset
    file = f"{name}.csv"
    path = os.path.join(base_dir, file)

    if not os.path.exists(path):
        raise FileNotFoundError(
            f"Dataset '{name}' not found in: {base_dir}. "
            f"Available datasets: {', '.join(os.listdir(base_dir))}"
        )

    return pd.read_csv(path)

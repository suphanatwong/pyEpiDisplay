import pytest
import subprocess
import pandas as pd
from pyepidisplay.data import data
from pyepidisplay.tabpct import tabpct

# Load the Outbreak dataset
df = data("Outbreak")

# Print columns for reference (optional)
print("Columns in dataset:", df.columns)

# ============================================
# Basic smoke test
# ============================================
def test_smoke():
    """Smoke test: tabpct runs without error and returns dict"""
    # Use valid columns
    result = tabpct(df["sex"], df["beefcurry"], graph=False)
    assert isinstance(result, dict)
    assert "table_row_percent" in result
    assert "table_column_percent" in result

# ============================================
# One-shot test: return is not None
# ============================================
def test_not_none():
    result = tabpct(df["sex"], df["beefcurry"], graph=False)
    assert result is not None

# ============================================
# Helper function to run R tabpct for comparison
# ============================================
def run_r_tabpct(row_name="sex", col_name="beefcurry"):
    """
    Run R tabpct using epiDisplay::tabpct on the Outbreak dataset.
    row_name, col_name: strings for column names in R dataset
    """
    r_code = f"""
    suppressMessages(library(epiDisplay))
    data(Outbreak)
    df <- Outbreak
    print(tabpct(df${row_name}, df${col_name}))
    """
    result = subprocess.run(
        ["Rscript", "-e", r_code],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        raise RuntimeError(f"R error: {result.stderr}")
    return result.stdout


def compare_py_r_tabpct(df):
    print("\n============ PYTHON COMMAND ============\n")
    print("tabpct")

    # Python output
    py_output = tabpct(df["sex"], df["beefcurry"], graph=False)

    # print("\n============ Python RESULT ============\n")
    print(py_output)

    #R output
    r_output = run_r_tabpct()

    print("\n============ R RESULT ============\n")
    print(r_output)

    # Strip spaces + newlines for comparison
    py_clean = str(py_output).replace(" ", "").replace("\n", "")
    r_clean = r_output.replace(" ", "").replace("\n", "")

    match = (py_clean == r_clean)

    print(f"\nMATCH: {match}\n")
    return match

# ============================================
# Helper function to run R tabpct for comparison
# ============================================
def run_r_tabpct(row_name="sex", col_name="beefcurry"):
    """
    Run R tabpct using epiDisplay::tabpct on the Outbreak dataset.
    row_name, col_name: strings for column names in R dataset
    """
    r_code = f"""
    suppressMessages(library(epiDisplay))
    data(Outbreak)
    df <- Outbreak
    print(tabpct(df${row_name}, df${col_name}))
    """
    result = subprocess.run(
        ["Rscript", "-e", r_code],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        raise RuntimeError(f"R error: {result.stderr}")
    return result.stdout


def run_r_tabpct_graph(row_name="sex", col_name="beefcurry"):
    """
    Run R tabpct using epiDisplay::tabpct on the Outbreak dataset.
    row_name, col_name: strings for column names in R dataset
    """
    r_code = f"""
    suppressMessages(library(epiDisplay))
    data(Outbreak)
    df <- Outbreak
    print(tabpct(df${row_name}, df${col_name}, graph=TRUE))
    """
    result = subprocess.run(
        ["Rscript", "-e", r_code],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        raise RuntimeError(f"R error: {result.stderr}")
    return result.stdout

def compare_py_r_tabpct_graph(df):
    print("\n============ PYTHON COMMAND ============\n")
    print("tabpct")

    # Python output
    py_output = tabpct(df["sex"], df["beefcurry"], graph=True)

    # print("\n============ Python RESULT ============\n")
    print(py_output)

    #R output
    r_output = run_r_tabpct_graph()

    print("\n============ R RESULT ============\n")
    print(r_output)

    # Strip spaces + newlines for comparison
    py_clean = str(py_output).replace(" ", "").replace("\n", "")
    r_clean = r_output.replace(" ", "").replace("\n", "")

    match = (py_clean == r_clean)

    print(f"\nMATCH: {match}\n")
    return match

# ============================================
# Helper function to run R tabpct for comparison
# ============================================
def run_r_tabpct(row_name="sex", col_name="beefcurry"):
    """
    Run R tabpct using epiDisplay::tabpct on the Outbreak dataset.
    row_name, col_name: strings for column names in R dataset
    """
    r_code = f"""
    suppressMessages(library(epiDisplay))
    data(Outbreak)
    df <- Outbreak
    print(tabpct(df${row_name}, df${col_name}))
    """
    result = subprocess.run(
        ["Rscript", "-e", r_code],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        raise RuntimeError(f"R error: {result.stderr}")
    return result.stdout


def run_r_tabpct_graph_col(row_name="sex", col_name="beefcurry"):
    """
    Run R tabpct using epiDisplay::tabpct on the Outbreak dataset.
    row_name, col_name: strings for column names in R dataset
    """
    r_code = f"""
    suppressMessages(library(epiDisplay))
    data(Outbreak)
    df <- Outbreak
    print(tabpct(df${row_name}, df${col_name}, percent = 'row', graph=TRUE))
    """
    result = subprocess.run(
        ["Rscript", "-e", r_code],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        raise RuntimeError(f"R error: {result.stderr}")
    return result.stdout

def compare_py_r_tabpct_graph_col(df):
    print("\n============ PYTHON COMMAND ============\n")
    print("tabpct")

    # Python output
    py_output = tabpct(df["sex"], df["beefcurry"], graph=True, percent="row")

    # print("\n============ Python RESULT ============\n")
    print(py_output)

    #R output
    r_output = run_r_tabpct_graph_col()

    print("\n============ R RESULT ============\n")
    print(r_output)

    # Strip spaces + newlines for comparison
    py_clean = str(py_output).replace(" ", "").replace("\n", "")
    r_clean = r_output.replace(" ", "").replace("\n", "")

    match = (py_clean == r_clean)

    print(f"\nMATCH: {match}\n")
    return match
tabpct(df["sex"], df["beefcurry"], graph=True, percent="col")

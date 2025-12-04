import pytest
from pyepidisplay.data import data

from pyepidisplay.des import des
import subprocess
df = data("Outbreak")

# print(des(df))
def smoke_test():
    result = des(df)  
    return result

def one_shot_test():
    result = des(df)
    assert result is not None

# ============================================
# 1) Call R's epiDisplay::des()
# ============================================

def run_r_des():
    r_code = """
    suppressMessages(library(epiDisplay))
    data(Outbreak)
    df <- Outbreak
    print(des(df))
    """

    print("\n============ R COMMAND ============\n")
    print(r_code)

    result = subprocess.run(
        ["Rscript", "-e", r_code],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        raise RuntimeError(f"R error: {result.stderr}")

    return result.stdout

def compare_py_r_des(df):
    print("\n============ PYTHON COMMAND ============\n")
    print("des(df)")

    # Python output
    py_output = des(df)

    print("\n============ Python RESULT ============\n")
    print(py_output)

    # R output
    r_output = run_r_des()

    print("\n============ R RESULT ============\n")
    print(r_output)

    # Strip spaces + newlines for comparison
    py_clean = str(py_output).replace(" ", "").replace("\n", "")
    r_clean = r_output.replace(" ", "").replace("\n", "")

    match = (py_clean == r_clean)

    print(f"\nMATCH: {match}\n")
    return match
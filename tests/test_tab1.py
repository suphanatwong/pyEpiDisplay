import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pytest
from pyepidisplay.data import data

from pyepidisplay.tab1 import tab1
#outbreak = pd.read_csv("/Users/Joey/Downloads/FallQuarter/CSE583/pyEpiDisplay/src/pyepidisplay/datasets/Outbreak.csv")
outbreak = data("Outbreak")

def test_smoke():
    """
    author: Jiayi
    reviewer: Marthin
    category: smoke test
    """
    tab1("age", outbreak)
    return

def check_output_type():
    """
    author: Jiayi
    reviewer: Marthin
    category: one-shot test
    """
    type(tab1("age", outbreak)) 
    return

def check_column_number():
    """
    author: Jiayi
    reviewer: Marthin
    category: one-shot test
    """
    tab1("age", outbreak).shape[1] 
    return

def check_final_cumulative_percent():
    """
    author: Jiayi
    reviewer: Marthin
    category: one-shot test
    """
    # check the the last value in column "Cumulative Percent" should be close to 100
    np.testing.assert_almost_equal(tab1("age", outbreak).iloc[-1]["Cumulative Percent"], 100.0, decimal=1)
    return

def valid_input_1():
    """
    author: Jiayi
    reviewer: Marthin
    category: edge test
    """
    with pytest.raises(ValueError, match ="Column name must be a string."):
        tab1(3, outbreak)
    return

def valid_input_2():
    """
    author: Jiayi
    reviewer: Marthin
    category: edge test
    """
    with pytest.raises(ValueError, match ="Input data must be a pandas DataFrame." ):
        tab1("age", outbreak)
    return

def edge_test_2():
    """
    make sure the input column exists in the dataframe
    """
    with pytest.raises(ValueError, match = "Column is not found in DataFrame."):
        tab1("ages", outbreak)
    return

def test_column_na():
    """
    make sure the input column does not contain NA values
    """
    with pytest.raises(ValueError, match = "Column contains NA values."):
        tab1("age", outbreak)
    return

def test_dataframe_validity():
    """
    make sure the input dataframe is in valid data type
    """
    with pytest.raises(ValueError, match = "Input data must be a pandas DataFrame."):
        tab1("age", outbreak)
    return


## example test
def some_smoke_test(arg1: int):
    """
    author: ianqs
    reviewer: eleftasia
    category: smoke test
    """
    return arg1 + 1

def some_pattern_test(f_name: str):
    """
    author: ianqs
    reviewer: eleftasia
    category: pattern test (not relevant)
    justification: some well thought out justification
    """
    pass

def other_smoke_test(arg1: int):
    """
    author: eleftasia
    reviewer: ianqs
    category: smoke test
    """
    return arg1 + 2  # See how it's different from the original that I had?

def some_pattern_test(f_name: str):
    """
    author: ianqs
    reviewer: eleftasia
    category: pattern test
    """
    return ...
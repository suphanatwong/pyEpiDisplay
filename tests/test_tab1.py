"""
This is docstring for test_tab1.py
"""

import numpy as np
import pytest
from pyepidisplay.data import data
from pyepidisplay.tab1 import tab1

outbreak = data("Outbreak")

def test_smoke():
    """
    author: Jiayi
    reviewer: Marthin
    category: smoke test
    """
    tab1("age", outbreak)

def check_output_type():
    """
    author: Jiayi
    reviewer: Marthin
    category: one-shot test
    """
    type(tab1("age", outbreak))

def check_column_number():
    """
    author: Jiayi
    reviewer: Marthin
    category: one-shot test
    """
    print(tab1("age", outbreak).shape[1])

def valid_input_1():
    """
    author: Jiayi
    reviewer: Marthin
    category: edge test
    """
    with pytest.raises(ValueError, match ="Column name must be a string."):
        tab1(3, outbreak)

def valid_input_2():
    """
    author: Jiayi
    reviewer: Marthin
    category: edge test
    """
    with pytest.raises(ValueError, match ="Input data must be a pandas DataFrame." ):
        tab1("age", outbreak)

def column_exists():
    """
    author: Jiayi
    reviewer: Marthin
    category: edge test
    """
    with pytest.raises(ValueError, match = "Column is not found in DataFrame."):
        tab1("region", outbreak)

def check_null_value():
    """
    author: Jiayi
    reviewer: Marthin
    category: edge test
    """
    with pytest.raises(ValueError, match = "Column contains NA values."):
        tab1("onset", outbreak)

def test_column_na():
    """
    make sure the input column does not contain NA values
    """
    with pytest.raises(ValueError, match = "Column contains NA values."):
        tab1("onset", outbreak)

def test_tab1_pattern():
    """
    author: Jiayi
    reviewer: Marthin
    category: pattern test
    """
    result = tab1("age", outbreak)

    # Cumulative Percent must end at ~100 ----
    x = tab1("age", outbreak).iloc[-1]["Cumulative Percent"]
    np.testing.assert_almost_equal(x, 100.0, decimal=1)

    # Cumulative Percent must be non-decreasing ----
    assert result["Cumulative Percent"].is_monotonic_increasing

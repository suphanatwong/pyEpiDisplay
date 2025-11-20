"""
Tests for the entropy function
"""
# tableStack_test.py
import pandas as pd
import numpy as np
from pyEpiDisplay.tableStack import tableStack
from pyEpiDisplay.data import data
from pyEpiDisplay.datasets import DATA_PATH

# Create sample data instead of loading from data()
def test_tableStack():
    df = pd.read_csv(DATA_PATH + '/Outbreak.csv')
    result = tableStack(
        df,
        vars=['age', 'sex', 'nausea'],
        by='sex',
        test=True
    )
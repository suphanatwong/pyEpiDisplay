# tableStack_test.py
import pandas as pd
import numpy as np
from tableStack import tableStack
from pyEpiDisplay.data import data

# Create sample data instead of loading from data()
#df = data('Outbreak')
df = pd.read_csv('/Users/suphanatwongsanuphat/Documents/UW/2025/Fall 2025/CSE 883 Software Dev for DS/pyEpiDisplay/Outbreak.csv')
result = tableStack(
    df,
    vars=['age', 'sex', 'nausea'],
    by='sex',
    test=True
)
print(result)
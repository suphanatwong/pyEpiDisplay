"""
Example of tab1() using the Outbreak dataset.

author: Jiayi Ding
reviewer: Marthin Mandig
category: example
"""

from pyepidisplay.data import data
from pyepidisplay.tab1 import tab1

# Example of tab1() using the Outbreak dataset from pyepidisplay.data,
# and the column "age" of the table.
# There are 2 inputs for tab1():
# 1. column name (string): the name of the column to be summarized.
# 2. data (pandas DataFrame): the dataset containing the column.

df=data("Outbreak") # change it to your own DataFrame if needed
print(tab1("age", df)) # change "age" to your own column name if needed

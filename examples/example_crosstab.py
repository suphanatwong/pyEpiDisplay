"""
Example of logistic_display() using the Outbreak dataset.

author: marthin mandig
reviewer: Jiayi Ding
category: example
"""

from pyepidisplay.crosstab_function import my_crosstab
from pyepidisplay.data import data

#load dataset
df=data("Outbreak")

my_crosstab(df['nausea'], df['sex'])
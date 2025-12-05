"""
Example of logistic_display() using the Outbreak dataset.

author: marthin mandig
reviewer: Jiayi Ding
category: example
"""

from pyepidisplay.summ_function import summ
from pyepidisplay.data import data

#load dataset
df=data("Outbreak")

subset = df[
    (df['sex'] == 1) &
    (df['age'] >= 13) &
    (df['age'] != 99) &
    (df['nausea'] == 1)
]
print(summ(subset['age']))
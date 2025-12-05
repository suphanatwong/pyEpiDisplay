"""
Example of logistic_display() using the Outbreak dataset.

author: scatherinekim
reviewer: suphanatwong
category: example
"""

from pyepidisplay.logistic_display import logistic_display
from pyepidisplay.data import data

#load dataset
df=data("Outbreak")

df_results = logistic_display('nausea ~ beefcurry + saltegg', df)
print(df_results)

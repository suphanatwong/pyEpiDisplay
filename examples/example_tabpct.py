"""
Example of tabpct() using the Outbreak dataset.

author: suphanatwong
reviewer: anna
category: example
"""

from pyepidisplay.data import data
from pyepidisplay.tabpct import tabpct

#load dataset
df = data("Outbreak")

#run tabpct

tabpct(df["sex"])
tabpct(df["sex"], df["beefcurry"])

#run tabpct with graph
tabpct(df["sex"], df["beefcurry"], graph=True)

#run tabpct with graph and row percent
tabpct(df["sex"], df["beefcurry"], graph=True, percent="row")

#run tabpct with graph and col percent
tabpct(df["sex"], df["beefcurry"], graph=True, percent="col")
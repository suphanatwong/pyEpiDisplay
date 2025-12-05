"""
Example of data() using the Outbreak dataset.

author: suphanatwong
reviewer: anna
category: example
"""

from pyepidisplay.data import data

#load dataset
df=data("Outbreak")
print(df.head())

df=data("outbreak")
print(df.head())


df=data(Outbreak)
print(df.head())

df=data(outbreak)
print(df.head())
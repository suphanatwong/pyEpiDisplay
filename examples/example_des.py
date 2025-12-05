"""
Example of des() using the Outbreak dataset.

author: suphanatwong
reviewer: anna
category: example
"""

from pyepidisplay.data import data
from pyepidisplay.des import des

#load dataset
df = data("Outbreak")

#run des
des(df=df)
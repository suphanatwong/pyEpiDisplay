#!/usr/bin/env python
# coding: utf-8

"""
cse583_summ_function module.
Provides a summary function for pandas Series and example usage.
"""

import sys
import pyreadr
import matplotlib.pyplot as plt
import seaborn as sns

FILE_PATH = "/Users/marthinmandig/Downloads/epiDisplay/data/Outbreak.rdata"

# Read rdata file
result = pyreadr.read_r(FILE_PATH)
print(result.keys())

# Extract dataset
df = result['Outbreak']
print(df.head())

def summ(series):
    """
    Summarize a pandas Series with count, mean, median, std, min, and max.
    """
    clean_series = series.dropna()
    summary = {
        "obs": clean_series.count(),
        "mean": clean_series.mean(),
        "median": clean_series.median(),
        "s.d.": clean_series.std(),
        "min": clean_series.min(),
        "max": clean_series.max()
    }
    return summary

# Example usage
subset = df[
    (df['sex'] == 1) &
    (df['age'] >= 13) &
    (df['age'] != 99) &
    (df['nausea'] == 1)
]
print(summ(subset['age']))

sns.boxplot(x=subset['age'])
plt.title("Age Distribution of Males (13+) with Nausea")
plt.xlabel("Age (years)")
plt.show()

grouped = df[df['age'] != 99].groupby('sex')['age'].apply(summ)
print(grouped)
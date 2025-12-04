#!/usr/bin/env python
# coding: utf-8

"""
cse583_summ_function module.
Provides a summary function for pandas Series and example usage.
"""

import matplotlib.pyplot as plt
import seaborn as sns


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
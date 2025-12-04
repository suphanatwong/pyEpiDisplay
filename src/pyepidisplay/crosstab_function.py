"""
crosstab_function module.
Provides a general-purpose cross-tabulation function with counts, percentages, and chi-square test.
"""

import pandas as pd
from scipy.stats import chi2_contingency


# Read rdata file

def my_crosstab(x_var, y_var, chisq=True):
    """
    General-purpose cross-tabulation function.
    Displays counts, row percentages, column percentages,
    and optionally runs a chi-square test.
    """
    tab = pd.crosstab(x_var, y_var, dropna=False)

    print("\nCounts:")
    print(tab)

    print("\nRow Percentages (%):")
    row_pct = tab.div(tab.sum(axis=1), axis=0) * 100
    print(row_pct.round(1))

    print("\nColumn Percentages (%):")
    col_pct = tab.div(tab.sum(axis=0), axis=1) * 100
    print(col_pct.round(1))

    if chisq:
        chi2, p_value, dof, expected = chi2_contingency(tab)
        print("\nChi-square Test:")
        print(f"Chi2 = {chi2:.3f}, df = {dof}, p-value = {p_value:.4f}")
        print("\nExpected counts:")
        print(pd.DataFrame(expected, index=tab.index, columns=tab.columns).round(1))

# coding: utf-8
"""Module for calculating confidence intervals for means.

This module provides a Python implementation of R's epiDisplay ci.mean() function.
"""

import numpy as np
from scipy import stats

def ci_mean(x, ci=0.95):
    """Calculate confidence interval for a mean.

    Args:
        x: Array or list of numeric values.
        ci: Confidence level (default: 0.95).

    Returns:
        dict: Dictionary containing mean, sd, se, and CI bounds.
    """
    x = np.array(x)
    x = x[~np.isnan(x)]

    mean = np.mean(x)
    n = len(x)

    # If n < 2, we can't compute sd/se/CI (degrees of freedom would be <= 0)
    if n < 2:
        sd = np.nan
        se = np.nan
        lower = np.nan
        upper = np.nan
    else:
        sd = np.std(x, ddof=1)
        se = sd / np.sqrt(n)

        alpha = 1 - ci
        tval = stats.t.ppf(1 - alpha/2, df=n-1)

        lower = mean - tval * se
        upper = mean + tval * se

    return {
      "mean": mean,
      "sd": sd,
      "se": se,
      "ci_lower": lower,
      "ci_upper": upper
    }


# ## A pretty printer

def print_ci_mean(result):
    """Print confidence interval results in a formatted way.

    Args:
        result: Dictionary returned by ci_mean().
    """
    print(f"Mean:           {result['mean']:.3f}")
    print(f"SD:             {result['sd']:.3f}")
    print(f"SE:             {result['se']:.3f}")
    print(f"95% CI Lower:   {result['ci_lower']:.3f}")
    print(f"95% CI Upper:   {result['ci_upper']:.3f}")


# ## Test on the outbreak dataset

# import pandas as pd

# outbreak_df = pd.read_csv("outbreak.csv")
# outbreak_df.head()


# print_ci_mean(ci_mean(outbreak_df["age"]))


# ## Compare to R's output

# $mean
# [1] 23.69104
#
# $sd
# [1] 19.67349
#
# $se
# [1] 0.5948025
#
# $ci
# [1] 22.52396 24.85813
#

# Yes, it matches!


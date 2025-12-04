#!/usr/bin/env python
# coding: utf-8

# The regress.display() function in R takes in a linear regression object and outputs a table of linear model summary. When the Outbreak Investigations dataset is the dataset, this function can show how the average onset time of showing symptoms changes depending on whether a person ate beef curry or salt egg.
# 
# 
# The output provides the following data: 
# - The adj. coeff
# - The 95% CI
# - P(t-test)
# - P(F-test)
# - No. of observations

import pandas as pd
import numpy as np
import statsmodels.api as sm

def regress_display(model):
    """
    Mimics epiDisplay::regress.display in R.
    Generates a summary table for linear regression models, including
    adjusted coefficients, 95% confidence intervals, t-test p-values,
    and sequential Type I ANOVA F-test p-values.

    Parameters:
        model (statsmodels.regression.linear_model.RegressionResultsWrapper):
            A fitted statsmodels OLS model, e.g. smf.ols(...).fit().

    Returns:
        pd.DataFrame:
            A table containing variable names, adjusted coefficients
            with 95% confidence intervals, t-test p-values, and
            F-test p-values based on Type I ANOVA.
    """
    outcome = model.model.data.ynames
    print(f"Linear regression predicting {outcome}\n")

    coef = model.params
    ci = model.conf_int()
    ci.columns = ["Lower 95% CI", "Upper 95% CI"]
    p_t = model.pvalues

    # Compute sequential Type I ANOVA F-test p-values
    anova_table = sm.stats.anova_lm(model, typ=1)

    data = []
    for var in coef.index:
        if var == 'Intercept':
            continue

        # Label binary variables
        if var in model.model.data.orig_exog.columns:
            unique_vals = model.model.data.orig_exog[var].dropna().unique()
            if set(unique_vals) <= {0, 1}:
                label = f"{var}: 1 vs 0"
            else:
                label = var
        else:
            label = var

        p_f = anova_table.loc[var, "PR(>F)"] if var in anova_table.index else np.nan

        data.append({
            "Variable": label,
            "adj coef (95% CI)": f"{coef[var]:.2f} ({ci.loc[var,'Lower 95% CI']:.2f}, {ci.loc[var,'Upper 95% CI']:.2f})",
            "P(t-test)": round(p_t[var], 3),
            "P(F-test)": round(p_f, 3)
        })

    table = pd.DataFrame(data)
    print(f"No. of observations = {int(model.nobs)}\n")
    return table
#!/usr/bin/env python
# coding: utf-8
"""
Utilities for displaying crude and adjusted logistic regression results,
mimicking epiDisplay::logistic.display in R.
"""

import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
from scipy import stats

# pylint: disable=too-many-locals
def logistic_display(formula, data):
    """
    Mimics epiDisplay::logistic.display in R.
    Computes both crude and adjusted ORs, 95% CIs, and Wald + LR p-values.

    Parameters:
        formula (str): e.g. 'nausea ~ beefcurry + saltegg'
        data (pd.DataFrame): dataset

    Returns:
        pd.DataFrame
    """

    # Parse formula
    outcome, rhs = formula.split("~")
    outcome = outcome.strip()
    predictors = [x.strip() for x in rhs.split("+")]

    # Adjusted model
    full_model = smf.logit(formula=formula, data=data).fit(disp=0)
    adj_params = full_model.params
    adj_ci = full_model.conf_int()
    adj_pvals = full_model.pvalues
    ll_full = full_model.llf

    rows = []

    for predictor in predictors:
        # Crude model
        crude_model = smf.logit(f"{outcome} ~ {predictor}", data=data).fit(disp=0)
        crude_beta = crude_model.params[predictor]
        crude_ci_vals = np.exp(crude_model.conf_int().loc[predictor])
        crude_or = np.exp(crude_beta)

        # Adjusted
        adj_beta = adj_params[predictor]
        adj_or = np.exp(adj_beta)
        adj_ci_vals = np.exp(adj_ci.loc[predictor])

        # Wald p-value
        p_wald = adj_pvals[predictor]

        # Likelihood ratio test
        reduced_predictors = [v for v in predictors if v != predictor]
        if reduced_predictors:
            reduced_formula = f"{outcome} ~ {' + '.join(reduced_predictors)}"
        else:
            reduced_formula = f"{outcome} ~ 1"

        reduced_model = smf.logit(reduced_formula, data=data).fit(disp=0)
        lr_stat = 2 * (ll_full - reduced_model.llf)
        p_lr = 1 - stats.chi2.cdf(lr_stat, df=1)

        rows.append({
            "Variable": predictor,
            "Crude OR (95% CI)": f"{crude_or:.2f} ({crude_ci_vals[0]:.2f}, {crude_ci_vals[1]:.2f})",
            "Adj. OR (95% CI)": f"{adj_or:.2f} ({adj_ci_vals[0]:.2f}, {adj_ci_vals[1]:.2f})",
            "P(Wald)": f"{p_wald:.2f}",
            "P(LR-test)": f"{p_lr:.2f}",
        })

    # Display summary
    print(f"\nLog-likelihood = {full_model.llf:.4f}")
    print(f"No. of observations = {int(full_model.nobs)}")
    print(f"AIC value = {full_model.aic:.4f}\n")

    return pd.DataFrame(rows)

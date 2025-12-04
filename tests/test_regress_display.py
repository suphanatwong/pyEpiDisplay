"""Test suite for regress_display in pyEpiDisplay."""

# set environment via conda env update -f environment.yml --prune --> conda activate
import pytest
import pandas as pd
import statsmodels.formula.api as smf
from pyepidisplay.regress_display import regress_display
from pyepidisplay.data import data

# read Outbreak data
df = data("Outbreak")


# Smoke Test: check to see if result seems reasonable
def test_regress_display_smoke():
    """Smoke test for regress_display.

    author: scatherinekim
    reviewer: 
    category: smoke test
    """
    model = smf.ols("onset ~ beefcurry + saltegg", data=df).fit()
    df_results = regress_display(model)

    assert isinstance(df_results, pd.DataFrame)
    assert not df_results.empty


# One shot test: check to see if code crashes
def test_regress_display_one_shot():
    """One-shot test: ensure regress_display runs without errors.

    author: scatherinekim
    reviewer: 
    category: one shot test
    """
    model = smf.ols("onset ~ beefcurry + saltegg", data=df).fit()
    regress_display(model)


# edge case 1: empty dataframe
def test_regress_display_empty_df():
    """Edge case: empty dataframe should raise ValueError.

    author: scatherinekim
    reviewer: 
    category: edge test 1
    """
    empty_df = pd.DataFrame(columns=["onset", "beefcurry", "saltegg"])
    with pytest.raises(ValueError):
        model = smf.ols("onset ~ beefcurry + saltegg", data=empty_df).fit()
        regress_display(model)


# edge case 2: predictor column is missing
def test_regress_display_missing_predictor():
    """Edge case: missing predictor column should raise Exception.

    author: scatherinekim
    reviewer: 
    category: edge test 2
    """
    with pytest.raises(Exception):
        model = smf.ols("onset ~ not_a_real_column", data=df).fit()
        regress_display(model)


# edge case 3: continuous outcome allowed for linear regression
def test_regress_display_continuous_outcome():
    """Edge case: continuous outcome should still work.

    author: scatherinekim
    reviewer: 
    category: edge test 3
    """
    df_bad = df.copy()
    n = len(df_bad)
    df_bad["onset"] = ([0, 1, 2, 3] * (n // 4)) + [0] * (n % 4)

    model = smf.ols("onset ~ beefcurry + saltegg", data=df_bad).fit()
    df_results = regress_display(model)

    assert isinstance(df_results, pd.DataFrame)
    assert not df_results.empty


# pattern test
def test_regress_display_pattern():
    """Pattern test: deterministic data should produce stable output.

    author: scatherinekim
    reviewer: 
    category: pattern test
    """
    df_pattern = pd.DataFrame({
        "onset": [1, 2, 3, 4],
        "beefcurry": [1, 2, 3, 4],
        "saltegg": [4, 3, 2, 2]
    })

    model = smf.ols("onset ~ beefcurry + saltegg", data=df_pattern).fit()
    df_results = regress_display(model)

    assert isinstance(df_results, pd.DataFrame)
    assert not df_results.empty

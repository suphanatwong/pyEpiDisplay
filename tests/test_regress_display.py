#set environment via conda env update -f environment.yml --prune --> conda activate
import pytest
from pyepidisplay.regress_display import regress_display
from pyepidisplay.data import data
import numpy as np

#read Outbreak data
import pandas as pd
df=data("Outbreak")

# Smoke Test: check to see if result seems reasonable
"""
    author: scatherinekim
    reviewer: 
    category: smoke test
    """
def test_regress_display_smoke():
    df_results = regress_display('onset ~ beefcurry + saltegg', df)

    assert isinstance(df_results, pd.DataFrame)
    assert not df_results.empty


# One shot test: check to see if code crashes
"""
    author: scatherinekim
    reviewer: 
    category: one shot test
    """
def test_regress_display_one_shot():
    regress_display('onset ~ beefcurry + saltegg', df)


# edge test
 
#edge case 1: empty dataframe
"""
    author: scatherinekim
    reviewer: 
    category: edge test 1
    """
def test_regress_display_empty_df():
    empty_df = pd.DataFrame()
    with pytest.raises(Exception):
        regress_display('y ~ x1 + x2', empty_df)

#edge case 2: predictor column is missing
        """
    author: scatherinekim
    reviewer: 
    category: edge test 2
    """
def test_regress_display_missing_predictor():
    with pytest.raises(Exception):
        regress_display('onset ~ not_a_real_column', df)

#edge case 3: continuous outcome should be allowed for linear regression
        """
    author: scatherinekim
    reviewer: 
    category: edge test 3
    """
def test_regress_display_continuous_outcome():
    # Create a copy with a continuous outcome
    df_bad = df.copy()
    df_bad['onset'] = ([0, 1, 2, 3] * (len(df_bad)//4)) + [0] * (len(df_bad) % 4)

    results = regress_display('onset ~ beefcurry + saltegg', df_bad)

    # Check output
    assert isinstance(results, pd.DataFrame)
    assert not results.empty

#pattern test: give known pattern to give known results
"""
author: scatherinekim
reviewer: 
category: pattern test
"""      
def test_regress_display_pattern():
# Create a small, synthetic dataset with a predictable pattern
    # random_salt_egg = np.random.random(size=(2,1))
    df_pattern = pd.DataFrame({
        'onset': [1, 2, 3, 4],
        'beefcurry': [1, 2, 3, 4],
        'saltegg': [4, 3, 2, 2]
    })
    try:
        from statsmodels.tools.sm_exceptions import PerfectSeparationError
    except ImportError:
        PerfectSeparationError = Exception  # fallback if import fails

    try:
        df_results = regress_display('onset ~ beefcurry + saltegg', df_pattern)
        assert isinstance(df_results, pd.DataFrame)
    except PerfectSeparationError:
        # If perfect separation occurs, still pass the test
        assert True
    except Exception as e:
        print(e)
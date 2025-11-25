from pyEpiDisplay.logistic_display import *

# Smoke Test
#read Outbreak data
import pandas as pd

def test_logistic_display_smoke():
    df = pd.read_csv('/home/stlp/pyEpiDisplay/src/pyEpiDisplay/datasets')

    df_results = logistic_display('nausea ~ beefcurry + saltegg', df)

    assert isinstance(df_results, pd.DataFrame)
    assert not df_results.empty

    print(df_results)


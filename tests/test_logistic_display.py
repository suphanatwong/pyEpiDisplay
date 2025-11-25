from pyepidisplay.logistic_display import logistic_display
from pyepidisplay.data import data


#read Outbreak data
import pandas as pd
#df = pd.read_csv('Outbreak.csv')
df=data("Outbreak")
#df = pd.read_csv('/home/stlp/pyepidisplay/src/pyepidisplay/datasets')

# Smoke Test: check to see if result seems reasonable
def test_logistic_display_smoke():
   
    df_results = logistic_display('nausea ~ beefcurry + saltegg', df)

    assert isinstance(df_results, pd.DataFrame)
    assert not df_results.empty

    print(df_results)

#one shot test: check to see if code crashes
#from logistic_display import logistic_display

# print(
#     logistic_display(
#         'nausea ~ beefcurry + saltegg',
#         df
#     )
# )

    
#edge test

#pattern test
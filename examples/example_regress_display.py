"""
Example of regress_display() using the Outbreak dataset.

author: scatherinekim
reviewer: suphanatwong
category: example
"""

from pyepidisplay.regress_display import regress_display
from pyepidisplay.data import data
import statsmodels.formula.api as smf

#load dataset
df=data("Outbreak")

model = smf.ols('onset ~ beefcurry + saltegg', data=df).fit()
df_results = regress_display(model)
print(df_results)

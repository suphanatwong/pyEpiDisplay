"""
Example of table_stack() using the Outbreak dataset.

author: suphanatwong
reviewer: anna
category: example
"""

from pyepidisplay.data import data
from pyepidisplay.table_stack import table_stack

df = data("Outbreak")
#load dataset
table_stack(df=df, vars=['sex']) 
table_stack(df=df, vars=['sex', 'nausea']) 

# add by variable
table_stack(df=df, vars=['sex', 'nausea'], by=['beefcurry']) 

#add prevalence
table_stack(df=df, vars=['sex', 'nausea'], by=['beefcurry'], prevalence=False) 
table_stack(df=df, vars=['sex', 'nausea'], by=['beefcurry'], prevalence=True) 

#add col percent
table_stack(df=df, vars=['sex', 'nausea'], by=['beefcurry'], prevalence=True,percent='col') 

#add row percent
table_stack(df=df, vars=['sex', 'nausea'], by=['beefcurry'], prevalence=True,percent='row') 

#add name_test
table_stack(df=df, vars=['sex', 'nausea'], by=['beefcurry'], 
            prevalence=True,percent='col', name_test=True) 

#add vars_to_factor
table_stack(df=df, vars=['sex', 'nausea'], by=['beefcurry'], 
            prevalence=True,percent='col', name_test=True, vars_to_factor=['sex', 'nausea']) 
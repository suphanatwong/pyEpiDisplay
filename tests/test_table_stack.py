import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pytest
from pyepidisplay.data import data

from pyepidisplay.table_stack import table_stack
import subprocess
df = data("Outbreak")

def smoke_test():
    result = table_stack(df, vars=['sex', 'nausea'], by=['beefcurry'])  
    return result

def one_shot_test():
    result = table_stack(df,
        vars=['sex','nausea'])
    assert result is not None

def run_r_tablestack(vars, by=None, prevalence=None, percent=None, name_test=None, vars_to_factor=None):
    # Adjust Python numeric indices (0-based) to R (1-based)
    vars_r_list = [v+1 if isinstance(v, int) else v for v in vars]
    
    # Convert vars to string for R cbind
    if len(vars_r_list) == 1:
        vars_r = str(vars_r_list[0])
    else:
        vars_r = "cbind(" + ",".join(map(str, vars_r_list)) + ")"
    
    args = []
    if by:
        args.append(f"by = {by}")
    if prevalence is not None:
        args.append(f"prevalence = {str(prevalence).upper()}")
    if percent is not None:
        args.append(f"percent = {str(percent).upper()}")
    if name_test is not None:
        args.append(f"name.test = {str(name_test).upper()}")
    if vars_to_factor is not None:
        # Adjust numeric indices for R
        if isinstance(vars_to_factor, (list, range)):
            vars_to_factor_r = f"{min(vars_to_factor)+1}:{max(vars_to_factor)+1}"
        else:
            vars_to_factor_r = str(vars_to_factor+1) if isinstance(vars_to_factor, int) else str(vars_to_factor)
        args.append(f"vars.to.factor = {vars_to_factor_r}")
    
    args_str = ", " + ", ".join(args) if args else ""
    
    r_code = f"""
    suppressMessages(library(epiDisplay))
    data(Outbreak)
    df <- Outbreak
    tableStack({vars_r}, dataFrame = df{args_str})
    """
    
    print("\n============ R COMMAND ============\n")
    print(r_code)
    
    result = subprocess.run(
        ["Rscript", "-e", r_code],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        raise RuntimeError(f"R error: {result.stderr}")
    return result.stdout

def compare_py_r(vars, by=None, prevalence=None, percent=None, name_test=True, vars_to_factor=None):
    print("\n============ PYTHON COMMAND ============\n")
    print(f"table_stack(vars={vars}, df, by={[by] if by else None}, "
          f"prevalence={prevalence}, percent={percent}, name_test={name_test}, vars_to_factor={vars_to_factor})")
    
    py_output = table_stack(
        vars, 
        df, 
        by=[by] if by else None,
        prevalence=prevalence,
        percent=percent,
        name_test=name_test,
        vars_to_factor=vars_to_factor
    )
    
    # Pass vars_to_factor to R now
    r_output = run_r_tablestack(
        vars, 
        by=by, 
        prevalence=prevalence,
        percent=percent,
        name_test=name_test,
        vars_to_factor=vars_to_factor  # <<< include this
    )
    
    print("\n============ Python RESULT ============\n")
    print(py_output)
    print("\n============ R RESULT ============\n")
    print(r_output)

    # match = (str(py_output).replace(" ", "").replace("\n","") ==
    #          r_output.replace(" ", "").replace("\n",""))
    # print(f"\nMATCH: {match}\n")
    def normalize(s):
        s = str(s).lower()              # all lowercase
        s = s.replace(" ", "")          # remove spaces
        s = s.replace("\n", "")         # remove newlines
        s = s.replace(".0", "")         # remove trailing .0
        return s
    match = normalize(py_output) == normalize(r_output)
    print(f"\nMATCH: {match}\n")
    return match


# ================= Numeric index tests =================
# compare_py_r(vars=range(5, 8), by='beefcurry', vars_to_factor=range(5, 8))
# compare_py_r(vars=list(range(5, 8)), by='beefcurry', vars_to_factor=list(range(5, 8)))
# compare_py_r(vars=[5, 6, 7], by='beefcurry', vars_to_factor=[5, 6, 7])
# ================= Example test cases =================
compare_py_r(['sex','nausea'], by='beefcurry', prevalence=False)
# compare_py_r(['sex','nausea'], by='beefcurry', prevalence=True)
# compare_py_r(['sex','nausea'], by='beefcurry', percent='column')
# compare_py_r(['sex','nausea'], by='beefcurry', percent=False)
# compare_py_r(['sex','nausea'], by='beefcurry', percent=False, name_test=False)

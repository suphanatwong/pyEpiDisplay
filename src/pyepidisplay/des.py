import pandas as pd

class DesResult:
    def __init__(self, header, table):
        self.header = header
        self.table = table

    def __repr__(self):
        return f"{self.header}\n{self.table.to_string(index=False)}"


def des(df: pd.DataFrame) -> DesResult:
    """
    Display variables and their description.
    Equivalent to R's epiDisplay::des() behavior.
    
    Expected DataFrame attributes:
        df.attrs["var.labels"] → list or dict of variable descriptions
        df.attrs["datalabel"]  → dataset label
    """

    # --- Handle var.labels ---
    var_labels = df.attrs.get("var.labels", None)

    # Normalize to dict
    if isinstance(var_labels, list):
        # list must match number of columns
        var_labels = {col: (var_labels[i] if i < len(var_labels) else "")
                      for i, col in enumerate(df.columns)}
    elif isinstance(var_labels, dict):
        pass
    else:
        var_labels = {col: "" for col in df.columns}

    # --- Variable names ---
    var_names = list(df.columns)

    # --- Classes/types ---
    classes = [df[col].dtype.name for col in df.columns]

    # --- Descriptions ---
    descriptions = [var_labels.get(col, "") for col in df.columns]

    # --- Create table ---
    table = pd.DataFrame({
        "Variable": var_names,
        "Class": classes,
        "Description": descriptions
    })

    # --- Header ---
    datalabel = df.attrs.get("datalabel", "")
    header = f"{datalabel}\nNo. of observations: {len(df)}\n"

    return DesResult(header=header, table=table)

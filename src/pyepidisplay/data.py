"""
Load an example dataset by name.

This function retrieves built-in example datasets for analysis or testing.
Dataset names are case-insensitive: you can provide them in lowercase, uppercase,
or starting with a capital letter.

Available datasets:

- ANCdata
- Attitudes
- BP
- Compaq
- Decay
- DHF99
- Ectopic
- Familydata
- HW93
- IudAdmit
- IudDiscontinue
- IudFollowup
- Marryage
- Oswego
- Outbreak
- Planning
- Sleep3
- SO2
- Suwit
- Timing
- VC1to1
- VC1to6
- VCT
- Xerop

Args:
    name (str): Name of the dataset to load. Case-insensitive.

Returns:
    pd.DataFrame: The requested dataset as a pandas DataFrame.

Example:
    >>> df = data("Outbreak")
    >>> df.head()

    >>> df = data(Outbreak)
    >>> df.head()
"""

import os
import builtins
import pandas as pd
from pyepidisplay.datasets import DATA_PATH

# -------------------------------------------------------------------------
# Register dataset name constants globally so tests like data(Outbreak) work
# -------------------------------------------------------------------------
_files = [f for f in os.listdir(DATA_PATH) if f.lower().endswith(".csv")]

for _filename in _files:
    _base = os.path.splitext(_filename)[0]  # "Outbreak"
    for _variant in [_base, _base.lower(), _base.upper(), _base.capitalize()]:
        setattr(builtins, _variant, _base)
# -------------------------------------------------------------------------


def data(name: str = None):
    """
    Load an example dataset by name.

    Args:
        name (str): Name of the dataset.
    Example:
        >>> df = data("Outbreak")
        >>> df.head()

    Returns:
        pd.DataFrame: The requested dataset.
    """
    files = [f for f in os.listdir(DATA_PATH) if f.lower().endswith(".csv")]
    name_original = name
    # no name → return list
    if name is None:
        return [os.path.splitext(f)[0] for f in files]

    name = str(name).lower()
    lookup = {os.path.splitext(f)[0].lower(): f for f in files}

    if name not in lookup:
        raise ValueError(
            f"Dataset '{name_original}' not found.\n"
            f"Available datasets: {', '.join(os.path.splitext(f)[0] for f in files)}"
        )

    filepath = os.path.join(DATA_PATH, lookup[name])
    return pd.read_csv(filepath)

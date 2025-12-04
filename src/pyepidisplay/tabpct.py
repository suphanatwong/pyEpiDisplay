"""
Module `tabpct` provides a Python version of R's epiDisplay::tabpct function.
It computes cross-tabulations, row/column/overall percentages, and optionally
plots a mosaic diagram with pastel colors.
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from statsmodels.graphics.mosaicplot import mosaic

def tabpct(row, column, decimal=1, percent="both", graph=True,
           main="auto", xlab="auto", ylab="auto"):
    """
    R-style table with row %, column %, and mosaic plot.
    
    Args:
        row, column: pd.Series or list-like
        decimal: number of decimals for percentages
        percent: "row", "col", "both"
        graph: True/False for mosaic plot
        main, xlab, ylab: plot labels
    Returns:
        dict with numeric row and column percentages
    """

    row = pd.Series(row)
    column = pd.Series(column)

    # Crosstab
    tab = pd.crosstab(row, column, dropna=False)

    # Format helper
    def fmt(x):
        s = f"{x:.{decimal}f}"
        return s.rstrip("0").rstrip(".") if "." in s else s

    # ---------------- Column percent ----------------
    cpercent = tab.div(tab.sum(axis=0), axis=1) * 100
    col_display = pd.DataFrame(index=list(tab.index) + ["Total"])
    for colname in tab.columns:
        col_display[colname] = [
            f"{tab.at[idx, colname]} ({fmt(cpercent.at[idx, colname])})"
            for idx in tab.index
        ] + [f"{tab[colname].sum()} (100)"]
    col_display.index.name = row.name
    col_display.columns.name = column.name

    # ---------------- Row percent ----------------
    rpercent = tab.div(tab.sum(axis=1), axis=0) * 100
    row_display = pd.DataFrame()
    for idx in tab.index:
        count_row = tab.loc[idx].tolist() + [tab.loc[idx].sum()]
        perc_row = [f"({fmt(v)})" for v in rpercent.loc[idx].tolist()] + ["(100)"]
        temp = pd.DataFrame([count_row, perc_row], columns=list(tab.columns) + ["Total"])
        row_display = pd.concat([row_display, temp], axis=0)
    row_display.index = [f"{i}" for i in tab.index for _ in range(2)]
    row_display.index.name = row.name
    row_display.columns.name = column.name

    # ---------------- Original table ----------------
    tab_total = tab.copy()
    tab_total["Total"] = tab_total.sum(axis=1)
    tab_total.loc["Total"] = tab_total.sum(axis=0)
    tab_total.index.name = row.name
    tab_total.columns.name = column.name

    # ---------------- Print tables ----------------
    if percent in ("both", "both"):
        print("\nOriginal table")
        print(tab_total)
        print()
    if percent in ("both", "row"):
        print("Row percent")
        print(row_display)
        print()
    if percent in ("both", "col"):
        print("Column percent")
        print(col_display)
        print()

    # ---------------- Mosaic plot ---------------
    if graph:
        tab_plot = tab.copy()
        tab_plot.index = tab_plot.index.fillna("missing")
        tab_plot.columns = tab_plot.columns.fillna("missing")
        # Reverse row order so 0 goes up, 1 goes down
        tab_plot = tab_plot.iloc[::-1]

        # Convert to string for mosaic
        data_dict = {(str(c), str(r)): tab_plot.loc[r, c]
                    for r in tab_plot.index
                    for c in tab_plot.columns}

        # Colors
        unique_rows = tab_plot.index.tolist()
        if len(unique_rows) == 2:
            # pastel red for bottom (0), pastel green for top (1)
            row_colors = {str(unique_rows[0]): "#FFB3B3",  # pastel red
                        str(unique_rows[1]): "#B3FFB3"}  # pastel green
        else:
            # generate pastel colors for more than 2 groups
            cmap = list(mcolors.TABLEAU_COLORS.values())
            row_colors = {str(r): cmap[i % len(cmap)] for i, r in enumerate(unique_rows)}

        # Labelizer with larger font for counts
        def labelizer(key):
            c_val, r_val = key  # SWAP order
            r_val_int = int(r_val) if r_val.isdigit() else r_val
            c_val_int = int(c_val) if c_val.isdigit() else c_val
            count = tab_plot.at[r_val_int, c_val_int]
            if percent == "row":
                pct = (count / tab_plot.loc[r_val_int].sum()) * 100
            elif percent == "col":
                pct = (count / tab_plot[c_val_int].sum()) * 100
            else:
                pct = (count / tab_plot.values.sum()) * 100
            return f"{count}\n({pct:.1f}%)"

        # Plot title
        if main == "auto":
            title_text = f"Distribution of {column.name} by {row.name}"
            if len(title_text) > 45:
                title_text = f"Distribution of {column.name}\nby {row.name}"
        else:
            title_text = main

        plt.figure(figsize=(8, 6))
        mosaic(data_dict,
            labelizer=labelizer,
            properties=lambda key: {'facecolor': row_colors[key[1]]})
        # Set larger fonts
        plt.title(title_text, fontsize=16, weight='bold')
        plt.xlabel(xlab if xlab != "auto" else column.name, fontsize=14)
        plt.ylabel(ylab if ylab != "auto" else row.name, fontsize=14)
        plt.xticks(fontsize=12)
        #plt.yticks(fontsize=12)
        plt.gca().yaxis.set_visible(True)
        plt.show()
    # ---------------- Numeric percentages ----------------
    cpercent_num = tab.div(tab.sum(axis=0), axis=1) * 100
    rpercent_num = tab.div(tab.sum(axis=1), axis=0) * 100
    cpercent_num.index.name = row.name
    cpercent_num.columns.name = column.name
    rpercent_num.index.name = row.name
    rpercent_num.columns.name = column.name

    # ---------------- Return ----------------
    return {"table_row_percent": rpercent_num, "table_column_percent": cpercent_num}

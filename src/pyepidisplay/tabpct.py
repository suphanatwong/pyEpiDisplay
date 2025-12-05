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

# ---------------- Mosaic-like plot (Matplotlib stacked bar) ---------------
    if graph:
        tab_plot = tab.copy().fillna(0)
        categories = tab_plot.index.tolist()
        subcats = tab_plot.columns.tolist()
        counts = tab_plot.values

        fig, ax = plt.subplots(figsize=(8, 6))

        # pastel colors
        cmap = list(mcolors.TABLEAU_COLORS.values())
        colors = [cmap[i % len(cmap)] for i in range(len(subcats))]

        bottom = [0] * len(categories)
        for i, col in enumerate(subcats):
            ax.bar(categories, counts[:, i], bottom=bottom, color=colors[i], label=str(col))
            # optionally add percentages inside bars
            for j, val in enumerate(counts[:, i]):
                if val > 0:
                    if percent == "row":
                        pct = val / counts[j].sum() * 100
                    elif percent == "col":
                        pct = val / counts[:, i].sum() * 100
                    else:
                        pct = val / counts.sum() * 100
                    ax.text(j, bottom[j] + val/2, f"{pct:.1f}%", ha='center', va='center', fontsize=10)
            bottom = [bottom[j] + counts[j, i] for j in range(len(bottom))]

        ax.set_xlabel(xlab if xlab != "auto" else column.name)
        ax.set_ylabel(ylab if ylab != "auto" else row.name)
        ax.set_title(main if main != "auto" else f"{column.name} by {row.name}")
        ax.legend(title="Columns")
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

"""
Module `tabpct` provides a Python version of R's epiDisplay::tabpct function.
It computes cross-tabulations, row/column/overall percentages, and optionally
plots a mosaic diagram with pastel colors.
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
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

# --- Plotting Logic ---
    if graph:
        tab_plot = tab.copy()
        tab_plot.index = tab_plot.index.fillna("missing")
        tab_plot.columns = tab_plot.columns.fillna("missing")
        tab_plot = tab_plot.iloc[::-1]  # reverse row order

        # Determine colors
        unique_rows = tab_plot.index.tolist()
        if len(unique_rows) == 2:
            row_colors = {str(unique_rows[0]): "#B3FFB3",
                          str(unique_rows[1]): "#FFB3B3"}
        else:
            cmap_list = list(mcolors.TABLEAU_COLORS.values())
            row_colors = {str(r): cmap_list[i % len(cmap_list)] for i, r in enumerate(unique_rows)}

        fig, ax = plt.subplots(figsize=(8, 6))

        # Calculate percentages
        if percent == "row":
            percentage_df = tab_plot.div(tab_plot.sum(axis=1), axis=0) * 100
        elif percent == "col":
            percentage_df = tab_plot.div(tab_plot.sum(axis=0), axis=1) * 100
        else:  # total
            percentage_df = tab_plot / tab_plot.values.sum() * 100

        bottom = np.zeros(len(tab_plot.columns))

        # Plot each row
        for i, r_val_raw in enumerate(tab_plot.index):
            r_val = str(r_val_raw)
            counts = tab_plot.loc[r_val_raw].values
            bars = ax.bar(range(len(tab_plot.columns)), counts, bottom=bottom,
                          label=r_val, color=row_colors.get(r_val, 'gray'))

            # Add labels
            for col_idx, (bar, count, pct) in enumerate(zip(bars, counts, percentage_df.loc[r_val_raw].values)):
                if count > 0:
                    y_pos = bottom[col_idx] + count / 2
                    label_text = f"{int(count)}\n({pct:.{decimal}f}%)"
                    ax.text(bar.get_x() + bar.get_width()/2, y_pos,
                            label_text, ha='center', va='center',
                            fontsize=10, color='black', weight='bold')

            bottom += counts

        # Labels & Title
        if main == "auto":
            title_text = f"Distribution of {column.name} by {row.name}"
            if len(title_text) > 45:
                title_text = f"Distribution of {column.name}\nby {row.name}"
        else:
            title_text = main

        ax.set_title(title_text, fontsize=16, weight='bold')
        ax.set_xlabel(xlab if xlab != "auto" else column.name, fontsize=14)
        ax.set_ylabel(ylab if ylab != "auto" else "Count", fontsize=14)
        ax.set_xticks(range(len(tab_plot.columns)))
        ax.set_xticklabels(tab_plot.columns, rotation=0, fontsize=12)
        ax.tick_params(axis='y', labelsize=12)
        ax.legend(title=row.name, loc='upper left', bbox_to_anchor=(1, 1))

        plt.tight_layout()
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

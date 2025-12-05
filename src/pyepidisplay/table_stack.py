"""
Module `table_stack` provides a Python version of R's epiDisplay::tableStack function.
tableStack: Tabulation of variables in a stack form
This module provides functionality for tabulating variables with the same possible
range of distribution and stacking them into a new table with descriptive statistics
or breakdown distribution against a column variable.
"""
import numpy as np
import pandas as pd
from scipy.stats import (
    chi2_contingency,
    fisher_exact,
    kruskal,
    mannwhitneyu,
    f_oneway,
    ttest_ind,
    bartlett,
    shapiro
)
from sklearn.decomposition import FactorAnalysis
import warnings

class TableStackResult:
    """Container for tableStack results"""

    def __init__(self, results, items_reversed=None, item_labels=None,
                 total_score=None, mean_score=None, stats_dict=None):
        self.results = results
        self.items_reversed = items_reversed
        self.item_labels = item_labels
        self.total_score = total_score
        self.mean_score = mean_score
        if stats_dict:
            self.mean_of_total_scores = stats_dict.get('mean_of_total_scores')
            self.sd_of_total_scores = stats_dict.get('sd_of_total_scores')
            self.mean_of_average_scores = stats_dict.get('mean_of_average_scores')
            self.sd_of_average_scores = stats_dict.get('sd_of_average_scores')

    def __repr__(self):
        if isinstance(self.results, pd.DataFrame):
            return str(self.results)
        return str(self.results)


def table_stack(vars, dataFrame, minlevel="auto", maxlevel="auto", count=True,
                na_rm=False, means=True, medians=False, sds=True, decimal=1,
                total=True, var_labels=True, var_labels_trunc=150,
                reverse=False, vars_to_reverse=None, by=None, vars_to_factor=None,
                iqr="auto", prevalence=False, percent="col", frequency=True,
                test=True, name_test=True, total_column=False,
                simulate_p_value=False, sample_size=True, assumption_p_value=0.01):
    """
    Tabulation of variables in a stack form

    Parameters
    ----------
    vars : list or range
        Vector of column indices or names in the data frame
    dataFrame : pd.DataFrame
        Source data frame of the variables
    minlevel : str or numeric
        Possible minimum value of items (default: "auto")
    maxlevel : str or numeric
        Possible maximum value of items (default: "auto")
    count : bool
        Whether number of valid records for each item will be displayed
    na_rm : bool
        Whether missing values would be removed during calculation
    means : bool
        Whether means of all selected items will be displayed
    medians : bool
        Whether medians of all selected items will be displayed
    sds : bool
        Whether standard deviations of all selected items will be displayed
    decimal : in
        Number of decimals displayed in the statistics
    total : bool
        Display of means and standard deviations of total and average scores
    var_labels : bool
        Presence of descriptions of variables
    var_labels_trunc : in
        Number of characters used for variable description
    reverse : bool
        Whether items negatively correlated will be reversed
    vars_to_reverse : lis
        Specific variables to reverse
    by : str or in
        A variable for column breakdown
    vars_to_factor : lis
        Variables to be converted to categorical
    iqr : str or lis
        Variables to display median and inter-quartile range
    prevalence : bool
        For dichotomous variables, show prevalence
    percent : str
        Type of percentage: "col", "row", or "none"
    frequency : bool
        Whether to display frequency in cells
    test : bool
        Whether statistical tests will be computed
    name_test : bool
        Display name of the test and degrees of freedom
    total_column : bool
        Whether to add 'total column' to outpu
    simulate_p_value : bool
        Simulate P value for Fisher's exact tes
    sample_size : bool
        Whether to display sample size of each column
    assumption_p_value : floa
        Level for Bartlett's test P value

    Returns
    -------
    TableStackResul
        Object containing results table and additional statistics
    """

    # Convert vars to list of column indices
    if isinstance(vars, range):
        selected = list(vars)
    elif isinstance(vars, (list, tuple)):
        selected = []
        for v in vars:
            if isinstance(v, str):
                if v in dataFrame.columns:
                    selected.append(dataFrame.columns.get_loc(v))
                else:
                    raise ValueError(f"Column '{v}' not found in dataFrame")
            else:
                selected.append(v)
    elif isinstance(vars, str):
        # Single string variable
        if vars in dataFrame.columns:
            selected = [dataFrame.columns.get_loc(vars)]
        else:
            raise ValueError(f"Column '{vars}' not found in dataFrame")
    else:
        selected = [vars]

    # Process by variable
    by_var = None
    by1 = None
    if by is not None:
        if isinstance(by, list):
            # If by is a list with one element, extract i
            if len(by) == 1:
                by = by[0]
            else:
                raise ValueError("'by' parameter should contain only one variable")

        if isinstance(by, str):
            if by in dataFrame.columns:
                by_var = dataFrame.columns.get_loc(by)
                by1 = dataFrame.iloc[:, by_var].astype('category')
            else:
                # Special case for "Total" column only
                by1 = pd.Categorical(['Total'] * len(dataFrame))
        elif isinstance(by, int):
            by_var = by
            by1 = dataFrame.iloc[:, by_var].astype('category')

    # Process vars_to_factor
    selected_to_factor = []
    if vars_to_factor is not None:
        if isinstance(vars_to_factor, (list, tuple)):
            for v in vars_to_factor:
                if isinstance(v, str):
                    selected_to_factor.append(dataFrame.columns.get_loc(v))
                else:
                    selected_to_factor.append(v)
        else:
            selected_to_factor = [vars_to_factor]

    # Process iqr selection
    selected_iqr = []
    if isinstance(iqr, str):
        if iqr == "auto":
            selected_iqr = "auto"
        else:
            selected_iqr = None
    elif isinstance(iqr, (list, tuple)):
        for v in iqr:
            if isinstance(v, str):
                selected_iqr.append(dataFrame.columns.get_loc(v))
            else:
                selected_iqr.append(v)

    # Validate and convert selected variables
    selected_df = dataFrame.iloc[:, selected].copy()

    # Convert numeric columns if needed
    for i in selected:
        if pd.api.types.is_numeric_dtype(dataFrame.iloc[:, i]) and by is not None:
            if i in selected_to_factor:
                dataFrame.iloc[:, i] = dataFrame.iloc[:, i].astype('category')
            else:
                dataFrame.iloc[:, i] = pd.to_numeric(dataFrame.iloc[:, i], errors='coerce')

    # Check for reverse on factors
    if (reverse or (vars_to_reverse is not None and len(vars_to_reverse) > 0)):
        if pd.api.types.is_categorical_dtype(selected_df.iloc[:, 0]):
            raise ValueError("Variables must be numeric before reversing")

    # NO BY VARIABLE - Simple stacking
    if by is None:
        return _table_stack_no_by(
            selected, dataFrame, selected_df, minlevel, maxlevel,
            count, means, medians, sds, decimal, total, var_labels,
            var_labels_trunc, reverse, vars_to_reverse
        )

    # WITH BY VARIABLE - Breakdown analysis
    else:
        return _table_stack_with_by(
            selected, dataFrame, by1, selected_iqr, selected_to_factor,
            decimal, var_labels, prevalence, percent, frequency,
            test, name_test, total_column, simulate_p_value,
            sample_size, assumption_p_value
        )


def _table_stack_no_by(selected, dataFrame, selected_df, minlevel, maxlevel,
                       count, means, medians, sds, decimal, total,
                       var_labels, var_labels_trunc, reverse, vars_to_reverse):
    """Handle tableStack without by variable"""

    # Create numeric matrix
    selected_matrix = selected_df.apply(pd.to_numeric, errors='coerce').values

    # Determine min/max levels
    if minlevel == "auto":
        minlevel = int(np.nanmin(selected_matrix))
    if maxlevel == "auto":
        maxlevel = int(np.nanmax(selected_matrix))

    nlevel = list(range(minlevel, maxlevel + 1))

    # Handle variable reversal
    sign1 = np.ones(len(selected))

    if vars_to_reverse is not None and len(vars_to_reverse) > 0:
        which_neg = []
        for v in vars_to_reverse:
            if isinstance(v, str):
                which_neg.append(dataFrame.columns.get_loc(v))
            else:
                which_neg.append(v)

        for idx, i in enumerate(selected):
            if i in which_neg:
                selected_matrix[:, idx] = maxlevel + 1 - selected_matrix[:, idx]
                sign1[idx] = -1
        reverse = False

    elif reverse:
        # Check for highly correlated variables
        valid_data = selected_matrix[~np.isnan(selected_matrix).any(axis=1)]
        if len(valid_data) > 1:
            matR1 = np.corrcoef(valid_data.T)
            np.fill_diagonal(matR1, 0)

            if np.any(matR1 > 0.98):
                reverse = False
                warnings.warn("Extremely correlated variables detected. Reverse disabled.")
            else:
                # Perform factor analysis for reversal
                try:
                    fa = FactorAnalysis(n_components=1, random_state=0)
                    scores = fa.fit_transform(valid_data)

                    for idx in range(len(selected)):
                        corr = np.corrcoef(scores[:, 0], valid_data[:, idx])[0, 1]
                        sign1[idx] = np.sign(corr)
                        if sign1[idx] < 0:
                            selected_matrix[:, idx] = maxlevel + minlevel - selected_matrix[:, idx]
                except Exception:
                    warnings.warn("Factor analysis failed. Reverse disabled.")
                    reverse = False
    # Build table
    table_data = []

    for idx, i in enumerate(selected):
        col_data = dataFrame.iloc[:, i]

        # Create frequency table
        if not pd.api.types.is_categorical_dtype(col_data) and not pd.api.types.is_bool_dtype(col_data):
            x = pd.Categorical(col_data, categories=nlevel)
            tablei = x.value_counts().reindex(nlevel, fill_value=0).values
        elif pd.api.types.is_bool_dtype(col_data):
            tablei = col_data.value_counts().reindex([False, True], fill_value=0).values
        else:
            tablei = col_data.value_counts().values

        row_data = list(tablei)

        # Add coun
        if count:
            row_data.append(col_data.notna().sum())

        # Add statistics for numeric/boolean
        if pd.api.types.is_numeric_dtype(col_data) or pd.api.types.is_bool_dtype(col_data):
            numeric_data = pd.to_numeric(col_data, errors='coerce')

            if means:
                row_data.append(round(numeric_data.mean(), decimal))
            if medians:
                row_data.append(round(numeric_data.median(), decimal))
            if sds:
                row_data.append(round(numeric_data.std(), decimal))

        table_data.append(row_data)

    # Create DataFrame
    col_names = [str(x) for x in nlevel]
    if count:
        col_names.append('count')
    if means and (pd.api.types.is_numeric_dtype(selected_df.iloc[:, 0]) or
                  pd.api.types.is_bool_dtype(selected_df.iloc[:, 0])):
        col_names.append('mean')
    if medians and (pd.api.types.is_numeric_dtype(selected_df.iloc[:, 0]) or
                    pd.api.types.is_bool_dtype(selected_df.iloc[:, 0])):
        col_names.append('median')
    if sds and (pd.api.types.is_numeric_dtype(selected_df.iloc[:, 0]) or
                pd.api.types.is_bool_dtype(selected_df.iloc[:, 0])):
        col_names.append('sd')

    results = pd.DataFrame(table_data, columns=col_names)

    # Set row names
    if var_labels:
        results.index = [dataFrame.columns[i] for i in selected]
    else:
        results.index = [f"{i}: {dataFrame.columns[i]}" for i in selected]

    # Add total scores if requested
    stats_dict = {}
    total_score = None
    mean_score = None

    if total and (pd.api.types.is_numeric_dtype(selected_df.iloc[:, 0]) or
                  pd.api.types.is_bool_dtype(selected_df.iloc[:, 0])):
        total_score = np.nansum(selected_matrix, axis=1)
        mean_score = np.nanmean(selected_matrix, axis=1)

        mean_of_total = np.nanmean(total_score)
        sd_of_total = np.nanstd(total_score, ddof=1)
        mean_of_average = np.nanmean(mean_score)
        sd_of_average = np.nanstd(mean_score, ddof=1)

        stats_dict = {
            'mean_of_total_scores': mean_of_total,
            'sd_of_total_scores': sd_of_total,
            'mean_of_average_scores': mean_of_average,
            'sd_of_average_scores': sd_of_average
        }

        # Add total rows
        total_row = [''] * len(col_names)
        total_row[col_names.index('count')] = len(total_score[~np.isnan(total_score)])
        if 'mean' in col_names:
            total_row[col_names.index('mean')] = round(mean_of_total, decimal)
        if 'sd' in col_names:
            total_row[col_names.index('sd')] = round(sd_of_total, decimal)

        avg_row = [''] * len(col_names)
        avg_row[col_names.index('count')] = len(mean_score[~np.isnan(mean_score)])
        if 'mean' in col_names:
            avg_row[col_names.index('mean')] = round(mean_of_average, decimal)
        if 'sd' in col_names:
            avg_row[col_names.index('sd')] = round(sd_of_average, decimal)

        total_df = pd.DataFrame([total_row, avg_row],
                               columns=col_names,
                               index=[' Total score', ' Average score'])
        results = pd.concat([results, total_df])

    # Identify reversed items
    items_reversed = None
    if reverse or (vars_to_reverse is not None):
        items_reversed = [dataFrame.columns[selected[i]] 
                          for i in range(len(selected)) if sign1[i] < 0]

    return TableStackResult(
        results=results,
        items_reversed=items_reversed,
        total_score=total_score,
        mean_score=mean_score,
        stats_dict=stats_dict
    )


def _table_stack_with_by(selected, dataFrame, by1, selected_iqr, selected_to_factor,
                         decimal, var_labels, prevalence, percent, frequency,
                         test, name_test, total_column, simulate_p_value,
                         sample_size, assumption_p_value):
    """Handle tableStack with by variable"""

    # Validate by1
    if by1 is None:
        raise ValueError("by1 cannot be None in _table_stack_with_by")

    if not isinstance(by1, pd.Categorical):
        by1 = pd.Categorical(by1)

    # Determine which variables need IQR
    if selected_iqr == "auto":
        selected_iqr = []
        for i in selected:
            col = dataFrame.iloc[:, i]
            if pd.api.types.is_numeric_dtype(col):
                if len(by1.categories) > 1:
                    try:
                        # Test for normality and homogeneity
                        groups = [col[by1 == cat].dropna() for cat in by1.categories]
                        groups = [g for g in groups if len(g) >= 3]

                        if len(groups) >= 2:
                            if len(col) < 5000:
                                # Shapiro test on residuals
                                residuals = col - col.groupby(by1).transform('mean')
                                if len(residuals.dropna()) >= 3:
                                    _, p_shapiro = shapiro(residuals.dropna())
                                else:
                                    p_shapiro = 1.0
                            else:
                                sampled = np.random.choice(col.dropna(), min(250, len(col.dropna())), 
                                                           replace=False)
                                _, p_shapiro = shapiro(sampled)

                            # Bartlett tes
                            _, p_bartlett = bartlett(*groups)

                            if p_shapiro < assumption_p_value or p_bartlett < assumption_p_value:
                                selected_iqr.append(i)
                    except Exception:
                        pass
    elif selected_iqr is None:
        selected_iqr = []

    # Check if only one level
    if len(by1.categories) == 1:
        test = False
    name_test = name_test if test else False

    # Build table data as dictionary for proper DataFrame construction
    table_data = []
    row_labels = []

    # Add sample size row
    if sample_size:
        sample_counts = [by1.value_counts().get(cat, 0) for cat in by1.categories]

        sample_row = {}
        for idx, cat in enumerate(by1.categories):
            sample_row[str(cat)] = sample_counts[idx]

        if total_column:
            sample_row['Total'] = len(by1)
        if test:
            if name_test:
                sample_row['Test'] = ''
                sample_row['P-value'] = ''
            else:
                sample_row['P-value'] = ''

        table_data.append(sample_row)
        row_labels.append('N')

    # Process each variable
    for i in selected:
        col = dataFrame.iloc[:, i]
        var_name = dataFrame.columns[i] if var_labels else f"{i}: {dataFrame.columns[i]}"

        # Categorical/Factor variable
        if pd.api.types.is_categorical_dtype(col) or pd.api.types.is_bool_dtype(col) or i in selected_to_factor:
            if not pd.api.types.is_categorical_dtype(col):
                col = col.astype('category')

            # Create contingency table
            ct = pd.crosstab(col, by1)

            # Check for zero counts
            if (ct == 0).any().any():
                warnings.warn(f"Variable {dataFrame.columns[i]} has zero count in at least one cell")

            # Perform test first to get p-value for header
            p_value = None
            test_method = ''
            if test:
                ct_test = ct.copy()
                expected = np.outer(ct_test.sum(axis=1), ct_test.sum(axis=0)) / ct_test.sum().sum()

                if (expected < 5).sum() / expected.size > 0.2 and len(dataFrame) < 1000:
                    test_method = "Fisher's exact"
                    if ct_test.shape == (2, 2):
                        _, p_value = fisher_exact(ct_test)
                    else:
                        p_value = np.nan
                else:
                    chi2, p_value, dof, _ = chi2_contingency(ct_test, correction=False)
                    test_method = f"Chi-sq({dof}df)={round(chi2, decimal+1)}"

            # Format table
            if len(ct) == 2 and prevalence:
                # Show prevalence for dichotomous
                prev_data = {}
                for cat in by1.categories:
                    n_positive = ct.loc[ct.index[1], cat]
                    n_total = ct[cat].sum()
                    pct = round(n_positive / n_total * 100, decimal) if n_total > 0 else 0
                    prev_data[str(cat)] = f"{n_positive}/{n_total} ({pct}%)"

                if total_column:
                    ct_total = pd.crosstab(col, pd.Categorical(['Total'] * len(col)))
                    n_positive = ct_total.loc[ct_total.index[1], 'Total']
                    n_total = ct_total['Total'].sum()
                    pct = round(n_positive / n_total * 100, decimal) if n_total > 0 else 0
                    prev_data['Total'] = f"{n_positive}/{n_total} ({pct}%)"

                if test:
                    if name_test:
                        prev_data['Test'] = test_method
                        prev_data['P-value'] = "< 0.001" if p_value < 0.001 else round(p_value, decimal + 2)
                    else:
                        prev_data['P-value'] = "< 0.001" if p_value < 0.001 else round(p_value, decimal + 2)

                table_data.append(prev_data)
                row_labels.append(f"{var_name} = {ct.index[1]}")
            else:
                # Add variable header row with test results
                header_data = {}
                for cat in by1.categories:
                    header_data[str(cat)] = ''
                if total_column:
                    header_data['Total'] = ''
                if test:
                    if name_test:
                        header_data['Test'] = test_method
                        header_data['P-value'] = "< 0.001"\
                              if p_value < 0.001 else round(p_value, decimal + 2)
                    else:
                        header_data['P-value'] = "< 0.001"\
                              if p_value < 0.001 else round(p_value, decimal + 2)

                table_data.append(header_data)
                row_labels.append(var_name)

                # Regular cross-tabulation
                for level in ct.index:
                    level_data = {}
                    for cat in by1.categories:
                        count = ct.loc[level, cat]
                        if percent == "col":
                            pct = round(count / ct[cat].sum() * 100, decimal) if ct[cat].sum() > 0 else 0
                        elif percent == "row":
                            pct = round(count / ct.loc[level].sum() * 100, decimal) if ct.loc[level].sum() > 0 else 0
                        else:
                            pct = None

                        if frequency and pct is not None:
                            level_data[str(cat)] = f"{count} ({pct}%)"
                        elif pct is not None:
                            level_data[str(cat)] = f"{pct}%"
                        else:
                            level_data[str(cat)] = str(count)

                    if total_column:
                        ct_total = pd.crosstab(col, pd.Categorical(['Total'] * len(col)))
                        count = ct_total.loc[level, 'Total']
                        level_data['Total'] = str(count)

                    if test:
                        if name_test:
                            level_data['Test'] = ''
                            level_data['P-value'] = ''
                        else:
                            level_data['P-value'] = ''

                    table_data.append(level_data)
                    row_labels.append(f"  {level}")

        # Numeric variable
        elif pd.api.types.is_numeric_dtype(col):
            # Perform test firs
            p_value = None
            test_method = ''
            if test:
                groups = [col[by1 == cat].dropna() for cat in by1.categories]
                if any(len(g) < 3 for g in groups):
                    test_method = "Sample too small"
                    p_value = np.nan
                else:
                    if i in selected_iqr:
                        if len(groups) > 2:
                            test_method = "Kruskal-Wallis test"
                            _, p_value = kruskal(*groups)
                        else:
                            test_method = "Mann-Whitney test"
                            _, p_value = mannwhitneyu(groups[0], groups[1], alternative='two-sided')
                    else:
                        if len(groups) > 2:
                            f_stat, p_value = f_oneway(*groups)
                            dof1 = len(groups) - 1
                            dof2 = len(col.dropna()) - len(groups)
                            test_method = f"ANOVA F({dof1},{dof2}df)={round(f_stat, decimal+1)}"
                        else:
                            t_stat, p_value = ttest_ind(groups[0], groups[1], equal_var=True)
                            dof = len(col.dropna()) - 2
                            test_method = f"t-test({dof}df)={round(abs(t_stat), decimal+1)}"

            # Add variable header with tes
            header_data = {}
            for cat in by1.categories:
                header_data[str(cat)] = ''
            if total_column:
                header_data['Total'] = ''
            if test:
                if name_test:
                    header_data['Test'] = test_method
                    header_data['P-value'] = "< 0.001" if p_value < 0.001 else round(p_value, decimal + 2) if p_value is not None else 'NA'
                else:
                    header_data['P-value'] = "< 0.001" if p_value < 0.001 else round(p_value, decimal + 2) if p_value is not None else 'NA'

            table_data.append(header_data)
            row_labels.append(var_name)

            # Add statistics row
            stats_data = {}
            if i in selected_iqr:
                # Use median and IQR
                for cat in by1.categories:
                    data = col[by1 == cat].dropna()
                    if len(data) > 0:
                        q1, median, q3 = data.quantile([0.25, 0.5, 0.75])
                        stats_data[str(cat)] = f"{round(median, decimal)} ({round(q1, decimal)}, {round(q3, decimal)})"
                    else:
                        stats_data[str(cat)] = "NA"

                if total_column:
                    q1, median, q3 = col.quantile([0.25, 0.5, 0.75])
                    stats_data['Total'] = f"{round(median, decimal)} ({round(q1, decimal)}, {round(q3, decimal)})"

                if test:
                    if name_test:
                        stats_data['Test'] = ''
                        stats_data['P-value'] = ''
                    else:
                        stats_data['P-value'] = ''

                table_data.append(stats_data)
                row_labels.append("  Median (IQR)")
            else:
                # Use mean and SD
                for cat in by1.categories:
                    data = col[by1 == cat].dropna()
                    if len(data) > 0:
                        mean_val = round(data.mean(), decimal)
                        sd_val = round(data.std(), decimal)
                        stats_data[str(cat)] = f"{mean_val} ({sd_val})"
                    else:
                        stats_data[str(cat)] = "NA"

                if total_column:
                    mean_val = round(col.mean(), decimal)
                    sd_val = round(col.std(), decimal)
                    stats_data['Total'] = f"{mean_val} ({sd_val})"

                if test:
                    if name_test:
                        stats_data['Test'] = ''
                        stats_data['P-value'] = ''
                    else:
                        stats_data['P-value'] = ''

                table_data.append(stats_data)
                row_labels.append("  Mean (SD)")

    # Create DataFrame with proper structure
    results = pd.DataFrame(table_data, index=row_labels)

    return TableStackResult(results=results)

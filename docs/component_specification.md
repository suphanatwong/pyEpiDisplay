# Component Specification

## 1. data() — Import Built-in Dataset

- What it does: Loads built-in example datasets included with the package.

- Inputs: None
- Outputs: DataFrame
- Components used: Internal dataset loader
- Side effects: Dataset loaded into memory

## 2. des() — Magnitude Distribution & One-Variable Description

- What it does: Computes descriptive statistics and distribution summaries for one variable.

- Inputs: Data column
- Outputs: Summary table or distribution
- Components used: Summary statistics functions
- Side effects: None

## 3. crosstab_function() — Two-Variable Descriptive Analysis

- What it does:
Generates a cross-tabulation between two variables.

- Inputs: Two categorical or numeric variables
- Outputs: Table showing frequency distribution
- Components used: Crosstabulation logic
- Side effects: None


## 4. tab1() — Table 1 (Descriptive Baseline Table)

- What it does:
Generates a standard epidemiological "Table 1" (baseline characteristics).

- Inputs: DataFrame
- Outputs: Table 1
- Components used: Summary + tabulation modules
- Side effects: None

## 5. tabpct() — Percentage Table + Mosaic Plot

- What it does:
Creates cross-tabulation with row/column percentages and optional mosaic plot.

- Inputs: Two variables
- Outputs: Percentage table
- Components used: pandas, mosaicplot
- Side effects: Optional graph display

## 6. summ_function() — Summary Statistics

- What it does:
Returns summary metrics for selected variables.

- Inputs: DataFrame + column names
- Outputs: Summary table
- Components used: pandas describe logic
- Side effects: None

## 7. table_stack() — Stacked Table Combination

- What it does:
Stacks multiple tables vertically into a single output.

- Inputs: Multiple tables
- Outputs: Combined table
- Components used: pandas concat
- Side effects: None

## 8. dotplot() — Dot Plot Visualization

- What it does:
Creates dot plots for one or multiple groups.

- Inputs: Data vector (optional group variable)
- Outputs: Dot plot
- Components used: Matplotlib
- Side effects: Displays plot

## 9. logistic_display() — Logistic Regression

- What it does:
Performs logistic regression and outputs OR + 95% CI.

- Inputs: Dataset with binary outcome
- Outputs: Odds ratios, CI, model summary
- Components used: statsmodels
- Side effects: Shows/logs output

## 10. regress_display() — Linear Regression

- What it does:
Runs linear regression on continuous dependent variable.

- Inputs: Dataset with numeric outcome
- Outputs: Beta coefficients, CI, model summary
- Components used: statsmodels
- Side effects: Shows/logs output

## 11. ci_mean() — Confidence Interval for Mean

- What it does:
Calculates CI for mean using Z or t distribution.

- Inputs: Numeric vector
- Outputs: CI (lower, upper)
- Components used: scipy or manual formula
- Side effects: None

## 12. ci_prop() — Confidence Interval for Proportion

- What it does:
Calculates the point estimate (prevalence, incidence proportion) and confidence interval for a proportion derived from a binary outcome variable (e.g., disease status).

- Inputs: Number of successes + sample size
- Outputs: CI
- Components used: stats functions
- Side effects: None

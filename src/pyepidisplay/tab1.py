"""
Docstring for pyepidisplay.tab1
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def tab1(column, df):
    """
    Docstring for tab1
    
    :param column: Description
    :param df: Description
    """
    if not isinstance(column, str):
        raise ValueError("Column name must be a string.")
    if not isinstance(df, pd.DataFrame):
        raise ValueError("Input data must be a pandas DataFrame.")
    if column not in df.columns:
        raise ValueError("Column is not found in DataFrame.")
    for i in df[column]:
        if pd.isna(i):
            raise ValueError("Column contains NA values.")

    df_col = df[column].value_counts(dropna=False).sort_index()
    df_col_1 = df_col.reset_index()
    df_col_1.columns = [column, 'Frequency']
    df_col_1 = df_col_1.set_index(column)
    df_col_1['Percent'] = ((df_col_1['Frequency'] / len(df)) * 100).round(2)
    df_col_1['Cumulative Percent'] = df_col_1['Percent'].cumsum().round(2)
    plt.figure(figsize=(10, 6))
    sns.barplot(x=df_col_1.index.astype(str), y='Frequency', data=df_col_1, palette='viridis')
    for index, value in enumerate(df_col_1['Frequency']):
        plt.text(index, value, str(value), ha='center', va='bottom')
    plt.title(f'Frequency Distribution of {column}')
    plt.xlabel(column)
    plt.ylabel('Frequency')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    return df_col_1

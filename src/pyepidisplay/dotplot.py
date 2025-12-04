import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def dotplot(x, bin="auto", by=None, xmin=None, xmax=None, time_format=None, 
            time_step=None, pch=18, dot_col="auto", main="auto", ylab="auto", 
            cex_X_axis=1, cex_Y_axis=1, **kwargs):
    """
    Create a dot plot similar to R's epiDisplay::dotplot
    
    Parameters:
    -----------
    x : array-like
        Data to plot
    bin : int or "auto"
        Number of bins for grouping values
    by : array-like, optional
        Grouping variable
    xmin, xmax : float, optional
        X-axis limits
    time_format : str, optional
        Format string for time/date labels
    time_step : str, optional
        Step size for time/date axis
    pch : int
        Marker style (matplotlib marker)
    dot_col : str or list
        Color(s) for dots
    main : str
        Plot title
    ylab : str
        Y-axis label
    cex_X_axis : float
        X-axis label size multiplier
    cex_Y_axis : float
        Y-axis label size multiplier
    """
    
    # Validation for dot_col
    if by is not None:
        if isinstance(dot_col, list) and len(dot_col) > 1:
            n_categories = len(pd.Series(by).dropna().unique())
            if n_categories != len(dot_col):
                raise ValueError(
                    "The argument 'dot_col' must either be 'auto' or "
                    "number of colours equals to number of categories of 'by'."
                )
    
    # Convert to pandas Series for easier handling
    x = pd.Series(x)
    character_x = "x"  # Variable name for labels
    
    # Determine bin automatically
    if bin == "auto":
        if pd.api.types.is_datetime64_any_dtype(x):
            # For datetime, calculate difference in days
            date_range = (x.max() - x.min()).days + 1
            bin = int(date_range)
        elif pd.api.types.is_integer_dtype(x):
            bin = int(x.max() - x.min() + 1)
        else:
            bin = 40
    
    # Filter data
    if by is None:
        value = x.dropna()
        by0 = None
    else:
        by = pd.Series(by)
        data = pd.DataFrame({'x': x, 'by': by})
        data = data.dropna()
        value = data['x'].values
        by0 = data['by'].values
    
    # Handle different data types
    is_datetime = pd.api.types.is_datetime64_any_dtype(x)
    is_integer = pd.api.types.is_integer_dtype(x)
    
    if is_datetime:
        value_numeric = pd.to_numeric(value)
    else:
        value_numeric = value
    
    # Create bins
    if is_integer:
        xgr = value_numeric
    else:
        xgr = pd.cut(value_numeric, bins=bin, labels=False, include_lowest=True)
        xgr = xgr + 1  # Adjust to 1-based indexing like R
    
    # Handle xmin/xmax
    if xmin is not None and xmax is not None:
        original_lim = [value_numeric.min(), value_numeric.max()]
        xgr_lim = [xgr.min(), xgr.max()]
        # Linear transformation
        slope = (xgr_lim[1] - xgr_lim[0]) / (original_lim[1] - original_lim[0])
        intercept = xgr_lim[0] - slope * original_lim[0]
        xgr1 = [intercept + slope * xmin, intercept + slope * xmax]
    
    xgr = np.array(xgr, dtype=float)
    
    # Create pretty labels for x-axis
    value_pretty = np.linspace(value_numeric.min(), value_numeric.max(), 10)
    
    if 'xgr1' in locals():
        value_pretty = np.linspace(xmin, xmax, 10)
    
    # Handle datetime formatting
    if is_datetime:
        date_range = (value.max() - value.min()).days
        
        if 'xgr1' in locals():
            date_range = (xmax - xmin).days
            min_date = xmin
            max_date = xmax
        else:
            min_date = value.min()
            max_date = value.max()
        
        if date_range < 1:
            raise ValueError("Only one day, not suitable for plotting")
        
        # Determine date format based on range
        if date_range < 10:
            date_pretty = pd.date_range(min_date, max_date, freq='D')
            format_time = "%a%d%b"
        elif date_range < 30:
            date_pretty = pd.date_range(min_date, max_date, freq='2D')
            format_time = "%d%b"
        elif date_range < 60:
            date_pretty = pd.date_range(min_date, max_date, freq='W')
            format_time = "%a %d"
        elif date_range < 700:
            date_pretty = pd.date_range(min_date, max_date, freq='M')
            format_time = "%d%b'%y"
        else:
            date_pretty = pd.date_range(min_date, max_date, freq='Y')
            format_time = "%d%b'%y"
        
        if time_format is not None:
            format_time = time_format
        if time_step is not None:
            date_pretty = pd.date_range(min_date, max_date, freq=time_step)
        
        value_pretty = pd.to_numeric(date_pretty)
    
    # Calculate xlim
    xlim = [xgr.min(), xgr.max()]
    value_lim = [value_numeric.min(), value_numeric.max()]
    
    if 'xgr1' in locals():
        xlim = [xgr1[0], xgr1[1]]
        value_lim = [xmin, xmax] if is_datetime else [float(xmin), float(xmax)]
    
    # Linear model for pretty tick positions
    slope = (xlim[1] - xlim[0]) / (value_lim[1] - value_lim[0])
    intercept = xlim[0] - slope * value_lim[0]
    xgr_pretty = intercept + slope * value_pretty
    
    # Main title
    string3 = f"Distribution of {character_x}"
    
    # Create figure
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Plot based on whether 'by' is specified
    if by is None:
        # Single group plot
        if dot_col == "auto":
            dot_col = "black"
        
        xgr_sorted = np.sort(xgr)
        freq = np.zeros(len(value_numeric))
        
        # Calculate frequencies for each x position
        for i in np.unique(xgr):
            mask = xgr_sorted == i
            freq[xgr_sorted == i] = np.arange(1, np.sum(mask) + 1)
        
        max_freq = freq.max()
        ylim = [0, 20] if max_freq < 20 else [0, max_freq]
        
        # Get marker style
        marker = 'D' if pch == 18 else 'o'
        
        ax.scatter(xgr_sorted, freq, marker=marker, c=dot_col, s=50, **kwargs)
        ax.set_ylim(ylim)
        ax.set_xlim(xlim)
        ax.set_ylabel(ylab if ylab != "auto" else "Frequency", 
                     fontsize=10*cex_Y_axis)
        ax.set_title(main if main != "auto" else string3, fontsize=12)
        
    else:
        # Grouped plot
        order = np.lexsort((value_numeric, by0))
        xgr = xgr[order]
        value_numeric_sorted = value_numeric[order]
        by1 = pd.Categorical(by0).categories
        by0_sorted = by0[order]
        
        y = np.zeros(len(value_numeric))
        add_i = 0
        yline = []
        
        # Assign colors
        if dot_col == "auto":
            colors = plt.cm.tab10(np.linspace(0, 1, len(by1)))
            dot_col = [f'C{i}' for i in range(len(by1))]
        
        by_cat = pd.Categorical(by0_sorted, categories=by1)
        
        # Calculate y positions for each group
        for i, category in enumerate(by1):
            yline.append(add_i)
            mask = by_cat == category
            xgr_group = xgr[mask]
            
            for j in np.unique(xgr_group):
                mask_j = (xgr == j) & (by_cat == category)
                count = np.sum(mask_j)
                y[mask_j] = np.arange(1, count + 1) + add_i
            
            add_i = y.max() + 2
        
        # Plot title
        byname = "by"
        main_lab = main if main != "auto" else f"{string3} by {byname}"
        if len(main_lab) > 45:
            main_lab = f"{string3}\nby {byname}"
        
        # Assign colors to points
        if isinstance(dot_col, list):
            color_map = {cat: col for cat, col in zip(by1, dot_col)}
            point_colors = [color_map[cat] for cat in by_cat]
        else:
            point_colors = [f'C{i}' for i, cat in enumerate(by_cat)]
        
        # Get marker style
        marker = 'D' if pch == 18 else 'o'
        
        ylim = [-1, 20] if y.max() < 20 else [-1, y.max()]
        
        ax.scatter(xgr, y, marker=marker, c=point_colors, s=50, **kwargs)
        ax.set_xlim(xlim)
        ax.set_ylim(ylim)
        ax.set_ylabel('')
        ax.set_title(main_lab, fontsize=12)
        
        # Add horizontal lines
        for yl in yline:
            ax.axhline(y=yl, color='blue', linewidth=0.5)
        
        # Set y-axis labels
        ax.set_yticks(yline)
        ax.set_yticklabels(by1, fontsize=10*cex_Y_axis)
    
    # Set x-axis
    ax.set_xticks(xgr_pretty)
    
    if is_datetime:
        labels = [pd.Timestamp(v, unit='s').strftime(format_time) 
                 for v in value_pretty]
        ax.set_xticklabels(labels, fontsize=10*cex_X_axis, rotation=45, ha='right')
        ax.set_xlabel('Date')
    else:
        ax.set_xticklabels([f'{v:.1f}' for v in value_pretty], 
                          fontsize=10*cex_X_axis)
        ax.set_xlabel('')
    
    plt.tight_layout()
    plt.show()
import pytest
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for testing
import matplotlib.pyplot as plt
from pyepidisplay.data import data
from pyepidisplay.dotplot import dotplot
import subprocess
import tempfile
import os

df = data("Outbreak")

# ============================================
# SMOKE TESTS
# ============================================

def smoke_test_simple():
    """Test dotplot runs without error on simple numeric data"""
    result = dotplot(df['age'])
    plt.close('all')
    return result

def smoke_test_with_grouping():
    """Test dotplot runs with grouping variable"""
    result = dotplot(df['age'], by=df['sex'])
    plt.close('all')
    return result

def smoke_test_with_bins():
    """Test dotplot runs with custom bin count"""
    result = dotplot(df['age'], bin=20)
    plt.close('all')
    return result

# ============================================
# ONE SHOT TESTS
# ============================================

def one_shot_test_simple():
    result = dotplot(df['age'])
    plt.close('all')
    assert result is None  # dotplot shows plot, returns None

def one_shot_test_grouped():
    result = dotplot(df['age'], by=df['sex'])
    plt.close('all')
    assert result is None

# ============================================
# R COMPARISON TESTS
# ============================================

def run_r_dotplot_simple():
    """Run R's epiDisplay::dotplot on age"""
    r_code = """
    suppressMessages(library(epiDisplay))
    data(Outbreak)
    df <- Outbreak
    
    # Save plot to file
    png('r_dotplot_simple.png', width=800, height=600)
    dotplot(df$age)
    dev.off()
    
    # Print summary stats for verification
    cat("R_Min:", min(df$age, na.rm=TRUE), "\\n")
    cat("R_Max:", max(df$age, na.rm=TRUE), "\\n")
    cat("R_N:", sum(!is.na(df$age)), "\\n")
    """

    print("\n============ R COMMAND (Simple) ============\n")
    print(r_code)

    result = subprocess.run(
        ["Rscript", "-e", r_code],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print(f"R stderr: {result.stderr}")
        raise RuntimeError(f"R error: {result.stderr}")

    return result.stdout

def run_r_dotplot_grouped():
    """Run R's epiDisplay::dotplot on age by sex"""
    r_code = """
    suppressMessages(library(epiDisplay))
    data(Outbreak)
    df <- Outbreak
    
    # Save plot to file
    png('r_dotplot_grouped.png', width=800, height=600)
    dotplot(df$age, by=df$sex)
    dev.off()
    
    # Print summary stats for verification
    cat("R_Min:", min(df$age, na.rm=TRUE), "\\n")
    cat("R_Max:", max(df$age, na.rm=TRUE), "\\n")
    cat("R_N:", sum(!is.na(df$age)), "\\n")
    cat("R_Groups:", length(unique(df$sex[!is.na(df$sex)])), "\\n")
    """

    print("\n============ R COMMAND (Grouped) ============\n")
    print(r_code)

    result = subprocess.run(
        ["Rscript", "-e", r_code],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print(f"R stderr: {result.stderr}")
        raise RuntimeError(f"R error: {result.stderr}")

    return result.stdout

def compare_py_r_dotplot_simple():
    """Compare Python and R dotplot outputs for simple case"""
    print("\n============ PYTHON COMMAND (Simple) ============\n")
    print("dotplot(df['age'])")

    # Python output - save to file
    plt.figure()
    dotplot(df['age'])
    plt.savefig('py_dotplot_simple.png')
    plt.close('all')

    # Calculate Python summary stats
    py_min = df['age'].min()
    py_max = df['age'].max()
    py_n = df['age'].notna().sum()

    # Print Python summary stats
    print("\n============ PYTHON STATS ============\n")
    print(f"Py_Min: {py_min}")
    print(f"Py_Max: {py_max}")
    print(f"Py_N: {py_n}")

    # R output
    r_output = run_r_dotplot_simple()

    print("\n============ R STATS ============\n")
    print(r_output)

    print("\n============ COMPARISON ============")
    print("Visual comparison: Check 'py_dotplot_simple.png' vs 'r_dotplot_simple.png'")
    print("Files generated for manual inspection.")
    
    # Parse R output with error handling
    try:
        r_lines = [line for line in r_output.strip().split('\n') if line.strip()]
        
        if len(r_lines) < 3:
            print(f"Warning: Expected 3 lines from R, got {len(r_lines)}")
            print(f"R output lines: {r_lines}")
            return False
        
        r_min = float(r_lines[0].split(':')[1].strip())
        r_max = float(r_lines[1].split(':')[1].strip())
        r_n = int(r_lines[2].split(':')[1].strip())
        
        # Compare stats
        print(f"\nPy_Min: {py_min} == R_Min: {r_min} ? {py_min == r_min}")
        print(f"Py_Max: {py_max} == R_Max: {r_max} ? {py_max == r_max}")
        print(f"Py_N: {py_n} == R_N: {r_n} ? {py_n == r_n}")
        
        stats_match = (py_min == r_min and py_max == r_max and py_n == r_n)
        print(f"\nStats Match: {stats_match}")
        
        return stats_match
        
    except (IndexError, ValueError) as e:
        print(f"Error parsing R output: {e}")
        print(f"R output was: {r_output}")
        return False

def compare_py_r_dotplot_grouped():
    """Compare Python and R dotplot outputs for grouped case"""
    print("\n============ PYTHON COMMAND (Grouped) ============\n")
    print("dotplot(df['age'], by=df['sex'])")

    # Python output - save to file
    plt.figure()
    dotplot(df['age'], by=df['sex'])
    plt.savefig('py_dotplot_grouped.png')
    plt.close('all')

    # Calculate Python summary stats
    py_min = df['age'].min()
    py_max = df['age'].max()
    py_n = df['age'].notna().sum()
    py_groups = df['sex'].nunique()

    # Print Python summary stats
    print("\n============ PYTHON STATS ============\n")
    print(f"Py_Min: {py_min}")
    print(f"Py_Max: {py_max}")
    print(f"Py_N: {py_n}")
    print(f"Py_Groups: {py_groups}")

    # R output
    r_output = run_r_dotplot_grouped()

    print("\n============ R STATS ============\n")
    print(r_output)

    print("\n============ COMPARISON ============")
    print("Visual comparison: Check 'py_dotplot_grouped.png' vs 'r_dotplot_grouped.png'")
    print("Files generated for manual inspection.")
    
    # Parse R output with error handling
    try:
        r_lines = [line for line in r_output.strip().split('\n') if line.strip()]
        
        if len(r_lines) < 4:
            print(f"Warning: Expected 4 lines from R, got {len(r_lines)}")
            print(f"R output lines: {r_lines}")
            return False
        
        r_min = float(r_lines[0].split(':')[1].strip())
        r_max = float(r_lines[1].split(':')[1].strip())
        r_n = int(r_lines[2].split(':')[1].strip())
        r_groups = int(r_lines[3].split(':')[1].strip())
        
        # Compare stats
        print(f"\nPy_Min: {py_min} == R_Min: {r_min} ? {py_min == r_min}")
        print(f"Py_Max: {py_max} == R_Max: {r_max} ? {py_max == r_max}")
        print(f"Py_N: {py_n} == R_N: {r_n} ? {py_n == r_n}")
        print(f"Py_Groups: {py_groups} == R_Groups: {r_groups} ? {py_groups == r_groups}")
        
        stats_match = (py_min == r_min and py_max == r_max and 
                       py_n == r_n and py_groups == r_groups)
        print(f"\nStats Match: {stats_match}")
        
        return stats_match
        
    except (IndexError, ValueError) as e:
        print(f"Error parsing R output: {e}")
        print(f"R output was: {r_output}")
        return False

# ============================================
# PYTEST FIXTURES AND TESTS
# ============================================

@pytest.fixture(scope="module")
def outbreak_data():
    return data("Outbreak")

def test_dotplot_simple(outbreak_data):
    """Test simple dotplot"""
    dotplot(outbreak_data['age'])
    plt.close('all')

def test_dotplot_grouped(outbreak_data):
    """Test grouped dotplot"""
    dotplot(outbreak_data['age'], by=outbreak_data['sex'])
    plt.close('all')

def test_dotplot_custom_colors(outbreak_data):
    """Test dotplot with custom colors"""
    dotplot(outbreak_data['age'], by=outbreak_data['sex'], 
            dot_col=['red', 'blue'])
    plt.close('all')

def test_dotplot_custom_bins(outbreak_data):
    """Test dotplot with custom bin count"""
    dotplot(outbreak_data['age'], bin=15)
    plt.close('all')

# ============================================
# MANUAL RUN
# ============================================

if __name__ == "__main__":
    print("Running dotplot tests...\n")
    
    # Smoke tests
    print("=== SMOKE TESTS ===")
    smoke_test_simple()
    print("✓ Simple dotplot smoke test passed")
    
    smoke_test_with_grouping()
    print("✓ Grouped dotplot smoke test passed")
    
    smoke_test_with_bins()
    print("✓ Custom bins dotplot smoke test passed")
    
    # Comparison tests
    print("\n=== COMPARISON TESTS ===")
    compare_py_r_dotplot_simple()
    print("\n")
    compare_py_r_dotplot_grouped()

"""
Example of ci_mean() using the Outbreak dataset.

author: Anna Kroening
reviewer: Cat Kim
category: example
"""

from pyepidisplay.data import data
from pyepidisplay.ci_mean import ci_mean, print_ci_mean

# Load dataset
df = data("Outbreak")

# Run ci_mean on the 'Age' column
# The function handles calculating the mean, SE, SD and CI internally.
result = ci_mean(df['Age'], ci=0.95)

# Print the results
print_ci_mean(result, ci=0.95)
"""
Example of ci_prop() using the Outbreak dataset.

author: Anna Kroening
reviewer: Cat Kim
category: example
"""

from pyepidisplay.data import data
from pyepidisplay.ci_prop import ci_prop, print_ci_prop

# Load dataset
df = data("Outbreak")

# Calculate CI for proportion of people who ate beef curry
result = ci_prop(df['beefcurry'], ci=0.95)

# Print the results
print_ci_prop(result, ci=0.95)

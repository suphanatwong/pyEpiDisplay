# Translating R Packages into Python: A Pilot Project of epiDisplay
### Team Members:
* Anna Kroening (MSIM)
* Cat Kim (BIME)
* Jiayi Ding (BIME)
* Marthin Mandig (BIME)
* Suphanat Wongsanuphat (BIME)

## Project Overview:
Epidemiological data analysis increasingly needs to handle novel data sources such as imaging, text, signal, and genomic data, along with machine learning approaches. Some of these capabilities are limited in R but are rapidly expanding in Python. As a result, many epidemiologists are transitioning to Python; however, Python currently has limited epidemiological data analysis packages. We will (but not limited to): 
1) Develop a Python package that translates the core functionalities of the R package EpiDisplay.
2) Learn how to translate an existing R package into Python, including understanding differences in syntax, data structures, and library ecosystems between R and Python.

The intended audience of our project ranges from epidemiology students to experts interested in performing data analysis and visualization tasks in Python.

To install the package, 

## Audience
 - Students & Public Health Trainees
   
Need: Quick, accessible functions for core analytical tasks in a Python environment.

Value: Provides pre-built, easy-to-use functions for essential calculations: ci_prop(), ci_mean(), crosstab_function(), and summ_function(). This accelerates the learning curve by focusing on interpretation rather than complex coding.

- R-to-Python Transitioners
  
Need: Direct, familiar translations of key R functions to maintain workflow continuity during the transition.

Value: Offers equivalent syntax for displaying regression models (logistic_display(), regress_display()) and manipulating data (table_stack()), reducing the overhead of adopting a new language for common epidemiological work.

- Experienced Epidemiologists & Data Scientist

Need: A reliable, standardized package to integrate classic metrics into complex, novel data workflows (e.g., genomics, imaging, text analysis).

Value: Serves as the essential epidemiological core within the Python ecosystem, allowing experts to seamlessly combine robust statistical measures (e.g., ORs from logistic_display()) with advanced machine learning libraries, using data() to load test sets easily.

## Translated Functionalities
* logistic_display()
  * author: Cat Kim
* regress_display()
  * author: Cat Kim
* crosstab_function
  * author: Marthin Mandig
* summ_function
  * author: Marthin Mandig
* data
  * author: Suphanat (AT) Wongsanuphat
* table_stack
  * author: Suphanat (AT) Wongsanuphat
* ci_prop
  * author: Anna Kroening
* ci_mean
  * author: Anna Kroening

## Test Functions
* test_logistic_display()
  * author: Cat Kim
* test_regress_display()
  * author: Cat Kim
* test_crosstab
  * author: Marthin Mandig
* test_summ
  * author: Marthin Mandig
* test_ci_mean
  * author: Anna Kroening
* test_ci_prop
  * author: Anna Kroening
* test_table_stack
  * author: Suphanat (AT) Wongsanuphat
* test_data()
  * author: Suphanat (AT) Wongsanuphat

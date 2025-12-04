# Functional Specification

## Background
In the field of epidemiology, data analysis and visualization is critical for processing and presenting data that can inform interventions and improve health outcomes, and epiDisplay is a computational tool and R package that can be helpful in epidemiological data exploration and visualization. However, epidemiologists are increasingly pivoting away from R as R can have limited capabilities that cannot handle novel data sources like imaging, text, signal, and genomic data. Additionally, though they are trying to transition into using Python, Python has limited epidemiological data analysis packages. 

Our project goal is to translate the epiDisplay R package into Python and  understand differences in syntax, data structures, and library ecosystems between R and Python. Ultimately, we will develop a Python package that translates core functionalities of the R package EpiDisplay.

## User profile. Who uses the system. What they know about the domain and computing (e.g., can browse the web, can program in Python)

## Data sources
### Outbreak Dataset: Thailand 1990 Food Poisoning Outbreak
The foundation of our project is the Outbreak dataset, which originates from a critical public health investigation in Supan Buri Province, Thailand, on August 25, 1990. The incident involved an acute gastrointestinal illness affecting attendees of a national handicapped sports day held at a provincial college.

#### Investigation Details and Findings:
* Scope: An epidemiological team was deployed to determine the cause of the outbreak, involving interviews with all 1,210 individuals present at the event, alongside environmental surveys, analysis of food samples, and swabs collected from food handlers.
* Case Definition: A person was formally identified as a case if they had consumed any dinner food item and subsequently experienced a combination of symptoms, specifically vomiting, nausea, abdominal pain, and diarrhea.
* Attack Rate: Out of 1,094 persons, 485 met the case definition, resulting in a high overall attack rate of 43%. The most frequently reported symptoms among cases were nausea (93%), vomiting (88%), and abdominal pain (81.5%). The mean incubation period for the illness was determined to be 3.20 hours.
* Hypothesis Testing and Source Identification: Initial descriptive analysis identified three of the four food items consumed as having a statistically significant association with illness. However, the analysis focused heavily on the eclairs, which were prepared the night before and held at room temperature for over 12 hours prior to serving.
* Analytical Benchmark: A definitive statistical evaluation using unconditional logistic regression confirmed that only the consumption of eclairs remained a statistically significant risk factor, yielding a high adjusted Relative Risk (RR) of 11.96 (95% Confidence Interval: 9-22).
* Laboratory Confirmation: Microbiological analysis strongly supported the epidemiological findings. Laboratory examination of the eclairs indicated heavy growth of Staphylococcus aureus (producing toxins A and C) and Bacillus cereus. While nasal swabs from healthy food handlers identified similar bacteria, the phage types differed from those found in the implicated food, confirming the contaminated eclairs as the vehicle for the outbreak.

## Use cases. Describing at least two use cases. For each, describe: (a) the objective of the user interaction (e.g., withdraw money from an ATM); and (b) the expected interactions between the user and your system.


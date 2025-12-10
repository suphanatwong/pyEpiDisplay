# Functional Specification

## Background
In the field of epidemiology, data analysis and visualization is critical for processing and presenting data that can inform interventions and improve health outcomes, and epiDisplay is a computational tool and R package that can be helpful in epidemiological data exploration and visualization. However, epidemiologists are increasingly pivoting away from R as R can have limited capabilities that cannot handle novel data sources like imaging, text, signal, and genomic data. Additionally, though they are trying to transition into using Python, Python has limited epidemiological data analysis packages. 

Our project goal is to translate the epiDisplay R package into Python and  understand differences in syntax, data structures, and library ecosystems between R and Python. Ultimately, we will develop a Python package that translates core functionalities of the R package EpiDisplay.

## User profile. Who uses the system. What they know about the domain and computing (e.g., can browse the web, can program in Python)

Henry is an epidemiology M.S. student with no prior background in R but with lots of experience in Python. 
Priorities:
Become more familiar with R for epidemiology applications, especially because almost all of his coursework is taught with R. 
Wants a python version of epiDisplay that is intuitive, easy to use, as well as easy to understand the documentation of as he still wants to gain exposure in R.


James is a software developer and wants to use functions for R but only works in Python. 
Priorities:
Doesn't care too much about the epi data, just wants to add some of the functions in converting R to python in his packages. 
Doesn't have much time to add it. 


## Primary Built-in Data source (Use for testing)
### Outbreak Dataset: Thailand 1990 Food Poisoning Outbreak
We wil be testing our functions using epiDisplay's Outbreak dataset, which originates from a critical public health investigation in Supan Buri Province, Thailand, on August 25, 1990. The incident involved an acute gastrointestinal illness affecting attendees of a national handicapped sports day held at a provincial college.

#### Investigation Details and Findings:
* Scope: An epidemiological team was deployed to determine the cause of the outbreak, involving interviews with all 1,210 individuals present at the event, alongside environmental surveys, analysis of food samples, and swabs collected from food handlers.
* Case Definition: A person was formally identified as a case if they had consumed any dinner food item and subsequently experienced a combination of symptoms, specifically vomiting, nausea, abdominal pain, and diarrhea.
* Attack Rate: Out of 1,094 persons, 485 met the case definition, resulting in a high overall attack rate of 43%. The most frequently reported symptoms among cases were nausea (93%), vomiting (88%), and abdominal pain (81.5%). The mean incubation period for the illness was determined to be 3.20 hours.
* Hypothesis Testing and Source Identification: Initial descriptive analysis identified three of the four food items consumed as having a statistically significant association with illness. However, the analysis focused heavily on the eclairs, which were prepared the night before and held at room temperature for over 12 hours prior to serving.
* Analytical Benchmark: A definitive statistical evaluation using unconditional logistic regression confirmed that only the consumption of eclairs remained a statistically significant risk factor, yielding a high adjusted Relative Risk (RR) of 11.96 (95% Confidence Interval: 9-22).
* Laboratory Confirmation: Microbiological analysis strongly supported the epidemiological findings. Laboratory examination of the eclairs indicated heavy growth of Staphylococcus aureus (producing toxins A and C) and Bacillus cereus. While nasal swabs from healthy food handlers identified similar bacteria, the phage types differed from those found in the implicated food, confirming the contaminated eclairs as the vehicle for the outbreak.

**Citation**: 
Thaikruea L, Pataraarechachai J, Savanpunyalert P, Naluponjiragul U. An unusual outbreak of food poisoning. Southeast Asian J Trop Med Public Health. 1995;26(1):78-85.


## Other Built-in Data Sources

* Age at marriage (Marryage): A dataset containing data on the age at first marriage of attendants at a workshop in 1997. It has 27 observations on 7 variables.
* ANC data (ANCdata): A dataset recording high-risk pregnant women in a trial on new versus old ANC methods in two clinics, with the outcome being perinatal mortality. It contains 755 observations on 3 variables.
* Attitudes dataset (Attitudes): Data from an attitude survey among hospital staff, focused on attitudes related to services. It includes 136 observations on 7 variables.
* Blood pressure (BP): Records of 100 adults from a small cross-sectional survey in 2001, investigating blood pressure and its determinants in a community.
* Cancer survival (Compaq): Data used for checking the survival difference between cancer patients in private and public hospitals. It includes 1064 observations on 7 variables.
* Ectopic pregnancy (Ectopic): Data from a case-control study investigating history of abortion as a risk factor for ectopic pregnancy. It has 723 observations on 4 variables and includes a case series and two control groups.
* Hookworm 1993 (HW93): Data from a study on hookworm prevalence and intensity in 1993.
* Hookworm and blood loss: Listed as a dataset in the documentation content.
* IUD trial admission data (IudAdmit): Data concerning the admission of cases for IUD (Intrauterine Device) trials.
* IUD trial discontinuation data (IudDiscontinue): Data on the discontinuation of IUD trial cases.
* IUD trial follow-up data (IudFollowup): Data on the follow-up cases of IUD trials.
* Oswego: A dataset derived from an outbreak of food poisoning that occurred in the US.
* Sleepiness: Listed as a dataset in the documentation content.
* Timing exercise (Timing): A dataset used for exercises, containing variables related to the timing of daily activities like hour/minute of going to bed, waking up, and arrival at a workshop.
* Tooth decay (Decay): A dataset on tooth decay and mutan streptococci, examining the relationship between the bacteria and the presence of decayed teeth. It contains 436 observations on 2 variables.
* Voluntary counselling and testing (VCT): A dataset on attitudes toward VCT, containing records of 200 women working at a tourist destination community.
* Xerophthalmia and respiratory infection: Data from an Indonesian study on vitamin A deficiency and the risk of respiratory infection, adopted from Diggle et al., Analysis of Longitudinal Data.

## Use cases. Describing at least two use cases. For each, describe: (a) the objective of the user interaction (e.g., withdraw money from an ATM); and (b) the expected interactions between the user and your system.
Import external dataset 

Import build-in dataset

Display dataset and Pivot table with multiple variables

Descriptive analytics
Frequency, Count, Sum
Central of Tendency: Mean, Median
Measure of Variation: SD, IQR, …
Check for outliers

Data Visualization
Exploratory Data Visualization
Publication/ Report Data Visualization

Inferential Analytics 
Logistic regression with OR and 95% confidence interval
Linear regression











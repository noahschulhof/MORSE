# MORSE_data
This part of the `MORSE` repository contains the input files (with corresponding links), data, and scripts needed to reproduce the results in the `MORSE` manuscript. The tables below indicate which script produces each figure. The `MadHitter` input files are in separate repositories, as they have been used in the original `MadHitter` [paper](https://www.nature.com/articles/s41467-022-29154-2), and have been made available for other cancer-related studies.

## CPLEX_testing
This folder contains an implementation/evaluation of the CPLEX [`populate`](https://www.ibm.com/docs/en/icos/22.1.1?topic=pool-algorithm-populate-procedure) method (for enumerating all optima of an ILP) on the 20 `MIPLIB` instances tested. `solve_new.ipynb` provides a walkthrough of this process.


## MadHitter

### Input Files
|Repository Link|Datasets|
|---------------|--------|
|https://ftp.ncbi.nlm.nih.gov/pub/catSMA/MadHitter_data/|`EMTAB6149`, `GSE103322`, `GSE70630`, `GSE84465`, `GSE89567`|
|https://ftp.ncbi.nlm.nih.gov/pub/catSMA/Additional_MadHitter_input_files/|`GSE117570`, `GSE127465`, `GSE147082`, `GSE162708`|

### Data
|Folder|Description|
|------|-----------|
|`sols`|Contains the gene solution sets for MadHitter instances optimized with and without MORSE.| 

### Scripts
|Figure(s)|Script|
|---------|------|
|10-11     |`num_sol.qmd`|
|12       |`shannon.qmd`|

To execute these scripts, open `MadHitter.Rproj` in `Rstudio` and select the desired script from the right panel.


## MIPLIB

### Input Files
- `mps_files` contains the raw input files (MIPLIB instances) on which testing was performed.

### Data
|Folder|Description|
|------|-----------|
|`obj_vals`|Contains the optimized objective value for each instance, as well as the objective value for each run for each instance optimized with MORSE. 
|`unique_results`| Contains the values of post-optimization objective function variables for instances optimized with and without MORSE.|
|`hamming_results`| Contains average pairwise Hamming distances between the solution vectors in `unique_results` derived using the three solution pool ordering methods described in the manuscript.|


### Scripts
|Figure(s)|Script|
|---------|------|
|1-3      |`hamming.qmd`|
|4-5      |`hamming_split.qmd`|
|6-8      |`unique_sols.qmd`|
|9        |`unique_tabular.qmd`|
|13-14    |`shannon.qmd`|
|15       |`obj.qmd`|

To execute these scripts, open `MIPLIB.Rproj` in `Rstudio` and select the desired script from the right panel.
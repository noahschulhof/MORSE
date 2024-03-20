# MORSE_data
This part of the `MORSE` repository contains the input files, links to input files, data, and scripts needed to reproduce the results in the `MORSE` manuscript. The tables below indicate which script produces each figure. The `MadHitter` input files are in separate repositories, as they have been used in the original `MadHitter` [paper](https://www.nature.com/articles/s41467-022-29154-2), and have been made available for other cancer-related studies.

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
|9-10     |`num_sol.qmd`|
|11       |`shannon.qmd`|

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
|4        |`hamming_split.qmd`|
|5-7      |`unique_sols.qmd`|
|8        |`unique_tabular.qmd`|
|12-13    |`shannon.qmd`|
|14       |`obj.qmd`|

To execute these scripts, open `MIPLIB.Rproj` in `Rstudio` and select the desired script from the right panel.
# MORSE
Author: [Noah Schulhof](mailto:nschulhof@u.northwestern.edu) with guidance from Pattara Sukprasert, Alejandro Schaffer, Samir Khuller, and Eytan Ruppin

Integer Linear Program (ILPs) and Mixed Integer Linear Programs (MILPs) are optimization problems in which a linear objective function is minimized or maximized while satisfying a set of linear constraints. All variables in ILPs are constrained to only take on integer values, while only some variables in MIPs must be integral. ILPs and MILPs often have multiple distinct optimal solutions, yet many optimization solvers struggle to efficiently explore the space of optima, returning certain solutions at disproportionately high frequencies. In the present work, we introduce `MORSE` (Multiple Optima via Random Sampling and careful choice of the parameter Epsilon), a parallelizable algorithm to efficiently generate multiple optima for ILPs and MILPs.

Paramount to our method is the selection of a small value $ε$ that determines the maximum value by which we may vary the objective function coefficients, as we explain with the following example. Consider the following instance: maximizing the expression $x+y$ subject to the constraints $x,y≤2$ and $x+y≤3.5$, $x,y∈Z$. Suppose we choose $ε=0.01$. Next, we randomly generate a perturbation vector of length two (equal to the number of coefficients in the objective function) whose entries $v_1, v_2 \stackrel{\text{i.i.d.}}{\sim} \mathcal{U}(1-ε, 1+ε)$. An example of such a perturbation vector is $[0.99864, 1.00142]$. We then map the vector entries to the coefficients in the objective function, which becomes $0.99864x+1.00142y$. Without modifying the constraints, we solve the resulting instance and obtain the optimum $\{ x=1, y=2 \}$. On another execution of `MORSE`, with the same value for $ε$, suppose we randomly generate the perturbation vector $[1.00045, 0.99312]$. After mapping the vector entries to the coefficients in the objective function, and solving the instance, we obtain the optimum $\{ x=2, y=1 \}$. By executing two independent runs of `MORSE`, we can find the two distinct optima for the provided instance. To generalize this notion, for any instance with $n>1$ distinct optima, we aim to find all distinct optima in $r≥n$ independent `MORSE` runs.  

If $ε$ is sufficiently small, we can prove that each optimum of the perturbed instance is an optimum of the original instance. By executing several `MORSE` runs in parallel, and aggregating the solutions found, one can explore the space of optima to any ILP or MILP.


## Prerequisites

- [`Python`](https://www.python.org/downloads/release/python-3116/) v3.11.6+
- [`Gurobi`](https://www.gurobi.com/solutions/gurobi-optimizer/) & [`gurobipy`](https://pypi.org/project/gurobipy/) v10.0.3+
- [`pandas`](https://pypi.org/project/pandas/) v2.1.2+

### Conda Installation of Gurobi
The following command installs `Gurobi` (version 11.0.0) and `gurobipy`
```bash
$ conda install -c gurobi gurobi
```
`pandas` comes pre-installed with the [Anaconda](https://docs.anaconda.com/free/anaconda/index.html) Distribution. Users running the [Miniconda](https://docs.anaconda.com/free/miniconda/) Distribution should execute the command:
```bash
$ conda install -c conda-forge pandas
```

### Obtaining a Gurobi License

To use the Gurobi Optimizer, a valid license is required. A guide to the available licenses can be found [here](https://support.gurobi.com/hc/en-us/articles/12684663118993-How-do-I-obtain-a-Gurobi-license).


## MORSE code files
MORSE includes four code files in python. Three are top-level scripts and one has helper functions.
solve.py -- solve one instance one time
parallel.py -- set-up parallel runs of solve.py that are for the same instance but using different pertubation vectors
agg.py -- aggregate solutions to collect summary data
morse.py -- helper functions

Instructions for using solve.py, parallel.py, and agg.py can be found below.

## Usage
```bash
$ python3 solve.py --instance_filepath instance.mps
```
- To write solutions to csv file, simply supply a filepath to the intended solutions file
```bash
$ python3 solve.py --instance_filepath instance.mps --sol_filepath solutions.csv
```

### Arguments to solve.py
For solve.py and the other programs in MORSE each command-line argument has a one-letter version preceded by a single-dash (good for compact command lines) and an equivalent long form preceded by two dashes (good for remembering the purpose of each argument).

`-i, --instance_filepath` filepath to instance (in .mps or .mps.gz format)  
`-s, --sol_filepath` filepath to solutions file [default=None]  
`-r, --random_seed` seed for Gurobi and random weights (if perturbation vector is not supplied) [default=None]  
`-p, --perturbation_vector` perturbation vector, passed as a quote-enclosed iterable [default=None]

### Example Run
```bash
$ wget https://miplib2010.zib.de/miplib3/miplib3/p0033.mps.gz
$ python3 solve.py --instance_filepath p0033.mps.gz --sol_filepath p0033_sols.csv
```

p0033..mps.gz is one of the problem instances listed below in the subsection Sample MPS Files.

### Example Output
Solutions are written in csv format to the filepath supplied to `--sol_filepath`; If no value is supplied, solutions will not be stored. Solution files contain the following fields:
- `VarName`: names of variables in the objective function
- `Value`: values of variables post-optimization  
- `Weight` multiplicative perturbations mapped to variables' coefficients in the objective function  

Executing the example run should yield a solution file at filepath `p0033_sols.csv` that resembles the following (`Value` and `Weight` values will naturally differ between runs):

|VarName|Value|Weight            |
|-------|-----|------------------|
|C157   |1.0  |0.9999736987837438|
|C158   |-0.0 |1.0000201635866284|
|C159   |-0.0 |1.0000600005644749|
|...    |...    |...|
|C187   |0.0  |1.0000163156917197|
|C188   |-0.0 |0.9999720270642298|
|C189   |0.0  |1.0000057960341204|

Full sample output can be found [here](https://gist.github.com/noahschulhof/4ee02a64ffcc37de2f88e92f02b79319).


## Parallelization
Central to MORSE is the ability to execute several runs in parallel. `parallel.py` can be used to generate parallelizable bash scripts. An example run is as follows:

```bash
$ python3 parallel.py \
    --script_filepath p0033_parallel.sh \
    --instance_filepath p0033.mps.gz \
    --num_runs 5 \
    --sol_filepath p0033_sols.csv
```

### Arguments to parallel.py
`-f, --script_filepath` filepath to parallelized script  
`-i, --instance_filepath` filepath to instance (in .mps or .mps.gz format)  
`-n, --num_runs` number of runs to be executed  
`-s, --sol_filepath` base filepath to solutions file [default=None]  
`-e, --executable` name of the python executable file [default=python3]  
`-r, --random_seeds` quote-enclosed iterable of random seeds to be used in individual runs [default=None]  
`-p, --perturbation_filepath` filepath to csv file with one perturbation vector per line [default=None]

### Example Output
The above command will yield the following script at the filepath `p0033_parallel.sh`
```bash
python3 solve.py -i p0033.mps.gz -s p0033_sols_1.csv  
python3 solve.py -i p0033.mps.gz -s p0033_sols_2.csv  
python3 solve.py -i p0033.mps.gz -s p0033_sols_3.csv  
python3 solve.py -i p0033.mps.gz -s p0033_sols_4.csv  
python3 solve.py -i p0033.mps.gz -s p0033_sols_5.csv
```
This script (or variations thereof) can subsequently be executed with a line-level parallelism tool of the user's choosing. We tested scripts produced by `parallel.py` on two compute farms that use the `SLURM` (Simple Linux Utility for Resource Management) formalism for job scheduling: [Biowulf](https://hpc.nih.gov/systems/) at the National Institutes of Health and [Quest](https://www.it.northwestern.edu/departments/it-services-support/research/computing/quest/) at Northwestern University.


## Aggregating Solutions
After executing runs in parallel, the solutions found can be aggregated into a single file with the script `agg.py`.
### Arguments to agg.py
`-m, --match` string to match solution files  
`-s, --sols_dir` filepath to solutions directory (defaults to working directory)  
`-o, --output_filepath` filepath to output aggregated solutions file  
`-c, --cleanup` flag to cleanup (delete) individual solution files  
`-v, --var_names` flag to store variable names in aggregated solutions file

### Example Run

After executing the script `p0033_parallel.csv` (generated in the previous section), the following command will aggregate all solution files (with variable names stored) into the file `p0033.csv` and remove the individual solution files:

```bash
$ python3 agg.py \
    --match p0033_sols \
    --output_filepath p0033_agg.csv \
    --cleanup \
    --var_names
```

### Example Output

The above command will yield an aggregated solution file at the filepath `p0033_agg.csv` that resembles the following (variable values will naturally differ between runs):
|C157|C158|C159|...|C181|C182|C183|C184|C185|C186|C187|C188|C189|
|----|----|----|----|----|----|----|----|----|----|----|----|----|
|1.0 |-0.0|-0.0|...|0.0 |1.0 |1.0 |1.0 |1.0 |1.0 |0.0 |-0.0|0.0 |
|1.0 |0.0 |-0.0|...|1.0 |1.0 |1.0 |1.0 |1.0 |1.0 |-0.0|-0.0|0.0 |
|1.0 |-0.0|-0.0|...|0.0 |1.0 |1.0 |1.0 |1.0 |1.0 |-0.0|-0.0|0.0 |
|1.0 |0.0 |0.0 |...|1.0 |1.0 |1.0 |1.0 |1.0 |1.0 |0.0 |-0.0|0.0 |
|1.0 |-0.0|-0.0|...|1.0 |1.0 |1.0 |1.0 |1.0 |1.0 |-0.0|-0.0|0.0 |

Full sample output can be found [here](https://gist.github.com/noahschulhof/48322e363a4ae97849a32a044cb0815d).


## Sample MPS Files
The directory `mps_files` contains 20 Mathematical Programming System (MPS) files, each of which is an ILP or MILP instance for which MORSE has been verified to find multiple distinct optima. These instances were retrieved from the Mixed Integer Programming Library ([MIPLIB](https://miplib.zib.de/)) versions 2.0 - 6.0.

The table below gives the full list of instances, the most recent MIPLIB version in which each instance appeared, and the number of distinct optima (enumerated using the `PySCIPOpt` [`count`](https://scipopt.github.io/PySCIPOpt/docs/html/classpyscipopt_1_1scip_1_1Model.html#a5eb880efb244834d39c062297388252b) function). Distinct optima counts marked with ≥ give the number of optima enumerated by count within a 24-hour runtime; if there is no ≥, then enumeration was fully completed in runtime <24 hours and hence the number of distinct optimal solutions is exact.

|MIPLIB instance|Most recent MIPLIB version|Number of distinct optima|
|---------------|--------------------------|-------------------------|
|`set1al`         | 2.0                      | 2                       |
|`set1cl`         | 2.0                      | 2                       |
|`p0201`          | 3.0                      | 4                      |
|`bell3a`         | 3.0                      | 5                       |
|`mod008`         | 3.0                      | 6                      |
|`p0033`          | 3.0                      | 9                      |
|`bell5`          | 3.0                      | 16                      |
|`lp41`           | 2.0                      | 24                      |
|`vpm2`           | 4.0                      | 33                      |
|`stein9`         | 2.0                      | 54                      |
|`stein45`        | 3.0                      | 70                     |
|`supportcase14`  | 6.0                      | 256                     |
|`supportcase16`  | 6.0                      | 256                     |
|`stein15`        | 3.0                      | 315                     |
|`stein27`        | 3.0                      | 2106                   |
|`harp2`          | 5.0                      | ≥1                      |
|`pigeon-10`      | 6.0                      | ≥6574                   |
|`app2-2`         | 6.0                      | ≥41819                  |
|`noswot`         | 6.0                      | ≥48776                  |
|`vpm1`           | 3.0                      | ≥86186                  |
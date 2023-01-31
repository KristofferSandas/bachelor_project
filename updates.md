# 31 jan 2023  - nanopore sim & initial RT sketch

#### On branch RTsim_GZ 


### nanopore real time simulator
The python function *rt_sim_testdata* copies one compressed fastq file at a time from the test data "fastq/pass" folder at a specified time interval. 
This function is run in a separate terminal and simulates the fastq batch files produced by the nanopore. The files are copied to a folder called 
"nanopore_output". This script runs in the background, separate from the pipeline.

### master py script checks output dir
The py script *batchSenser_master.py* is run in a terminal or from an IDE. It checks the simulated "nanopore_output" dir every t seconds. If new files
from the nanopore are detected, the script sends them through a snakemake workflow that ungzips them and sends them on to kraken2 classification.
Once each batch file is classififed, the results are added to a cumulative list of the total kraken2 results.

### problems
**Directory strucuture:** how will it be organized? What should be specifiable, what should be hardcoded?

**Snakemake run from python:** os.system() or snake API? 

**Snakemake Snakefile location:** snakemake reads "Snakefile"? How to do multiple workflows? New directories?

**Snakemake:** can I work beginning -> end in snakemake? Every time a file is sensed by the senser script it sends the file to ungzipping -> kraken2
-> append to cumulative list
  
**Snakemake parallell/waiting list:** how can I trigger a function/workflow from python wich runs detached from the master script? Meaning the master
script can keep sensing for files and just send the new files off to the workflow.
  
**Kraken2 database load:** even with minikraken 8gb database, loading time is bottleneck. Persistant database?

**Kraken2 GTDB flextaxD:** how long will it take to load a 60gb database? Need to go through database construction.

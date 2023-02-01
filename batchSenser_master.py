#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 29 17:20:46 2023

@author: bioinf


Checks the nanopore output folder every t seconds. If any new fastq.gz files have appeared,
they are sent to a snakemake workflow where they are unzipped and moved to another folder, 
and then run through kraken2. The kraken2 results are then appended to a cumulative list
containing the total kraken2 classification results. 

A temporary list with the files that have already been processed is kept in a temp file, 
so the script knows where to begin if the process is started again.

"""

import time
import os
#from datetime import datetime

def batchSenser(input_folder, # simulated nanopore output dir
                temp_folder = "temp/", # for temporary list file
                kraken_cumul_folder = "kraken_cumul_1/", # total kraken results kept in cumulative list here
                t = 3*60): # 3 min
    
    os.chdir("/home/bioinf/test_workflow_1/") # moves to working dir, to find Snakefile
    
    if not os.path.exists(temp_folder): # creates temp folder if it doesnt exsist
        os.mkdir(temp_folder)
    
    #timepoint = datetime.now()
    #dat = timepoint.date()
    #tim = str(timepoint.time())[:8]
    #tim = tim.replace(":", ".")
    #kraken_cumul_folder = "kraken_cumulative_" + str(dat) + "_" + tim + "/"
    if not os.path.exists(kraken_cumul_folder): # creates dir for kraken total results
        os.mkdir(kraken_cumul_folder) 
    
    # creates file for total kraken results if one does not exist already
    if not os.path.isfile(kraken_cumul_folder + "kraken_cumul_list.kraken2"):
        os.system("touch " + kraken_cumul_folder + "kraken_cumul_list.kraken2") # bash command: acceptable?
    
    # if there is a temp file from a previously started and aborted run, it is loaded here
    cumul_list = []
    if os.path.exists(temp_folder + "temp_cumul_list"):
        with open(temp_folder + "temp_cumul_list") as tempF:
            for line in tempF:
                line = line.rstrip()
                cumul_list.append(line)
        os.remove(temp_folder + "temp_cumul_list")
    print("current cumulative list:\n", cumul_list) # just for debugging/following script flow
    
    # endless loop checking nanopore_output dir every t seconds
    while True:
        try:
            time.sleep(t)
            print("\npinging nanopore_output")
            new_list = os.listdir(input_folder) # all files added to a list
            for i in new_list:
                if i not in cumul_list: # any new files sent to processing
                    bash_snakemake = "snakemake --cores 1 kraken_results/" + str(i)[:-9] + ".kraken2"
                    # snakemake workflow ungzips and sends to kraken
                    os.system(bash_snakemake)
                    bash_appendKraken = "cat kraken_results/" + str(i)[:-9] + ".kraken2 >> " + kraken_cumul_folder + "kraken_cumul_list.kraken2" 
                    # new kraken batch file appended to total results cumulative list
                    os.system(bash_appendKraken)
                    cumul_list.append(i)
                    print("\niteration complete")
                    print("\ncumulative list after iteration:", cumul_list)
            
        except KeyboardInterrupt: # if user aborts the process, completed files are stored in temp file
            print("interrupted")
            with open(temp_folder + "temp_cumul_list", 'w') as f:
                f.write('\n'.join(cumul_list))
            break
        
batchSenser(t = 5,
            input_folder = "/home/bioinf/test_workflow_1/nanopore_output/")
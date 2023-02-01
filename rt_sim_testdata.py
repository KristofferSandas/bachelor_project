#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 29 14:58:54 2023

@author: bioinf

A real time nanopore simulator made specifically to be used with the Nanopore test data from FOI.
The fastq files from the nanopore  test run are copied one at a time at a specific time interval
to a simulated output folder to mimic the sequential output of batch files from the nanopore.

A file is copied every t seconds (min_delay =< t =< max_delay).

"""

import os
import random
import time
import shutil

def rt_sim_testdata(input_folder, # where the original fastq.gz files are located
                    output_folder, # where the files are copied to: the simulated nanopore output dir
                    min_delay = 60*3, # 3 min
                    max_delay = 60*5, # 5 min
                    del_output_on_abort = False): # copied files are automatically removed upon user abort
    
    if not os.path.exists(output_folder): # creates the output dir if needed
        os.mkdir(output_folder)
        
    file_list = os.listdir(input_folder) # list all the files in the fastq/pass nanopore data dir
    #print(file_list, '\n')
    
    # sort the list
    file_list = sorted(file_list)
    #print(file_list, '\n')
    new_file_list = []
    #print(new_file_list, '\n')
    new_file_list.append(file_list[0])
    #print(new_file_list, '\n')
    for i in file_list[11:20]:
        new_file_list.append(i)
    #print(new_file_list, '\n')
    for i in file_list[1:11]:
        new_file_list.append(i)
    #print(new_file_list)
    
    try:
        for i in new_file_list: # for each fastq.gz file
            t = random.randint(min_delay, max_delay) # wait t seconds between files
            time.sleep(t)
            shutil.copy(input_folder + i, output_folder + i) # copy the file to the simulated nanopore dir
            print(i + " copied")
    except KeyboardInterrupt: # if user aborts the process, move out of the working dir
        print('\n----- aborted by user -----')
        if del_output_on_abort: # delete copied files if True
            print('----- removing output dir -----')
            shutil.rmtree(output_folder)
        
# call function
rt_sim_testdata(input_folder = "/home/bioinf/foi_test_data/fastq/pass/", 
                output_folder = "/home/bioinf/test_workflow_1/nanopore_output/",
                min_delay = 10,
                max_delay = 20,
                del_output_on_abort = False)
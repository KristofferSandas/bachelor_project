# -*- coding: utf-8 -*-
"""
Created on Thu Jan 26 13:39:50 2023

@author: krist

rt_sim function:

Produces a simulated batch file in fastq format at a random time interval
between min_delay and max_delay (seconds).

Each batch file contains n+1 sequences from the input file. n is a number between
min_nr and max_nr.

An output folder is created where the batch files are placed. There is an option
to chose to delete the created output folder upon user ending the process.
"""

from Bio import SeqIO
import random
import time
from datetime import datetime
import os
import shutil

def rt_sim(input_file, 
           output_folder = "output_folder", 
           min_delay = 60*3, # 3 min
           max_delay = 60*5, # 5 min
           min_nr = 5, 
           max_nr = 15,
           del_output_on_abort = False):

    # read in the data
    seq_list = []
    for record in SeqIO.parse(input_file, "fastq"):
        seq_list.append(record)
        
    #create and move to an output dir
    if not os.path.exists(output_folder):
        os.mkdir(output_folder)
    #print(output_folder, "created")
    os.chdir(output_folder)
    
    try:    
        # timed fastq producer
        i = 0
        j = 1
        while i < len(seq_list):
            #print(i)
            t = random.randint(min_delay, max_delay)
            time.sleep(t)
            n = random.randint(min_nr, max_nr)
            #print(seq_list[i:i+n])
            timepoint = datetime.now()
            dat = timepoint.date()
            tim = str(timepoint.time())[:8]
            tim = tim.replace(":", ".")
            output_name = "batch_" + str(j) + "_" + str(dat) + "_" + tim + ".fastq"
            SeqIO.write(seq_list[i:i+n], output_name, "fastq")
            print(output_name, "produced")
            j += 1
            i += n
            
        # change back from the output dir
        os.chdir('..')
    # if interrupted by user:
    except KeyboardInterrupt:
        print('\n----- aborted by user. moving out from output dir -----')
        os.chdir('..')
        if del_output_on_abort:
            print('----- removing output dir -----')
            shutil.rmtree(output_folder)
            
"""
rt_sim(input_file = "SRR21053861.fastq",
       min_delay = 5,
       max_delay = 10,
       del_output_on_abort = False
       )
"""


#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

# output folder location:
output_folder = "/projects/0/wtrcycle/users/edwin/edwin/hyperhydro_november_2015/RhineMeuse/05min/code__a__"

# starting and last run codes
start_code = 0
end_code = 624

# number of process within a loop
n_process = 36

# initializing some counters
i_code = start_code
start_loop = start_code

while start_loop < (end_code + 1):
   
   # initiate command lines
   cmd = ''
   
   # starting and end codes for this loop
   start_loop = i_code
   end_loop   = max(start_loop, i_code + n_process -1)
   end_loop   = min(end_loop, end_code)
   end_loop   = max(start_loop, end_loop)
   
   # generating jobs for this loop
   for i_code in range(start_loop, end_loop + 1, 1):
   
      cmd += "python 0_main_analyze_discharge.py " + str(output_folder) + str(i_code)
      cmd = cmd+" & "
      i_code = i_code + 1
   
   # don't foget to add the following line
   cmd = cmd + "wait"       
   
   # execute the jobs
   print cmd
   os.system(cmd)
   
   # starting loop for the next loope
   start_loop = i_code
     

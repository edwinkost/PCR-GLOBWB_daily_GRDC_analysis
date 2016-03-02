#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os


# PCR-GLOBWB output folder:
pcrglobwb_output_folder = str(sys.argv[1])

number_of_subfolders = 19

for i in range(1, number_of_subfolders + 1, 1):
    sub_folder = '%02i' %(i)
    cmd = 'python 0_main_analyze_discharge.py '+ sub_folder + " " + pcrglobwb_output_folder + " discharge_dailyTot_output "
    if (i % 5 == 0): cmd = cmd + " & "
    print cmd
    os.system(cmd)

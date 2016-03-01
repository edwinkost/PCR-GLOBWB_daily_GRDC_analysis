#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Edwin Husni Sutanudjaja (EHS, 19 Nov 2015): This is script for evaluating daily simulated discharge to GRDC discharge data.
# Edwin Husni Sutanudjaja (EHS, 01 Mar 2016): I modify the script 

import os
import sys
import glob
import shutil

import dischargeDailyGRDC

import logging
from logger import Logger
# get name for the logger
logger = logging.getLogger("main_script")

# PCR-GLOBWB results: model output directory 
pcrglobwb_output = {}
pcrglobwb_output["folder"]               = None # "/scratch/edwin/IWMI_run_20_nov/without_fossil_limit_with_pumping_limit_CRU/netcdf/"

# output directory storing analysis results (results from this script)
globalAnalysisOutputDir = None  # "/scratch/edwin/IWMI_run_20_nov/without_fossil_limit_with_pumping_limit_CRU/analysis/monthly_discharge/"

# optional: PCR-GLOBWB output and analysis output folders are based on the given the system argument
if len(sys.argv) > 1:
    pcrglobwb_output["folder"] = str(sys.argv[1])
    globalAnalysisOutputDir    = str(sys.argv[1])+"/analysis/"
try:
    os.makedirs(globalAnalysisOutputDir) 
except:
    pass 

# netcdf variable name
pcrglobwb_output["netcdf_variable_name"] = "discharge"

# netcdf file name:
pcrglobwb_output["netcdf_file_name"]     = None # "netcdf/discharge_dailyTot_output.nc"
if len(sys.argv) > 2:
    pcrglobwb_output["netcdf_file_name"] = str(sys.argv[2])

# time range for analyses
startDate = "1958-01-01" # None # "1960-01-31" #YYYY-MM-DD # None 
endDate   = "2010-12-31" # None # "2010-12-31" #YYYY-MM-DD # None 

# directory for GRDC files:
globalDirectoryGRDC = "/home/edwin/github/edwinkost/hyperhydro_pcrglobwb/daily_discharge_analysis_scripts/rhine_daily_discharge_data/"

# clone map
globalCloneMapFileName = "/projects/0/dfguu/users/edwin/data/hyperhydro/hyperhydro_wg1/EFAS/clone_maps/RhineMeuseHyperHydro5min.clone.map"

# ldd and cell area maps
lddMapFileName         = "/projects/0/dfguu/data/hydroworld/PCRGLOBWB20/input5min/routing/lddsound_05min.map"
cellAreaMapFileName    = "/projects/0/dfguu/data/hydroworld/PCRGLOBWB20/input5min/routing/cellsize05min.correct.map"

# the following is needed for evaluating model results with 5 arcmin resolution  # not working yet
catchmentClassFileName = None 




def main():

    # discharge analysis
    ####################################################################################################
    #
    # make analysisOutputDir
    # option to clean analysisOutputDir
    cleanOutputDir    = True 		
    analysisOutputDir = globalAnalysisOutputDir+"/daily_discharge_1958-2010/"
    try:
        os.makedirs(analysisOutputDir) 
    except:
        if cleanOutputDir == True: os.system('rm -r '+analysisOutputDir+"/*") 
    #
    # temporary directory (note that it is NOT a good idea to store temporary files in the memory (/dev/shm))
    temporary_directory = analysisOutputDir+"/tmp/"
    try:
        os.makedirs(temporary_directory) 
    except:
        os.system('rm -r '+temporary_directory+"/*") # make sure that temporary directory is clean 
    #
    # logger object for discharge analysis
    logger = Logger(analysisOutputDir)
    #
    # daily discharge evaluation (based on GRDC data)
    dischargeEvaluation = dischargeDailyGRDC.DailyDischargeEvaluation(pcrglobwb_output["folder"],\
                                                                      startDate, endDate, temporary_directory)
    # - get GRDC attributes of all stations:
    dischargeEvaluation.get_grdc_attributes(directoryGRDC = globalDirectoryGRDC)
    #
    # - evaluate daily discharge results
    dischargeEvaluation.evaluateAllModelResults(globalCloneMapFileName,\
                                                catchmentClassFileName,\
                                                lddMapFileName,\
                                                cellAreaMapFileName,\
                                                pcrglobwb_output,\
                                                analysisOutputDir)  
    ####################################################################################################

if __name__ == '__main__':
    sys.exit(main())

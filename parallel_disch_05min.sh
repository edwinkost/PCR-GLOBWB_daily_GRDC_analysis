#!/bin/bash
#SBATCH -N 1
#SBATCH -t 0:59:00
#SBATCH -p normal

python parallel_discharge_analysis.py


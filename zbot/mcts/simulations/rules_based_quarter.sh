#!/bin/bash
#SBATCH --nodes=1
#SBATCH --time=24:00:00
#SBATCH --job-name=MyJobName
#SBATCH --mem=2G
#SBATCH --partition=short
./rule_based_test.py -d 0.25 -e 1.0 -n quarter -mh /home/dawson.z/zbot/zbot/notebooks/random_forest_hand_rank.joblib -ma /home/dawson.z/zbot/zbot/notebooks/random_forest_action.joblib

#!/bin/bash
source ~/miniconda3/etc/profile.d/conda.sh #needed for conda lol
conda init bash
conda activate CenterNet
#script -f /home/haq/repos/IP_camera/src/terminal_log.log
cd /home/haq/repos/IP_camera/src
python /home/haq/repos/IP_camera/src/save_dataset_multiprocessing.py 

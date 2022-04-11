#!/bin/bash 
rm -rf _current_run_saved_files 
mkdir _current_run_saved_files 
rm -rf Run_info 
mkdir Run_info 
# Gen syntax: [interpreter] [code.py] [device] [sys_no] [run_no] [n_observables] [n_layers] [n_nodes] [write_to_file] 
python3 deepDMD.py '/cpu:0' 71 0 0 3 0 > System_71/MyRunInfo/Run_0.txt & 
wait
python3 deepDMD.py '/cpu:0' 71 1 1 3 2 > System_71/MyRunInfo/Run_1.txt & 
wait
python3 deepDMD.py '/cpu:0' 72 0 0 3 0 > System_72/MyRunInfo/Run_0.txt & 
wait
python3 deepDMD.py '/cpu:0' 72 1 1 3 2 > System_72/MyRunInfo/Run_1.txt & 
wait
echo "All sessions are complete" 
echo "=======================================================" 

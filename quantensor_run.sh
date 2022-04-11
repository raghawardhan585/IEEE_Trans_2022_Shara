#!/bin/bash 
rm -rf _current_run_saved_files 
mkdir _current_run_saved_files 
rm -rf Run_info 
mkdir Run_info 
# Gen syntax: [interpreter] [code.py] [device] [sys_no] [run_no] [n_observables] [n_layers] [n_nodes] [write_to_file] 
python3 deepDMD.py '/cpu:0' 28 0 0 3 0 > System_28/MyRunInfo/Run_0.txt & 
wait
python3 deepDMD.py '/cpu:0' 28 1 0 4 0 > System_28/MyRunInfo/Run_1.txt & 
wait
python3 deepDMD.py '/cpu:0' 28 2 1 3 2 > System_28/MyRunInfo/Run_2.txt & 
wait
python3 deepDMD.py '/cpu:0' 28 3 1 4 2 > System_28/MyRunInfo/Run_3.txt & 
wait
python3 deepDMD.py '/cpu:0' 28 4 2 3 3 > System_28/MyRunInfo/Run_4.txt & 
wait
python3 deepDMD.py '/cpu:0' 28 5 2 4 3 > System_28/MyRunInfo/Run_5.txt & 
wait
python3 deepDMD.py '/cpu:0' 28 6 3 3 5 > System_28/MyRunInfo/Run_6.txt & 
wait
python3 deepDMD.py '/cpu:0' 28 7 3 4 5 > System_28/MyRunInfo/Run_7.txt & 
wait
python3 deepDMD.py '/cpu:0' 28 8 4 3 6 > System_28/MyRunInfo/Run_8.txt & 
wait
python3 deepDMD.py '/cpu:0' 28 9 4 4 6 > System_28/MyRunInfo/Run_9.txt & 
wait
python3 deepDMD.py '/cpu:0' 28 10 5 3 8 > System_28/MyRunInfo/Run_10.txt & 
wait
python3 deepDMD.py '/cpu:0' 28 11 5 4 8 > System_28/MyRunInfo/Run_11.txt & 
wait
python3 deepDMD.py '/cpu:0' 28 12 6 3 9 > System_28/MyRunInfo/Run_12.txt & 
wait
python3 deepDMD.py '/cpu:0' 28 13 6 4 9 > System_28/MyRunInfo/Run_13.txt & 
wait
python3 deepDMD.py '/cpu:0' 28 14 7 3 11 > System_28/MyRunInfo/Run_14.txt & 
wait
python3 deepDMD.py '/cpu:0' 28 15 7 4 11 > System_28/MyRunInfo/Run_15.txt & 
wait
python3 deepDMD.py '/cpu:0' 28 16 8 3 12 > System_28/MyRunInfo/Run_16.txt & 
wait
python3 deepDMD.py '/cpu:0' 28 17 8 4 12 > System_28/MyRunInfo/Run_17.txt & 
wait
python3 deepDMD.py '/cpu:0' 28 18 9 3 14 > System_28/MyRunInfo/Run_18.txt & 
wait
python3 deepDMD.py '/cpu:0' 28 19 9 4 14 > System_28/MyRunInfo/Run_19.txt & 
wait
python3 deepDMD.py '/cpu:0' 28 20 10 3 15 > System_28/MyRunInfo/Run_20.txt & 
wait
python3 deepDMD.py '/cpu:0' 28 21 10 4 15 > System_28/MyRunInfo/Run_21.txt & 
wait
echo "All sessions are complete" 
echo "=======================================================" 

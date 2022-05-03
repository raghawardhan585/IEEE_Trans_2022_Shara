#!/bin/bash 
# Gen syntax: [interpreter] [code.py] [device] [sys_no] [run_no] [n_observables] [n_layers] [n_nodes] [write_to_file] 
python3 deepDMD.py '/cpu:0' 6 5 4 3 8 > System_6/MyRunInfo/Run_5.txt & 
wait
python3 deepDMD.py '/cpu:0' 6 6 4 4 8 > System_6/MyRunInfo/Run_6.txt & 
wait
python3 deepDMD.py '/cpu:0' 6 7 4 5 8 > System_6/MyRunInfo/Run_7.txt & 
wait
python3 deepDMD.py '/cpu:0' 6 8 8 3 16 > System_6/MyRunInfo/Run_8.txt & 
wait
python3 deepDMD.py '/cpu:0' 6 9 8 4 16 > System_6/MyRunInfo/Run_9.txt & 
wait
python3 deepDMD.py '/cpu:0' 6 10 8 5 16 > System_6/MyRunInfo/Run_10.txt & 
wait
python3 deepDMD.py '/cpu:0' 6 11 12 3 24 > System_6/MyRunInfo/Run_11.txt & 
wait
python3 deepDMD.py '/cpu:0' 6 12 12 4 24 > System_6/MyRunInfo/Run_12.txt & 
wait
python3 deepDMD.py '/cpu:0' 6 13 12 5 24 > System_6/MyRunInfo/Run_13.txt & 
wait
echo "All sessions are complete" 
echo "=======================================================" 

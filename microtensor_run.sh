#!/bin/bash 
# Gen syntax: [interpreter] [code.py] [device] [sys_no] [run_no] [n_observables] [n_layers] [n_nodes] [write_to_file] 
python3 deepDMD.py '/cpu:0' 6 14 16 3 24 > System_6/MyRunInfo/Run_14.txt &
wait
python3 deepDMD.py '/cpu:0' 6 15 16 4 24 > System_6/MyRunInfo/Run_15.txt &
wait
python3 deepDMD.py '/cpu:0' 6 16 20 3 30 > System_6/MyRunInfo/Run_16.txt &
wait
python3 deepDMD.py '/cpu:0' 6 17 20 4 30 > System_6/MyRunInfo/Run_17.txt &
wait
python3 deepDMD.py '/cpu:0' 6 18 24 3 36 > System_6/MyRunInfo/Run_18.txt &
wait
python3 deepDMD.py '/cpu:0' 6 19 24 4 36 > System_6/MyRunInfo/Run_19.txt &
wait
echo "All sessions are complete" 
echo "=======================================================" 

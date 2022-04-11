#!/bin/bash 
rm -rf _current_run_saved_files 
mkdir _current_run_saved_files 
rm -rf Run_info 
mkdir Run_info 
# Gen syntax: [interpreter] [code.py] [device] [sys_no] [run_no] [n_observables] [n_layers] [n_nodes] [write_to_file] 
python3 deepDMD.py '/gpu:2' 21 3 0 3 0 > System_21/MyRunInfo/Run_3.txt & 
python3 deepDMD.py '/gpu:3' 21 4 0 4 0 > System_21/MyRunInfo/Run_4.txt & 
wait
python3 deepDMD.py '/cpu:0' 21 5 1 3 2 > System_21/MyRunInfo/Run_5.txt & 
python3 deepDMD.py '/gpu:0' 21 6 1 4 2 > System_21/MyRunInfo/Run_6.txt & 
python3 deepDMD.py '/gpu:1' 21 7 2 3 3 > System_21/MyRunInfo/Run_7.txt & 
python3 deepDMD.py '/gpu:2' 21 8 2 4 3 > System_21/MyRunInfo/Run_8.txt & 
python3 deepDMD.py '/gpu:3' 21 9 3 3 5 > System_21/MyRunInfo/Run_9.txt & 
wait
python3 deepDMD.py '/cpu:0' 21 10 3 4 5 > System_21/MyRunInfo/Run_10.txt & 
python3 deepDMD.py '/gpu:0' 21 11 4 3 6 > System_21/MyRunInfo/Run_11.txt & 
python3 deepDMD.py '/gpu:1' 21 12 4 4 6 > System_21/MyRunInfo/Run_12.txt & 
python3 deepDMD.py '/gpu:2' 21 13 5 3 8 > System_21/MyRunInfo/Run_13.txt & 
python3 deepDMD.py '/gpu:3' 21 14 5 4 8 > System_21/MyRunInfo/Run_14.txt & 
wait
python3 deepDMD.py '/cpu:0' 21 15 6 3 9 > System_21/MyRunInfo/Run_15.txt & 
python3 deepDMD.py '/gpu:0' 21 16 6 4 9 > System_21/MyRunInfo/Run_16.txt & 
python3 deepDMD.py '/gpu:1' 21 17 7 3 11 > System_21/MyRunInfo/Run_17.txt & 
python3 deepDMD.py '/gpu:2' 21 18 7 4 11 > System_21/MyRunInfo/Run_18.txt & 
python3 deepDMD.py '/gpu:3' 21 19 8 3 12 > System_21/MyRunInfo/Run_19.txt & 
wait
python3 deepDMD.py '/cpu:0' 21 20 8 4 12 > System_21/MyRunInfo/Run_20.txt & 
python3 deepDMD.py '/gpu:0' 21 21 9 3 14 > System_21/MyRunInfo/Run_21.txt & 
python3 deepDMD.py '/gpu:1' 21 22 9 4 14 > System_21/MyRunInfo/Run_22.txt & 
python3 deepDMD.py '/gpu:2' 21 23 10 3 15 > System_21/MyRunInfo/Run_23.txt & 
python3 deepDMD.py '/gpu:3' 21 24 10 4 15 > System_21/MyRunInfo/Run_24.txt & 
wait
python3 deepDMD.py '/gpu:1' 22 2 0 3 0 > System_22/MyRunInfo/Run_2.txt & 
python3 deepDMD.py '/gpu:2' 22 3 0 4 0 > System_22/MyRunInfo/Run_3.txt & 
python3 deepDMD.py '/gpu:3' 22 4 1 3 2 > System_22/MyRunInfo/Run_4.txt & 
wait
python3 deepDMD.py '/cpu:0' 22 5 1 4 2 > System_22/MyRunInfo/Run_5.txt & 
python3 deepDMD.py '/gpu:0' 22 6 2 3 3 > System_22/MyRunInfo/Run_6.txt & 
python3 deepDMD.py '/gpu:1' 22 7 2 4 3 > System_22/MyRunInfo/Run_7.txt & 
python3 deepDMD.py '/gpu:2' 22 8 3 3 5 > System_22/MyRunInfo/Run_8.txt & 
python3 deepDMD.py '/gpu:3' 22 9 3 4 5 > System_22/MyRunInfo/Run_9.txt & 
wait
python3 deepDMD.py '/cpu:0' 22 10 4 3 6 > System_22/MyRunInfo/Run_10.txt & 
python3 deepDMD.py '/gpu:0' 22 11 4 4 6 > System_22/MyRunInfo/Run_11.txt & 
python3 deepDMD.py '/gpu:1' 22 12 5 3 8 > System_22/MyRunInfo/Run_12.txt & 
python3 deepDMD.py '/gpu:2' 22 13 5 4 8 > System_22/MyRunInfo/Run_13.txt & 
python3 deepDMD.py '/gpu:3' 22 14 6 3 9 > System_22/MyRunInfo/Run_14.txt & 
wait
python3 deepDMD.py '/cpu:0' 22 15 6 4 9 > System_22/MyRunInfo/Run_15.txt & 
python3 deepDMD.py '/gpu:0' 22 16 7 3 11 > System_22/MyRunInfo/Run_16.txt & 
python3 deepDMD.py '/gpu:1' 22 17 7 4 11 > System_22/MyRunInfo/Run_17.txt & 
python3 deepDMD.py '/gpu:2' 22 18 8 3 12 > System_22/MyRunInfo/Run_18.txt & 
python3 deepDMD.py '/gpu:3' 22 19 8 4 12 > System_22/MyRunInfo/Run_19.txt & 
wait
python3 deepDMD.py '/cpu:0' 22 20 9 3 14 > System_22/MyRunInfo/Run_20.txt & 
python3 deepDMD.py '/gpu:0' 22 21 9 4 14 > System_22/MyRunInfo/Run_21.txt & 
python3 deepDMD.py '/gpu:1' 22 22 10 3 15 > System_22/MyRunInfo/Run_22.txt & 
python3 deepDMD.py '/gpu:2' 22 23 10 4 15 > System_22/MyRunInfo/Run_23.txt & 
python3 deepDMD.py '/gpu:1' 23 7 0 3 0 > System_23/MyRunInfo/Run_7.txt & 
python3 deepDMD.py '/gpu:2' 23 8 0 4 0 > System_23/MyRunInfo/Run_8.txt & 
python3 deepDMD.py '/gpu:3' 23 9 1 3 2 > System_23/MyRunInfo/Run_9.txt & 
wait
python3 deepDMD.py '/cpu:0' 23 10 1 4 2 > System_23/MyRunInfo/Run_10.txt & 
python3 deepDMD.py '/gpu:0' 23 11 2 3 3 > System_23/MyRunInfo/Run_11.txt & 
python3 deepDMD.py '/gpu:1' 23 12 2 4 3 > System_23/MyRunInfo/Run_12.txt & 
python3 deepDMD.py '/gpu:2' 23 13 3 3 5 > System_23/MyRunInfo/Run_13.txt & 
python3 deepDMD.py '/gpu:3' 23 14 3 4 5 > System_23/MyRunInfo/Run_14.txt & 
wait
python3 deepDMD.py '/cpu:0' 23 15 4 3 6 > System_23/MyRunInfo/Run_15.txt & 
python3 deepDMD.py '/gpu:0' 23 16 4 4 6 > System_23/MyRunInfo/Run_16.txt & 
python3 deepDMD.py '/gpu:1' 23 17 5 3 8 > System_23/MyRunInfo/Run_17.txt & 
python3 deepDMD.py '/gpu:2' 23 18 5 4 8 > System_23/MyRunInfo/Run_18.txt & 
python3 deepDMD.py '/gpu:3' 23 19 6 3 9 > System_23/MyRunInfo/Run_19.txt & 
wait
python3 deepDMD.py '/cpu:0' 23 20 6 4 9 > System_23/MyRunInfo/Run_20.txt & 
python3 deepDMD.py '/gpu:0' 23 21 7 3 11 > System_23/MyRunInfo/Run_21.txt & 
python3 deepDMD.py '/gpu:1' 23 22 7 4 11 > System_23/MyRunInfo/Run_22.txt & 
python3 deepDMD.py '/gpu:2' 23 23 8 3 12 > System_23/MyRunInfo/Run_23.txt & 
python3 deepDMD.py '/gpu:3' 23 24 8 4 12 > System_23/MyRunInfo/Run_24.txt & 
wait
python3 deepDMD.py '/cpu:0' 23 25 9 3 14 > System_23/MyRunInfo/Run_25.txt & 
python3 deepDMD.py '/gpu:0' 23 26 9 4 14 > System_23/MyRunInfo/Run_26.txt & 
python3 deepDMD.py '/gpu:1' 23 27 10 3 15 > System_23/MyRunInfo/Run_27.txt & 
python3 deepDMD.py '/gpu:2' 23 28 10 4 15 > System_23/MyRunInfo/Run_28.txt & 
echo "All sessions are complete" 
echo "=======================================================" 

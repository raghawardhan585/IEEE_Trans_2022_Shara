#!/bin/bash 
rm -rf _current_run_saved_files 
mkdir _current_run_saved_files 
rm -rf Run_info 
mkdir Run_info 
# Gen syntax: [interpreter] [code.py] [device] [sys_no] [run_no] [n_observables] [n_layers] [n_nodes] [write_to_file] 
python3 deepDMD.py '/cpu:0' 24 0 0 3 0 > System_24/MyRunInfo/Run_0.txt & 
python3 deepDMD.py '/gpu:0' 24 1 0 4 0 > System_24/MyRunInfo/Run_1.txt & 
python3 deepDMD.py '/gpu:1' 24 2 1 3 2 > System_24/MyRunInfo/Run_2.txt & 
python3 deepDMD.py '/gpu:2' 24 3 1 4 2 > System_24/MyRunInfo/Run_3.txt & 
python3 deepDMD.py '/gpu:3' 24 4 2 3 3 > System_24/MyRunInfo/Run_4.txt & 
wait
python3 deepDMD.py '/cpu:0' 24 5 2 4 3 > System_24/MyRunInfo/Run_5.txt & 
python3 deepDMD.py '/gpu:0' 24 6 3 3 5 > System_24/MyRunInfo/Run_6.txt & 
python3 deepDMD.py '/gpu:1' 24 7 3 4 5 > System_24/MyRunInfo/Run_7.txt & 
python3 deepDMD.py '/gpu:2' 24 8 4 3 6 > System_24/MyRunInfo/Run_8.txt & 
python3 deepDMD.py '/gpu:3' 24 9 4 4 6 > System_24/MyRunInfo/Run_9.txt & 
wait
python3 deepDMD.py '/cpu:0' 24 10 5 3 8 > System_24/MyRunInfo/Run_10.txt & 
python3 deepDMD.py '/gpu:0' 24 11 5 4 8 > System_24/MyRunInfo/Run_11.txt & 
python3 deepDMD.py '/gpu:1' 24 12 6 3 9 > System_24/MyRunInfo/Run_12.txt & 
python3 deepDMD.py '/gpu:2' 24 13 6 4 9 > System_24/MyRunInfo/Run_13.txt & 
python3 deepDMD.py '/gpu:3' 24 14 7 3 11 > System_24/MyRunInfo/Run_14.txt & 
wait
python3 deepDMD.py '/cpu:0' 24 15 7 4 11 > System_24/MyRunInfo/Run_15.txt & 
python3 deepDMD.py '/gpu:0' 24 16 8 3 12 > System_24/MyRunInfo/Run_16.txt & 
python3 deepDMD.py '/gpu:1' 24 17 8 4 12 > System_24/MyRunInfo/Run_17.txt & 
python3 deepDMD.py '/gpu:2' 24 18 9 3 14 > System_24/MyRunInfo/Run_18.txt & 
python3 deepDMD.py '/gpu:3' 24 19 9 4 14 > System_24/MyRunInfo/Run_19.txt & 
wait
python3 deepDMD.py '/cpu:0' 24 20 10 3 15 > System_24/MyRunInfo/Run_20.txt & 
python3 deepDMD.py '/gpu:0' 24 21 10 4 15 > System_24/MyRunInfo/Run_21.txt & 
python3 deepDMD.py '/cpu:0' 25 0 0 3 0 > System_25/MyRunInfo/Run_0.txt & 
python3 deepDMD.py '/gpu:0' 25 1 0 4 0 > System_25/MyRunInfo/Run_1.txt & 
python3 deepDMD.py '/gpu:1' 25 2 1 3 2 > System_25/MyRunInfo/Run_2.txt & 
python3 deepDMD.py '/gpu:2' 25 3 1 4 2 > System_25/MyRunInfo/Run_3.txt & 
python3 deepDMD.py '/gpu:3' 25 4 2 3 3 > System_25/MyRunInfo/Run_4.txt & 
wait
python3 deepDMD.py '/cpu:0' 25 5 2 4 3 > System_25/MyRunInfo/Run_5.txt & 
python3 deepDMD.py '/gpu:0' 25 6 3 3 5 > System_25/MyRunInfo/Run_6.txt & 
python3 deepDMD.py '/gpu:1' 25 7 3 4 5 > System_25/MyRunInfo/Run_7.txt & 
python3 deepDMD.py '/gpu:2' 25 8 4 3 6 > System_25/MyRunInfo/Run_8.txt & 
python3 deepDMD.py '/gpu:3' 25 9 4 4 6 > System_25/MyRunInfo/Run_9.txt & 
wait
python3 deepDMD.py '/cpu:0' 25 10 5 3 8 > System_25/MyRunInfo/Run_10.txt & 
python3 deepDMD.py '/gpu:0' 25 11 5 4 8 > System_25/MyRunInfo/Run_11.txt & 
python3 deepDMD.py '/gpu:1' 25 12 6 3 9 > System_25/MyRunInfo/Run_12.txt & 
python3 deepDMD.py '/gpu:2' 25 13 6 4 9 > System_25/MyRunInfo/Run_13.txt & 
python3 deepDMD.py '/gpu:3' 25 14 7 3 11 > System_25/MyRunInfo/Run_14.txt & 
wait
python3 deepDMD.py '/cpu:0' 25 15 7 4 11 > System_25/MyRunInfo/Run_15.txt & 
python3 deepDMD.py '/gpu:0' 25 16 8 3 12 > System_25/MyRunInfo/Run_16.txt & 
python3 deepDMD.py '/gpu:1' 25 17 8 4 12 > System_25/MyRunInfo/Run_17.txt & 
python3 deepDMD.py '/gpu:2' 25 18 9 3 14 > System_25/MyRunInfo/Run_18.txt & 
python3 deepDMD.py '/gpu:3' 25 19 9 4 14 > System_25/MyRunInfo/Run_19.txt & 
wait
python3 deepDMD.py '/cpu:0' 25 20 10 3 15 > System_25/MyRunInfo/Run_20.txt & 
python3 deepDMD.py '/gpu:0' 25 21 10 4 15 > System_25/MyRunInfo/Run_21.txt & 
python3 deepDMD.py '/cpu:0' 26 0 0 3 0 > System_26/MyRunInfo/Run_0.txt & 
python3 deepDMD.py '/gpu:0' 26 1 0 4 0 > System_26/MyRunInfo/Run_1.txt & 
python3 deepDMD.py '/gpu:1' 26 2 1 3 2 > System_26/MyRunInfo/Run_2.txt & 
python3 deepDMD.py '/gpu:2' 26 3 1 4 2 > System_26/MyRunInfo/Run_3.txt & 
python3 deepDMD.py '/gpu:3' 26 4 2 3 3 > System_26/MyRunInfo/Run_4.txt & 
wait
python3 deepDMD.py '/cpu:0' 26 5 2 4 3 > System_26/MyRunInfo/Run_5.txt & 
python3 deepDMD.py '/gpu:0' 26 6 3 3 5 > System_26/MyRunInfo/Run_6.txt & 
python3 deepDMD.py '/gpu:1' 26 7 3 4 5 > System_26/MyRunInfo/Run_7.txt & 
python3 deepDMD.py '/gpu:2' 26 8 4 3 6 > System_26/MyRunInfo/Run_8.txt & 
python3 deepDMD.py '/gpu:3' 26 9 4 4 6 > System_26/MyRunInfo/Run_9.txt & 
wait
python3 deepDMD.py '/cpu:0' 26 10 5 3 8 > System_26/MyRunInfo/Run_10.txt & 
python3 deepDMD.py '/gpu:0' 26 11 5 4 8 > System_26/MyRunInfo/Run_11.txt & 
python3 deepDMD.py '/gpu:1' 26 12 6 3 9 > System_26/MyRunInfo/Run_12.txt & 
python3 deepDMD.py '/gpu:2' 26 13 6 4 9 > System_26/MyRunInfo/Run_13.txt & 
python3 deepDMD.py '/gpu:3' 26 14 7 3 11 > System_26/MyRunInfo/Run_14.txt & 
wait
python3 deepDMD.py '/cpu:0' 26 15 7 4 11 > System_26/MyRunInfo/Run_15.txt & 
python3 deepDMD.py '/gpu:0' 26 16 8 3 12 > System_26/MyRunInfo/Run_16.txt & 
python3 deepDMD.py '/gpu:1' 26 17 8 4 12 > System_26/MyRunInfo/Run_17.txt & 
python3 deepDMD.py '/gpu:2' 26 18 9 3 14 > System_26/MyRunInfo/Run_18.txt & 
python3 deepDMD.py '/gpu:3' 26 19 9 4 14 > System_26/MyRunInfo/Run_19.txt & 
wait
python3 deepDMD.py '/cpu:0' 26 20 10 3 15 > System_26/MyRunInfo/Run_20.txt & 
python3 deepDMD.py '/gpu:0' 26 21 10 4 15 > System_26/MyRunInfo/Run_21.txt & 
echo "All sessions are complete" 
echo "=======================================================" 

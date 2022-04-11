#!/bin/bash 
# Gen syntax: [interpreter] [code.py] [device] [sys_no] [run_no] [n_observables] [n_layers] [n_nodes] [write_to_file] 
python3 deepDMD.py '/cpu:0' 1 3 0 3 0 > System_1/MyRunInfo/Run_3.txt & 
wait
python3 deepDMD.py '/cpu:0' 1 4 0 4 0 > System_1/MyRunInfo/Run_4.txt & 
wait
python3 deepDMD.py '/cpu:0' 1 5 1 3 2 > System_1/MyRunInfo/Run_5.txt & 
wait
python3 deepDMD.py '/cpu:0' 1 6 1 4 2 > System_1/MyRunInfo/Run_6.txt & 
wait
python3 deepDMD.py '/cpu:0' 1 7 2 3 3 > System_1/MyRunInfo/Run_7.txt & 
wait
python3 deepDMD.py '/cpu:0' 1 8 2 4 3 > System_1/MyRunInfo/Run_8.txt & 
wait
python3 deepDMD.py '/cpu:0' 1 9 3 3 5 > System_1/MyRunInfo/Run_9.txt & 
wait
python3 deepDMD.py '/cpu:0' 1 10 3 4 5 > System_1/MyRunInfo/Run_10.txt & 
wait
python3 deepDMD.py '/cpu:0' 1 11 4 3 6 > System_1/MyRunInfo/Run_11.txt & 
wait
python3 deepDMD.py '/cpu:0' 1 12 4 4 6 > System_1/MyRunInfo/Run_12.txt & 
wait
python3 deepDMD.py '/cpu:0' 1 13 5 3 8 > System_1/MyRunInfo/Run_13.txt & 
wait
python3 deepDMD.py '/cpu:0' 1 14 5 4 8 > System_1/MyRunInfo/Run_14.txt & 
wait
python3 deepDMD.py '/cpu:0' 1 15 6 3 9 > System_1/MyRunInfo/Run_15.txt & 
wait
python3 deepDMD.py '/cpu:0' 1 16 6 4 9 > System_1/MyRunInfo/Run_16.txt & 
wait
python3 deepDMD.py '/cpu:0' 1 17 7 3 11 > System_1/MyRunInfo/Run_17.txt & 
wait
python3 deepDMD.py '/cpu:0' 1 18 7 4 11 > System_1/MyRunInfo/Run_18.txt & 
wait
python3 deepDMD.py '/cpu:0' 2 0 0 3 0 > System_2/MyRunInfo/Run_0.txt & 
wait
python3 deepDMD.py '/cpu:0' 2 1 0 4 0 > System_2/MyRunInfo/Run_1.txt & 
wait
python3 deepDMD.py '/cpu:0' 2 2 1 3 2 > System_2/MyRunInfo/Run_2.txt & 
wait
python3 deepDMD.py '/cpu:0' 2 3 1 4 2 > System_2/MyRunInfo/Run_3.txt & 
wait
python3 deepDMD.py '/cpu:0' 2 4 2 3 3 > System_2/MyRunInfo/Run_4.txt & 
wait
python3 deepDMD.py '/cpu:0' 2 5 2 4 3 > System_2/MyRunInfo/Run_5.txt & 
wait
python3 deepDMD.py '/cpu:0' 2 6 3 3 5 > System_2/MyRunInfo/Run_6.txt & 
wait
python3 deepDMD.py '/cpu:0' 2 7 3 4 5 > System_2/MyRunInfo/Run_7.txt & 
wait
python3 deepDMD.py '/cpu:0' 2 8 4 3 6 > System_2/MyRunInfo/Run_8.txt & 
wait
python3 deepDMD.py '/cpu:0' 2 9 4 4 6 > System_2/MyRunInfo/Run_9.txt & 
wait
python3 deepDMD.py '/cpu:0' 2 10 5 3 8 > System_2/MyRunInfo/Run_10.txt & 
wait
python3 deepDMD.py '/cpu:0' 2 11 5 4 8 > System_2/MyRunInfo/Run_11.txt & 
wait
python3 deepDMD.py '/cpu:0' 2 12 6 3 9 > System_2/MyRunInfo/Run_12.txt & 
wait
python3 deepDMD.py '/cpu:0' 2 13 6 4 9 > System_2/MyRunInfo/Run_13.txt & 
wait
python3 deepDMD.py '/cpu:0' 2 14 7 3 11 > System_2/MyRunInfo/Run_14.txt & 
wait
python3 deepDMD.py '/cpu:0' 2 15 7 4 11 > System_2/MyRunInfo/Run_15.txt & 
wait
python3 deepDMD.py '/cpu:0' 3 5 0 3 0 > System_3/MyRunInfo/Run_5.txt & 
wait
python3 deepDMD.py '/cpu:0' 3 6 0 4 0 > System_3/MyRunInfo/Run_6.txt & 
wait
python3 deepDMD.py '/cpu:0' 3 7 1 3 2 > System_3/MyRunInfo/Run_7.txt & 
wait
python3 deepDMD.py '/cpu:0' 3 8 1 4 2 > System_3/MyRunInfo/Run_8.txt & 
wait
python3 deepDMD.py '/cpu:0' 3 9 2 3 3 > System_3/MyRunInfo/Run_9.txt & 
wait
python3 deepDMD.py '/cpu:0' 3 10 2 4 3 > System_3/MyRunInfo/Run_10.txt & 
wait
python3 deepDMD.py '/cpu:0' 3 11 3 3 5 > System_3/MyRunInfo/Run_11.txt & 
wait
python3 deepDMD.py '/cpu:0' 3 12 3 4 5 > System_3/MyRunInfo/Run_12.txt & 
wait
python3 deepDMD.py '/cpu:0' 3 13 4 3 6 > System_3/MyRunInfo/Run_13.txt & 
wait
python3 deepDMD.py '/cpu:0' 3 14 4 4 6 > System_3/MyRunInfo/Run_14.txt & 
wait
python3 deepDMD.py '/cpu:0' 3 15 5 3 8 > System_3/MyRunInfo/Run_15.txt & 
wait
python3 deepDMD.py '/cpu:0' 3 16 5 4 8 > System_3/MyRunInfo/Run_16.txt & 
wait
python3 deepDMD.py '/cpu:0' 3 17 6 3 9 > System_3/MyRunInfo/Run_17.txt & 
wait
python3 deepDMD.py '/cpu:0' 3 18 6 4 9 > System_3/MyRunInfo/Run_18.txt & 
wait
python3 deepDMD.py '/cpu:0' 3 19 7 3 11 > System_3/MyRunInfo/Run_19.txt & 
wait
python3 deepDMD.py '/cpu:0' 3 20 7 4 11 > System_3/MyRunInfo/Run_20.txt & 
wait
python3 deepDMD.py '/cpu:0' 4 0 0 3 0 > System_4/MyRunInfo/Run_0.txt & 
wait
python3 deepDMD.py '/cpu:0' 4 1 0 4 0 > System_4/MyRunInfo/Run_1.txt & 
wait
python3 deepDMD.py '/cpu:0' 4 2 1 3 2 > System_4/MyRunInfo/Run_2.txt & 
wait
python3 deepDMD.py '/cpu:0' 4 3 1 4 2 > System_4/MyRunInfo/Run_3.txt & 
wait
python3 deepDMD.py '/cpu:0' 4 4 2 3 3 > System_4/MyRunInfo/Run_4.txt & 
wait
python3 deepDMD.py '/cpu:0' 4 5 2 4 3 > System_4/MyRunInfo/Run_5.txt & 
wait
python3 deepDMD.py '/cpu:0' 4 6 3 3 5 > System_4/MyRunInfo/Run_6.txt & 
wait
python3 deepDMD.py '/cpu:0' 4 7 3 4 5 > System_4/MyRunInfo/Run_7.txt & 
wait
python3 deepDMD.py '/cpu:0' 4 8 4 3 6 > System_4/MyRunInfo/Run_8.txt & 
wait
python3 deepDMD.py '/cpu:0' 4 9 4 4 6 > System_4/MyRunInfo/Run_9.txt & 
wait
python3 deepDMD.py '/cpu:0' 4 10 5 3 8 > System_4/MyRunInfo/Run_10.txt & 
wait
python3 deepDMD.py '/cpu:0' 4 11 5 4 8 > System_4/MyRunInfo/Run_11.txt & 
wait
python3 deepDMD.py '/cpu:0' 4 12 6 3 9 > System_4/MyRunInfo/Run_12.txt & 
wait
python3 deepDMD.py '/cpu:0' 4 13 6 4 9 > System_4/MyRunInfo/Run_13.txt & 
wait
python3 deepDMD.py '/cpu:0' 4 14 7 3 11 > System_4/MyRunInfo/Run_14.txt & 
wait
python3 deepDMD.py '/cpu:0' 4 15 7 4 11 > System_4/MyRunInfo/Run_15.txt & 
wait
python3 deepDMD.py '/cpu:0' 5 21 0 3 0 > System_5/MyRunInfo/Run_21.txt & 
wait
python3 deepDMD.py '/cpu:0' 5 22 0 4 0 > System_5/MyRunInfo/Run_22.txt & 
wait
python3 deepDMD.py '/cpu:0' 5 23 1 3 2 > System_5/MyRunInfo/Run_23.txt & 
wait
python3 deepDMD.py '/cpu:0' 5 24 1 4 2 > System_5/MyRunInfo/Run_24.txt & 
wait
python3 deepDMD.py '/cpu:0' 5 25 2 3 3 > System_5/MyRunInfo/Run_25.txt & 
wait
python3 deepDMD.py '/cpu:0' 5 26 2 4 3 > System_5/MyRunInfo/Run_26.txt & 
wait
python3 deepDMD.py '/cpu:0' 5 27 3 3 5 > System_5/MyRunInfo/Run_27.txt & 
wait
python3 deepDMD.py '/cpu:0' 5 28 3 4 5 > System_5/MyRunInfo/Run_28.txt & 
wait
python3 deepDMD.py '/cpu:0' 5 29 4 3 6 > System_5/MyRunInfo/Run_29.txt & 
wait
python3 deepDMD.py '/cpu:0' 5 30 4 4 6 > System_5/MyRunInfo/Run_30.txt & 
wait
python3 deepDMD.py '/cpu:0' 5 31 5 3 8 > System_5/MyRunInfo/Run_31.txt & 
wait
python3 deepDMD.py '/cpu:0' 5 32 5 4 8 > System_5/MyRunInfo/Run_32.txt & 
wait
python3 deepDMD.py '/cpu:0' 5 33 6 3 9 > System_5/MyRunInfo/Run_33.txt & 
wait
python3 deepDMD.py '/cpu:0' 5 34 6 4 9 > System_5/MyRunInfo/Run_34.txt & 
wait
python3 deepDMD.py '/cpu:0' 5 35 7 3 11 > System_5/MyRunInfo/Run_35.txt & 
wait
python3 deepDMD.py '/cpu:0' 5 36 7 4 11 > System_5/MyRunInfo/Run_36.txt & 
wait
python3 deepDMD.py '/cpu:0' 6 5 0 3 0 > System_6/MyRunInfo/Run_5.txt & 
wait
python3 deepDMD.py '/cpu:0' 6 6 0 4 0 > System_6/MyRunInfo/Run_6.txt & 
wait
python3 deepDMD.py '/cpu:0' 6 7 1 3 2 > System_6/MyRunInfo/Run_7.txt & 
wait
python3 deepDMD.py '/cpu:0' 6 8 1 4 2 > System_6/MyRunInfo/Run_8.txt & 
wait
python3 deepDMD.py '/cpu:0' 6 9 2 3 3 > System_6/MyRunInfo/Run_9.txt & 
wait
python3 deepDMD.py '/cpu:0' 6 10 2 4 3 > System_6/MyRunInfo/Run_10.txt & 
wait
python3 deepDMD.py '/cpu:0' 6 11 3 3 5 > System_6/MyRunInfo/Run_11.txt & 
wait
python3 deepDMD.py '/cpu:0' 6 12 3 4 5 > System_6/MyRunInfo/Run_12.txt & 
wait
python3 deepDMD.py '/cpu:0' 6 13 4 3 6 > System_6/MyRunInfo/Run_13.txt & 
wait
python3 deepDMD.py '/cpu:0' 6 14 4 4 6 > System_6/MyRunInfo/Run_14.txt & 
wait
python3 deepDMD.py '/cpu:0' 6 15 5 3 8 > System_6/MyRunInfo/Run_15.txt & 
wait
python3 deepDMD.py '/cpu:0' 6 16 5 4 8 > System_6/MyRunInfo/Run_16.txt & 
wait
python3 deepDMD.py '/cpu:0' 6 17 6 3 9 > System_6/MyRunInfo/Run_17.txt & 
wait
python3 deepDMD.py '/cpu:0' 6 18 6 4 9 > System_6/MyRunInfo/Run_18.txt & 
wait
python3 deepDMD.py '/cpu:0' 6 19 7 3 11 > System_6/MyRunInfo/Run_19.txt & 
wait
python3 deepDMD.py '/cpu:0' 6 20 7 4 11 > System_6/MyRunInfo/Run_20.txt & 
wait
echo "All sessions are complete" 
echo "=======================================================" 

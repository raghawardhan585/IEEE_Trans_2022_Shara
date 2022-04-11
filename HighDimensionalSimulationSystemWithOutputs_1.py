import numpy as np
import pandas as pd
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from itertools import product
from sklearn.preprocessing import Normalizer, MinMaxScaler, StandardScaler
import copy
import pickle
plt.rcParams["font.family"] = "Avenir"
plt.rcParams["mathtext.fontset"] = "cm"
plt.rcParams["font.size"] = 22
from Simulated_HighDimensional_Systems import *
import os
import shutil
# import keras
# from keras.models import Sequential
# from keras.layers import Dense

def organize_output_data_for_learning(ls_data, n_delay_embeddings =1, ls_output_columns = [0,1,2]):
    # Organize the data
    ls_dataset_indices = list(range(len(ls_data)))
    datapoints_per_dataset = len(ls_data[0]['Y'])
    X = np.empty((0, n_delay_embeddings * len(ls_output_columns)))
    Y = np.empty((0, len(ls_output_columns)))
    for d_i, j in product(ls_dataset_indices, list(range(n_delay_embeddings, datapoints_per_dataset))): # j tracks the output
        X = np.concatenate([X, ls_data[d_i]['Y'][j-n_delay_embeddings:j,ls_output_columns].T.reshape(1,-1)], axis=0)
        Y = np.concatenate([Y, ls_data[d_i]['Y'][j:j+1,ls_output_columns]], axis=0)
    return X,Y


def organize_output_data_for_deepDMD(ls_data, n_delay_embeddings =1, ls_output_columns = [0,1,2], with_intersection = True):
    # Organize the data
    ls_dataset_indices = list(range(len(ls_data)))
    datapoints_per_dataset = len(ls_data[0]['YT'])
    XpT = np.empty((0, n_delay_embeddings * len(ls_output_columns)))
    XfT = np.empty((0, n_delay_embeddings * len(ls_output_columns)))
    if with_intersection:
        for d_i, j in product(ls_dataset_indices, list(range(n_delay_embeddings, datapoints_per_dataset))): # j tracks the output
            XpT = np.concatenate([XpT, ls_data[d_i]['YT'][j-n_delay_embeddings:j,ls_output_columns].T.reshape(1,-1)], axis=0)
            XfT = np.concatenate([XfT, ls_data[d_i]['YT'][j-n_delay_embeddings+1:j+1,ls_output_columns].T.reshape(1,-1)], axis=0)
    else:
        n_delay_embedded_points_per_dataset = np.int(np.floor(datapoints_per_dataset / n_delay_embeddings))
        for d_i, j in product(ls_dataset_indices, list(range(n_delay_embedded_points_per_dataset - 1))):
            XpT = np.concatenate([XpT, ls_data[d_i]['YT'][j * n_delay_embeddings:(j + 1) * n_delay_embeddings,
                                       ls_output_columns].T.reshape(1, -1)], axis=0)
            XfT = np.concatenate([XfT, ls_data[d_i]['YT'][(j + 1) * n_delay_embeddings:(j + 2) * n_delay_embeddings,
                                       ls_output_columns].T.reshape(1, -1)], axis=0)
    return XpT, XfT

def organize_state_data_for_deepDMD(ls_data, ls_state_columns = [0,1,2,3,4,5]):
    # Organize the data
    ls_dataset_indices = list(range(len(ls_data)))
    n_states = len(ls_state_columns)
    XpT = np.empty((0, n_states))
    XfT = np.empty((0, n_states))
    for d_i in ls_dataset_indices:
        XpT = np.concatenate([XpT, ls_data[d_i]['XT'][0:-1,ls_state_columns]], axis=0)
        XfT = np.concatenate([XfT, ls_data[d_i]['XT'][1:,ls_state_columns]], axis=0)
    return XpT, XfT

def organize_state_and_output_data_for_deepDMD(ls_data, ls_state_columns = [0,1,2,3,4,5,6], ls_output_columns = [0]):
    # Organize the data
    ls_dataset_indices = list(range(len(ls_data)))
    n_states = len(ls_state_columns)
    n_outputs = len(ls_output_columns)
    XpT = np.empty((0, n_states))
    XfT = np.empty((0, n_states))
    YpT = np.empty((0, n_outputs))
    YfT = np.empty((0, n_outputs))
    for d_i in ls_dataset_indices:
        XpT = np.concatenate([XpT, ls_data[d_i]['XT'][0:-1,ls_state_columns]], axis=0)
        XfT = np.concatenate([XfT, ls_data[d_i]['XT'][1:,ls_state_columns]], axis=0)
        YpT = np.concatenate([YpT, ls_data[d_i]['YT'][0:-1,ls_output_columns]], axis=0)
        YfT = np.concatenate([YfT, ls_data[d_i]['YT'][1:,ls_output_columns]], axis=0)
    return XpT, XfT, YpT, YfT

def create_folder(SYSTEM_NO):
    storage_folder = '/Users/shara/Desktop/IEEETransactions_2022/System_' + str(SYSTEM_NO)
    if os.path.exists(storage_folder):
        shutil.rmtree(storage_folder)
        os.mkdir(storage_folder)
        # get_input = input('Do you wanna delete the existing system[y/n]? ')
        # if get_input == 'y':
        #     shutil.rmtree(storage_folder)
        #     os.mkdir(storage_folder)
        # else:
        #     return
    else:
        os.mkdir(storage_folder)
    return storage_folder

def output_type_1(A,B,Vm,K):
    # A--->C | B---|C
    # Model: C = Vm * A /(1 + B/K)
    C = Vm*A/(1 + (B/K))
    return C

def save_system(ls_data, dict_measurement_info, SYSTEM_NO):
    # STEP 2: ORGAINZE THE DATA FOR THE DELAY EMBEDDING
    # Simulation Parameters
    state_measured = dict_measurement_info['state_measured']
    output_measured = dict_measurement_info['output_measured']
    n_delay_embeddings = dict_measurement_info['n_delay_embedding']
    ls_measured_output_indices = dict_measurement_info['ls_measured_output_indices']
    ls_measured_state_indices = dict_measurement_info['ls_measured_state_indices']
    formulate_Koopman_output_data_with_intersection = dict_measurement_info[
        'formulate_Koopman_output_data_with_intersection']

    # Incorporate all of these into the functions
    if state_measured:
        n_delay_embeddings = 1
        formulate_Koopman_output_data_with_intersection = False
    if not output_measured:
        ls_measured_output_indices = []

    # Fill these functions
    if output_measured and not state_measured:
        XpT, XfT = organize_output_data_for_deepDMD(ls_data, n_delay_embeddings=n_delay_embeddings,
                                                    ls_output_columns=ls_measured_output_indices,
                                                    with_intersection=formulate_Koopman_output_data_with_intersection)
    elif state_measured and not output_measured:
        XpT, XfT = organize_state_data_for_deepDMD(ls_data, ls_state_columns=ls_measured_state_indices)
    elif state_measured and output_measured:
        XpT, XfT, YpT, YfT = organize_state_and_output_data_for_deepDMD(ls_data, ls_state_columns=ls_measured_state_indices, ls_output_columns=ls_measured_output_indices)

    # Partition to training and testing data
    n_one_third_data = np.int(np.floor(XpT.shape[0] / 3))

    dict_DATA_RAW = {}
    dict_DATA_RAW['train'] = {'XpT': XpT[0:n_one_third_data, :], 'XfT': XfT[0:n_one_third_data, :]}
    dict_DATA_RAW['valid'] = {'XpT': XpT[n_one_third_data:2 * n_one_third_data, :],
                              'XfT': XfT[n_one_third_data:2 * n_one_third_data, :]}
    dict_DATA_RAW['test'] = {'XpT': XpT[2 * n_one_third_data:, :], 'XfT': XfT[2 * n_one_third_data:, :]}
    dict_DATA_RAW['embedding'] = n_delay_embeddings

    dict_Scaler = {}
    dict_Scaler['XT'] = StandardScaler(with_mean=True, with_std=True).fit(dict_DATA_RAW['train']['XpT'])

    if state_measured and output_measured:
        dict_DATA_RAW['train']['YpT'] = YpT[0:n_one_third_data, :]
        dict_DATA_RAW['train']['YfT'] = YfT[0:n_one_third_data, :]
        dict_DATA_RAW['valid']['YpT'] = YpT[n_one_third_data:2 * n_one_third_data, :]
        dict_DATA_RAW['valid']['YfT'] = YfT[n_one_third_data:2 * n_one_third_data, :]
        dict_DATA_RAW['test']['YpT'] = YpT[2 * n_one_third_data:, :]
        dict_DATA_RAW['test']['YfT'] = YfT[2 * n_one_third_data:, :]
        dict_Scaler['YT'] = StandardScaler(with_mean=True, with_std=True).fit(dict_DATA_RAW['train']['YpT'])

    dict_DATA_SCALED = {}
    for i in ['train', 'test', 'valid']:
        dict_DATA_SCALED[i] = {}
        for items in dict_DATA_RAW[i]:
            if items in ['XpT', 'XfT']:
                dict_DATA_SCALED[i][items] = dict_Scaler['XT'].transform(dict_DATA_RAW[i][items])
            elif items in ['YpT', 'YfT']:
                dict_DATA_SCALED[i][items] = dict_Scaler['YT'].transform(dict_DATA_RAW[i][items])
    dict_DATA_SCALED['embedding'] = n_delay_embeddings

    # STEP 3: SAVE THE DATA TO THE REQUIED FOLDER
    storage_folder = create_folder(SYSTEM_NO)
    # Save the scaler
    with open(storage_folder + '/System_' + str(SYSTEM_NO) + '_DataScaler.pickle', 'wb') as handle:
        pickle.dump(dict_Scaler, handle)
    # Save the data for OC_deepDMD
    with open(storage_folder + '/System_' + str(SYSTEM_NO) + '_DeepDMDdata_Scaled.pickle', 'wb') as handle:
        pickle.dump(dict_DATA_SCALED, handle)
    # Save the unscaled deepDMD data
    with open(storage_folder + '/System_' + str(SYSTEM_NO) + '_DeepDMDdata_Unscaled.pickle', 'wb') as handle:
        pickle.dump(dict_DATA_SCALED, handle)
    # Save the original data
    with open(storage_folder + '/System_' + str(SYSTEM_NO) + '_SimulatedData.pickle', 'wb') as handle:
        pickle.dump(ls_data, handle)
    # Store the data in Koopman
    # with open('/Users/shara/Desktop/oc_deepDMD/koopman_data/System_' + str(SYSTEM_NO) + '_ocDeepDMDdata.pickle','wb') as handle:
    #     pickle.dump(dict_DATA_SCALED, handle)
    # Save the simulated data information as well
    with open(storage_folder + '/System_' + str(SYSTEM_NO) + '_SimulatedDataInfo.pickle', 'wb') as handle:
        pickle.dump(dict_measurement_info, handle)
    return


## STEP 1: SIMULATE THE SYSTEM
#

numpy_random_initial_condition_seed = 10
# Simulation Parameters
simulation_time = 60
sampling_time = 1.
t = np.arange(0, simulation_time, sampling_time)
# x0_init_ar = np.array([0.1,0.8])
x0_init_ar = np.array([10.1,4.1])
x0_init_iffl = np.array([20.,5.5])
# x0_init_go = np.array([0.1,0.8,0.4,0.3,0.3,0.8,1.])
x0_init_ts = np.array([10.1,5.1])
# x0_init_ts = np.array([6,0.8])

# ToggleSwitch_ActRep_IFFL
x0_init = np.array([])
x0_init = np.concatenate([x0_init, x0_init_ts])
x0_init = np.concatenate([x0_init, x0_init_ar])
x0_init = np.concatenate([x0_init, x0_init_iffl])
simulation_system = Ts_Ar_Iffl
N_SIMULATIONS = 60
np.random.seed(numpy_random_initial_condition_seed)
ls_seed_for_initial_condition = np.random.randint(0,10000,(N_SIMULATIONS))
ls_data = []
i=0
for i in range(N_SIMULATIONS):
    np.random.seed(ls_seed_for_initial_condition[i])
    x0_init_i = x0_init + np.random.normal(0, 1.5, size=x0_init.shape)
    X = odeint(simulation_system,x0_init_i,t,(1.,1.))
    if (np.sum(X>500) > 0) or (np.sum(X==0)>5):
        continue
    else:
        # Make the Output
        Y = output_type_1(X[:, 0:1], X[:, 1:2], 3, 1)
        Y = np.concatenate([Y, output_type_1(X[:, 2:3], X[:, 3:4], 3, 1)], axis=1)
        Y = np.concatenate([Y, output_type_1(X[:, 4:5], X[:, 5:6], 3, 1)], axis=1)
        dict_data_i = {'XT': X, 'YT': Y}
        ls_data.append(dict_data_i)

Xs = (X -np.mean(X,axis=0))/np.std(X,axis=0)
f,ax = plt.subplots(2,1,figsize=(8,10),sharex=True)
ax[0].plot(t,X[:,0:6])
ax[0].set_title('Unscaled')
ax[1].plot(t,Xs[:,0:6])
ax[1].legend(['x1','x2','x3','x4','x5','x6'],ncol=2,loc='upper right')
ax[1].set_title('Scaled')
f.show()

f,ax = plt.subplots(1,3,figsize=(15,5))
for i in range(N_SIMULATIONS):
    ax[0].plot(ls_data[i]['XT'][:, 0], ls_data[i]['XT'][:, 1])
    ax[1].plot(ls_data[i]['XT'][:, 2], ls_data[i]['XT'][:, 3])
    ax[2].plot(ls_data[i]['XT'][:, 4], ls_data[i]['XT'][:, 5])
ax[0].set_title('Toggle_Switch')
ax[1].set_title('Activator_Repressor')
ax[2].set_title('IFFL')
# ax[2].set_ylim([0,1])
# ax[2].set_xlim([0,8])
f.show()


dict_simulation_parameters = {'numpy_random_initial_condition_seed': numpy_random_initial_condition_seed, 'simulation_time':simulation_time, 'sampling_time': sampling_time, 't':t, 'x0_init_ar':x0_init_ar, 'x0_init_iffl':x0_init_iffl, 'x0_init_ts':x0_init_ts}


# ## SYSTEM 1 - Toggle Switch - State x1:2
# dict_measurement_info_1 = {'state_measured': True, 'output_measured': False, 'n_delay_embedding': 1, 'ls_measured_output_indices': [], 'ls_measured_state_indices': [0,1], 'formulate_Koopman_output_data_with_intersection': False}
# dict_measurement_info_1.update(dict_simulation_parameters)
# save_system(ls_data, dict_measurement_info = dict_measurement_info_1, SYSTEM_NO =1)
#
# ## SYSTEM 2 - Toggle Switch - State x1:2 Output y1
# dict_measurement_info_2 = {'state_measured': True, 'output_measured': True, 'n_delay_embedding': 1, 'ls_measured_output_indices': [0], 'ls_measured_state_indices': [0,1], 'formulate_Koopman_output_data_with_intersection': False}
# dict_measurement_info_2.update(dict_simulation_parameters)
# save_system(ls_data, dict_measurement_info = dict_measurement_info_2, SYSTEM_NO =2)
#
# ## SYSTEM 3 - Toggle_Switch___Activator_Repressor - State x1:4
# dict_measurement_info_3 = {'state_measured': True, 'output_measured': False, 'n_delay_embedding': 1, 'ls_measured_output_indices': [], 'ls_measured_state_indices': [0,1,2,3], 'formulate_Koopman_output_data_with_intersection': False}
# dict_measurement_info_3.update(dict_simulation_parameters)
# save_system(ls_data, dict_measurement_info = dict_measurement_info_3, SYSTEM_NO =3)
#
# ## SYSTEM 4 - Toggle_Switch___Activator_Repressor - State x1:4 Output y1,y2
# dict_measurement_info_4 = {'state_measured': True, 'output_measured': True, 'n_delay_embedding': 1, 'ls_measured_output_indices': [0,1], 'ls_measured_state_indices': [0,1,2,3], 'formulate_Koopman_output_data_with_intersection': False}
# dict_measurement_info_4.update(dict_simulation_parameters)
# save_system(ls_data, dict_measurement_info = dict_measurement_info_4, SYSTEM_NO =4)
#
# ## SYSTEM 5 - Toggle_Switch___Activator_Repressor - State x1:6
# dict_measurement_info_5 = {'state_measured': True, 'output_measured': False, 'n_delay_embedding': 1, 'ls_measured_output_indices': [], 'ls_measured_state_indices': [0,1,2,3,4,5], 'formulate_Koopman_output_data_with_intersection': False}
# dict_measurement_info_5.update(dict_simulation_parameters)
# save_system(ls_data, dict_measurement_info = dict_measurement_info_5, SYSTEM_NO =5)
#
# ## SYSTEM 6 - Toggle_Switch___Activator_Repressor - State x1:6 Output y1,y2,y3
# dict_measurement_info_6 = {'state_measured': True, 'output_measured': True, 'n_delay_embedding': 1, 'ls_measured_output_indices': [0,1,2], 'ls_measured_state_indices': [0,1,2,3,4,5], 'formulate_Koopman_output_data_with_intersection': False}
# dict_measurement_info_6.update(dict_simulation_parameters)
# save_system(ls_data, dict_measurement_info = dict_measurement_info_6, SYSTEM_NO =6)



#
# ## Output Only systems with delay embedding
# for n_delay_embedding in range(1,10):
#     # SYSTEM 10...19 - Output y1
#     dict_measurement_info_10 = {'state_measured': False, 'output_measured': True, 'n_delay_embedding': n_delay_embedding, 'ls_measured_output_indices': [0], 'ls_measured_state_indices': [], 'formulate_Koopman_output_data_with_intersection': False }
#     dict_measurement_info_10.update(dict_simulation_parameters)
#     save_system(ls_data, dict_measurement_info = dict_measurement_info_10, SYSTEM_NO =10+n_delay_embedding)
#
#     # SYSTEM 20...29 - Output y2
#     dict_measurement_info_20 = {'state_measured': False, 'output_measured': True, 'n_delay_embedding': n_delay_embedding, 'ls_measured_output_indices': [1], 'ls_measured_state_indices': [], 'formulate_Koopman_output_data_with_intersection': False }
#     dict_measurement_info_20.update(dict_simulation_parameters)
#     save_system(ls_data, dict_measurement_info = dict_measurement_info_20, SYSTEM_NO =20+n_delay_embedding)
#
#     # SYSTEM 30...39 - Output y3
#     dict_measurement_info_30 = {'state_measured': False, 'output_measured': True, 'n_delay_embedding': n_delay_embedding, 'ls_measured_output_indices': [2], 'ls_measured_state_indices': [], 'formulate_Koopman_output_data_with_intersection': False }
#     dict_measurement_info_30.update(dict_simulation_parameters)
#     save_system(ls_data, dict_measurement_info = dict_measurement_info_30, SYSTEM_NO =30+n_delay_embedding)
#
#     # SYSTEM 40...49 - Output y1,y2
#     dict_measurement_info_40 = {'state_measured': False, 'output_measured': True, 'n_delay_embedding': n_delay_embedding, 'ls_measured_output_indices': [0,1], 'ls_measured_state_indices': [], 'formulate_Koopman_output_data_with_intersection': False }
#     dict_measurement_info_40.update(dict_simulation_parameters)
#     save_system(ls_data, dict_measurement_info = dict_measurement_info_40, SYSTEM_NO =40+n_delay_embedding)
#
#     # SYSTEM 50...59 - Output y1,y3
#     dict_measurement_info_50 = {'state_measured': False, 'output_measured': True, 'n_delay_embedding': n_delay_embedding, 'ls_measured_output_indices': [0,2], 'ls_measured_state_indices': [], 'formulate_Koopman_output_data_with_intersection': False }
#     dict_measurement_info_50.update(dict_simulation_parameters)
#     save_system(ls_data, dict_measurement_info = dict_measurement_info_50, SYSTEM_NO =50+n_delay_embedding)
#
#     # SYSTEM 60...69 - Output y2,y3
#     dict_measurement_info_60 = {'state_measured': False, 'output_measured': True, 'n_delay_embedding': n_delay_embedding, 'ls_measured_output_indices': [1,2], 'ls_measured_state_indices': [], 'formulate_Koopman_output_data_with_intersection': False }
#     dict_measurement_info_60.update(dict_simulation_parameters)
#     save_system(ls_data, dict_measurement_info = dict_measurement_info_60, SYSTEM_NO =60+n_delay_embedding)
#
#     # SYSTEM 70...79 - Output y1,y2,y3
#     dict_measurement_info_70 = {'state_measured': False, 'output_measured': True, 'n_delay_embedding': n_delay_embedding, 'ls_measured_output_indices': [0,1,2], 'ls_measured_state_indices': [], 'formulate_Koopman_output_data_with_intersection': False }
#     dict_measurement_info_70.update(dict_simulation_parameters)
#     save_system(ls_data, dict_measurement_info = dict_measurement_info_70, SYSTEM_NO =70+n_delay_embedding)
#












## Bash Script Generation

dict_hp={}
dict_hp['ls_dict_size'] = [0,1,2,3,4,5]
dict_hp['ls_nn_layers'] = [3,4]
dict_hp['System_no'] = []
# dict_hp['System_no'] = dict_hp['System_no'] + list(range(1,7))
# dict_hp['System_no'] = dict_hp['System_no'] + list(range(11,13))
# dict_hp['System_no'] = dict_hp['System_no'] + list(range(21,25)) # gt
# dict_hp['System_no'] = dict_hp['System_no'] + [25,26,28,29] # mt # list(range(27,28)) # mt
dict_hp['System_no'] = dict_hp['System_no'] + list(range(31,40)) # mt
# dict_hp['System_no'] = dict_hp['System_no'] + list(range(41,50))
# dict_hp['System_no'] = dict_hp['System_no'] + list(range(51,60))
# dict_hp['System_no'] = dict_hp['System_no'] + list(range(61,70))
# dict_hp['System_no'] = dict_hp['System_no'] + list(range(71,80))

# system_running = 'goldentensor'
# system_running = 'optictensor'
system_running = 'microtensor'
# system_running = 'quantensor'

file = open('/Users/shara/Desktop/IEEETransactions_2022/' + system_running + '_run.sh','w')
if system_running in ['microtensor', 'quantensor', 'goldentensor']:
    ls_device = [' \'/cpu:0\' ']
# elif system_running in ['goldentensor', 'optictensor']:
#     ls_device = [' \'/cpu:0\' ', ' \'/gpu:0\' ', ' \'/gpu:1\' ', ' \'/gpu:2\' ', ' \'/gpu:3\' ']

# For each system of interest
dict_system_next_run = {}
for system_no in dict_hp['System_no']:
    # Create a MyRunInfo folder
    runinfo_folder = 'System_' + str(system_no) + '/MyRunInfo'
    if not os.path.exists(runinfo_folder):
        os.mkdir(runinfo_folder)
    if not os.path.exists(runinfo_folder + '/dummy_proxy.txt'):
        with open(runinfo_folder + '/dummy_proxy.txt', 'w') as f:
            f.write('This is created so that git does not experience an issue with')
    # Get the latest run number for each system # TODO - Check this part of the code
    try:
        ls_all_run_files = os.listdir('System_' + str(system_no) + '/MyMac')
        ls_run_numbers = [np.int(i[4:]) for i in ls_all_run_files if 'RUN_' in i]
        next_run = np.int(np.max(ls_run_numbers)) +1
    except:
        next_run = 0
    dict_system_next_run[system_no] = next_run

file.write('#!/bin/bash \n')
# file.write('rm nohup.out \n')
file.write('# Gen syntax: [interpreter] [code.py] [device] [sys_no] [run_no] [n_observables] [n_layers] [n_nodes] [write_to_file] \n')
ls_all_runs = []
n_devices = len(ls_device)
for system_no,n_x,n_l in product(dict_hp['System_no'],dict_hp['ls_dict_size'],dict_hp['ls_nn_layers']):
    run_number = dict_system_next_run[system_no]
    device_name = ls_device[np.mod(run_number,n_devices)]
    # Check if run file exists
    run_info_file = ' > System_' + str(system_no) + '/MyRunInfo/Run_' + str(run_number) + '.txt & \n'
    n_n = np.int(np.ceil(n_x*1.5))
    file.write('python3 deepDMD.py' + device_name + str(system_no) + ' ' + str(run_number) + ' ' + str(n_x) + ' ' + str(n_l) + ' ' + str(n_n) + run_info_file)
    if device_name == ls_device[-1]:
        file.write('wait\n')
    # Incrementing to the next run
    dict_system_next_run[system_no] = dict_system_next_run[system_no] + 1
file.write('echo "All sessions are complete" \n')
file.write('echo "=======================================================" \n')
file.close()


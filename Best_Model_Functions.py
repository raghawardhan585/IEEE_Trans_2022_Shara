import numpy as np
import pandas as pd
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from itertools import product
import random
import seaborn as sb
from sklearn.preprocessing import Normalizer, MinMaxScaler, StandardScaler
from sklearn.metrics import r2_score
import copy
import pickle
plt.rcParams["font.family"] = "Avenir"
plt.rcParams["mathtext.fontset"] = "cm"
plt.rcParams["font.size"] = 22
from Simulated_HighDimensional_Systems import *
import os
import shutil
import tensorflow as tf

dict_system_name = {1:'x1 - x2', 2: 'x1 - x2 - y1', 3:'x1 - x2 - x3 - x4', 4: 'x1 - x2 - x3 - x4 - y1 - y2', 5:'x1 - x2 - x3 - x4 - x5 - x6', 6: 'x1 - x2 - x3 - x4 - x5 - x6 - y1 - y2 - y3', 10: 'y1', 20: 'y2', 30: 'y3', 40: 'y1 - y2', 50: 'y1 - y3', 60: 'y2 - y3', 70: 'y1 - y2 - y3'}


def get_dict_param(run_folder_name_curr,SYS_NO,sess):
    dict_p = {}
    saver = tf.compat.v1.train.import_meta_graph(run_folder_name_curr + '/System_' + str(SYS_NO) + '_DeepDMDdata_Scaled.pickle.ckpt.meta', clear_devices=True)
    saver.restore(sess, tf.train.latest_checkpoint(run_folder_name_curr))
    try:
        psixpT = tf.get_collection('psixpT')[0]
        psixfT = tf.get_collection('psixfT')[0]
        xpT_feed = tf.get_collection('xpT_feed')[0]
        xfT_feed = tf.get_collection('xfT_feed')[0]
        KxT = tf.get_collection('KxT')[0]
        KxT_num = sess.run(KxT)
        dict_p['psixpT'] = psixpT
        dict_p['psixfT'] = psixfT
        dict_p['xpT_feed'] = xpT_feed
        dict_p['xfT_feed'] = xfT_feed
        dict_p['KxT_num'] = KxT_num
    except:
        print('State info not found')
    try:
        ypT_feed = tf.get_collection('ypT_feed')[0]
        yfT_feed = tf.get_collection('yfT_feed')[0]
        dict_p['ypT_feed'] = ypT_feed
        dict_p['yfT_feed'] = yfT_feed
        WhT = tf.get_collection('WhT')[0]
        WhT_num = sess.run(WhT)
        dict_p['WhT_num'] = WhT_num
    except:
        print('No output info found')
    return dict_p
def get_processed_run_info(df_results):
    dict_out = {}
    for system in list(df_results['system'].unique()):
        df_sys = df_results.loc[df_results['system'] == system,['system','system_no','run_no']]
        for system_no in list(df_sys['system_no'].unique()):# This is an indicator of the delay embedding
            dict_out[system_no] = list(df_sys.loc[df_sys['system_no']== system_no, 'run_no'])
    return dict_out
def resolve_complex_right_eigenvalues(E, W):
    eval = np.diag(E)
    comp_modes = []
    comp_modes_conj = []
    for i1 in range(E.shape[0]):
        if np.imag(E[i1, i1]) != 0:
            print(i1)
            # Find the complex conjugate
            for i2 in range(i1 + 1, E.shape[0]):
                if eval[i2] == eval[i1].conj():
                    break
            # i1 and i2 are the indices of the complex conjugate eigenvalues
            comp_modes.append(i1)
            comp_modes_conj.append(i2)
            E[i1, i1] = np.real(eval[i1])
            E[i2, i2] = np.real(eval[i1])
            E[i1, i2] = np.imag(eval[i1])
            E[i2, i1] = - np.imag(eval[i1])
            u1 = copy.deepcopy(np.real(W[:, i1:i1 + 1]))
            w1 = copy.deepcopy(np.imag(W[:, i1:i1 + 1]))
            W[:, i1:i1 + 1] = u1
            W[:, i2:i2 + 1] = w1
    E_out = np.real(E)
    W_out = np.real(W)
    return E_out, W_out, comp_modes, comp_modes_conj






# Initiation
try:
    with open('model_statistics_dataframe.pickle', 'rb') as handle:
        df_results = pickle.load(handle)
    dict_model_stats = df_results.T.to_dict()
    dict_processed_runs = get_processed_run_info(df_results)
    model_no = np.max(df_results.index) + 1
    STATE_NEW_RESULT = False
except:
    dict_model_stats = {}
    dict_processed_runs = {}
    model_no = 0
    STATE_NEW_RESULT = True



for SYSTEM_NO in dict_system_name.keys():
    if SYSTEM_NO >= 10: # Detect a delay embedded system
        # Get all the delay embeddings
        ls_delay_embeddings = [sys_name[8:] for sys_name in os.listdir() if sys_name[0:8] == 'System_'+ str(np.int(np.floor(SYSTEM_NO/10)))]
        ls_delay_embeddings = np.sort([np.int(i) for i in ls_delay_embeddings if not i == ''])
        # Load the dataset
        SYSTEM_NO = np.int(np.floor(SYSTEM_NO/10)*10)
        simulation_data_file = 'System_' + str(SYSTEM_NO + 1) + '/System_' + str(SYSTEM_NO + 1) + '_SimulatedData.pickle'
        with open(simulation_data_file, 'rb') as handle:
            ls_data = pickle.load(handle)
        # Iterate through each delay embedding
        for n_delay_embedding in ls_delay_embeddings:
            delay_embedded_system_no = SYSTEM_NO + n_delay_embedding
            system_runs_folder = 'System_' + str(delay_embedded_system_no) + '/MyMac'
            # Load the simulation info [required to convert the data to the required format]
            simulation_datainfo_file = 'System_' + str(delay_embedded_system_no) + '/System_' + str(delay_embedded_system_no) + '_SimulatedDataInfo.pickle'
            with open(simulation_datainfo_file, 'rb') as handle:
                dict_data_info = pickle.load(handle)
            n_outputs = len(dict_data_info['ls_measured_output_indices'])
            # Load the scalers
            scaler_file = 'System_' + str(delay_embedded_system_no) + '/System_' + str(delay_embedded_system_no) + '_DataScaler.pickle'
            with open(scaler_file, 'rb') as handle:
                dict_Scaler = pickle.load(handle)
            # Get the exhaustive list of runs
            ls_runs = np.sort([np.int(items[4:]) for items in os.listdir(system_runs_folder) if items[0:4] == 'RUN_'])
            # Time Reduction by processing only unprocessed runs
            if delay_embedded_system_no in dict_processed_runs.keys():
                ls_runs = list(set(ls_runs) - set(dict_processed_runs[delay_embedded_system_no]))


            # Iterate through each of the runs and each dataset
            for run_i in ls_runs:
                # Load the tensorflow environment
                sess_i = tf.InteractiveSession()
                run_folder_name_i = 'System_' + str(delay_embedded_system_no) + '/MyMac/RUN_' + str(run_i)
                dict_model_i = get_dict_param(run_folder_name_i, delay_embedded_system_no, sess_i)
                # Load the hyperparameters for each run
                with open(run_folder_name_i + '/dict_hyperparameters.pickle', 'rb') as handle:
                    dict_run_i_info = pickle.load(handle)
                # Iterate through each dataset
                ls_data_pred = []
                for data_i in ls_data:
                    # Find the initial condition
                    x0 = data_i['YT'][0:n_delay_embedding, dict_data_info['ls_measured_output_indices']].T.reshape(1, -1)
                    # Organize the data
                    XT_true = np.empty((0, x0.shape[1]))
                    if dict_data_info['formulate_Koopman_output_data_with_intersection']:
                        for j in range(n_delay_embedding, data_i['YT'].shape[0]):
                            XT_true = np.concatenate([XT_true, data_i['YT'][j - n_delay_embedding:j,
                                                               dict_data_info['ls_measured_output_indices']].T.reshape(1,-1)],axis=0)
                    else:
                        n_delay_embedded_points = np.int(np.floor(data_i['YT'].shape[0] / n_delay_embedding))
                        for j in range(n_delay_embedded_points):
                            XT_true = np.concatenate([XT_true, data_i['YT'][j * n_delay_embedding:(j + 1) * n_delay_embedding,
                                                           dict_data_info['ls_measured_output_indices']].T.reshape(1,-1)], axis=0)
                    # Scale the data
                    x0s = dict_Scaler['XT'].transform(x0)
                    XTs_true = dict_Scaler['XT'].transform(XT_true)
                    # Generate the observables
                    psiXT_true = dict_model_i['psixpT'].eval(feed_dict={dict_model_i['xpT_feed']: XTs_true})
                    # Generate 1-step predictions
                    psiXT_est_1step = np.concatenate([psiXT_true[0:1,:],np.matmul(psiXT_true[0:-1, :], dict_model_i['KxT_num'])],axis=0)
                    # Generate n-step predictions
                    psiXT_est_nstep = dict_model_i['psixpT'].eval(feed_dict={dict_model_i['xpT_feed']: x0s})
                    for step_i in range(XT_true.shape[0] - 1):
                        psiXT_est_nstep = np.concatenate([psiXT_est_nstep, np.matmul(psiXT_est_nstep[-1:, :], dict_model_i['KxT_num'])], axis=0)
                    # Get the states back from the observables
                    XTs_est_1step = psiXT_est_1step[:, 0:x0.shape[1]]
                    XTs_est_nstep = psiXT_est_nstep[:, 0:x0.shape[1]]
                    # Reverse scale the data
                    XT_est_1step = dict_Scaler['XT'].inverse_transform(XTs_est_1step)
                    XT_est_nstep = dict_Scaler['XT'].inverse_transform(XTs_est_nstep)
                    # Reverse the delay embedding
                    YT_true = np.empty((0, n_outputs))
                    YT_est_1step = np.empty((0, n_outputs))
                    YT_est_nstep = np.empty((0, n_outputs))
                    # YT_true = XT_true[0:,:].reshape(n_outputs,-1).T
                    # YT_est_1step = XT_est_1step[0:,:].reshape(n_outputs,-1).T
                    # YT_est_nstep = XT_est_nstep[0:,:].reshape(n_outputs,-1).T
                    if dict_data_info['formulate_Koopman_output_data_with_intersection']:
                        for j in range(XT_true.shape[0]):
                            YT_true = np.concatenate([YT_true, XT_true[j,:].reshape(n_outputs,-1).T[-1:,:]], axis=0)
                            YT_est_1step = np.concatenate([YT_est_1step, XT_est_1step[j,:].reshape(n_outputs, -1).T[-1:,:]], axis=0)
                            YT_est_nstep = np.concatenate([YT_est_nstep, XT_est_nstep[j,:].reshape(n_outputs, -1).T[-1:,:]], axis=0)
                    else:
                        for j in range(XT_true.shape[0]):
                            YT_true = np.concatenate([YT_true, XT_true[j,:].reshape(n_outputs,-1).T], axis=0)
                            YT_est_1step = np.concatenate([YT_est_1step, XT_est_1step[j,:].reshape(n_outputs, -1).T], axis=0)
                            YT_est_nstep = np.concatenate([YT_est_nstep, XT_est_nstep[j,:].reshape(n_outputs, -1).T], axis=0)
                    dict_data_pred_i = {
                        'YT_true': YT_true,
                        'YT_est_1step': YT_est_1step,
                        'YT_est_nstep': YT_est_nstep,
                        'psiXT_true': XTs_true,
                        'psiXT_est_1step': psiXT_est_1step,
                        'psiXT_est_nstep': psiXT_est_nstep
                    }
                    ls_data_pred.append(dict_data_pred_i)
                # Record the run statistics
                # *Assumed training, validation and test are split equally
                dict_model_stats[model_no] = {'system': SYSTEM_NO, 'n_delay_embedding': n_delay_embedding, 'system_no': delay_embedded_system_no, 'run_no': run_i, 'total_observables': n_outputs*n_delay_embedding + dict_run_i_info['x_obs']}
                dict_model_stats[model_no].update(dict_run_i_info)
                # Split the data as training, validaiton and test
                dict_data_run_i = {}
                for item in ['train','valid','test']:
                    dict_data_run_i[item] = {'true': np.empty((0,n_outputs)),'1-step': np.empty((0,n_outputs)),'n-step': np.empty((0,n_outputs))}
                n_datasets = len(ls_data_pred)
                for i in range(n_datasets):
                    if i <= (n_datasets/3):
                        item = 'train'
                    elif i <= (2*n_datasets/3):
                        item = 'valid'
                    else:
                        item = 'test'
                    dict_data_run_i[item]['true'] = np.concatenate([dict_data_run_i[item]['true'], ls_data_pred[i]['YT_true']],axis=0)
                    dict_data_run_i[item]['1-step'] = np.concatenate([dict_data_run_i[item]['1-step'], ls_data_pred[i]['YT_est_1step']], axis=0)
                    dict_data_run_i[item]['n-step'] = np.concatenate([dict_data_run_i[item]['n-step'], ls_data_pred[i]['YT_est_nstep']], axis=0)
                # Get the full model training, validation and test scores for 1-step and n-step
                for item in ['train','valid','test']:
                    dict_model_stats[model_no]['r2_' + str(item) + '_1step'] = r2_score(dict_data_run_i[item]['true'],dict_data_run_i[item]['1-step'])
                    dict_model_stats[model_no]['r2_' + str(item) + '_nstep'] = r2_score(dict_data_run_i[item]['true'],dict_data_run_i[item]['n-step'])
                # # Get the 1-step and n-step prediction errors for individual outputs as well
                # dict_data_run_i_all = {}
                # for item in ['true','1-step','n-step']:
                #     dict_data_run_i_all[item] = np.concatenate([np.concatenate([dict_data_run_i['train'][item],dict_data_run_i['valid'][item]],axis=0),dict_data_run_i['test'][item]],axis=0)
                # for i in range(ls_data[0]['YT'].shape[1]):
                #     if i in dict_data_info['ls_measured_output_indices']:
                #         dict_model_stats[model_no]['r2_y' + str(i)+'_1step'] = r2_score(dict_data_run_i_all['true'],dict_data_run_i_all['1-step'])
                #         dict_model_stats[model_no]['r2_y' + str(i) + '_nstep'] = r2_score(dict_data_run_i_all['true'],dict_data_run_i_all['n-step'])
                #     else:
                #         dict_model_stats[model_no]['r2_y' + str(i) + '_1step'] = np.nan
                #         dict_model_stats[model_no]['r2_y' + str(i) + '_nstep'] = np.nan
                model_no = model_no + 1
                # Undo the tensorflow session
                tf.reset_default_graph()
                sess_i.close()
    else: # State included system
        # Load the dataset
        simulation_data_file = 'System_' + str(SYSTEM_NO) + '/System_' + str(SYSTEM_NO) + '_SimulatedData.pickle'
        with open(simulation_data_file, 'rb') as handle:
            ls_data = pickle.load(handle)
        system_runs_folder = 'System_' + str(SYSTEM_NO) + '/MyMac'
        # Load the simulation info [required to convert the data to the required format]
        simulation_datainfo_file = 'System_' + str(SYSTEM_NO) + '/System_' + str(SYSTEM_NO) + '_SimulatedDataInfo.pickle'
        with open(simulation_datainfo_file, 'rb') as handle:
            dict_data_info = pickle.load(handle)
        n_states = len(dict_data_info['ls_measured_state_indices'])
        n_outputs = len(dict_data_info['ls_measured_output_indices'])
        # Check if output is available
        if n_outputs == 0:
            with_output = False
        else:
            with_output = True
        # Load the scalers
        scaler_file = 'System_' + str(SYSTEM_NO) + '/System_' + str(SYSTEM_NO) + '_DataScaler.pickle'
        with open(scaler_file, 'rb') as handle:
            dict_Scaler = pickle.load(handle)
        # Get the exhaustive list of runs
        try:
            ls_runs = np.sort([np.int(items[4:]) for items in os.listdir(system_runs_folder) if items[0:4] == 'RUN_'])
        except:
            continue
        # Time Reduction by processing only unprocessed runs
        if SYSTEM_NO in dict_processed_runs.keys():
            ls_runs = list(set(ls_runs) - set(dict_processed_runs[SYSTEM_NO]))

        # Iterate through each of the runs and each dataset
        for run_i in ls_runs:
            # Load the tensorflow environment
            sess_i = tf.InteractiveSession()
            run_folder_name_i = 'System_' + str(SYSTEM_NO) + '/MyMac/RUN_' + str(run_i)
            dict_model_i = get_dict_param(run_folder_name_i, SYSTEM_NO, sess_i)
            # Load the hyperparameters for each run
            with open(run_folder_name_i + '/dict_hyperparameters.pickle', 'rb') as handle:
                dict_run_i_info = pickle.load(handle)

            # Iterate through each dataset
            ls_data_pred = []
            for data_i in ls_data:
                # Data
                XT_true = data_i['XT'][:, dict_data_info['ls_measured_state_indices']]
                # Scale the data
                XTs_true = dict_Scaler['XT'].transform(XT_true)

                # Generate the observables
                psiXT_true = dict_model_i['psixpT'].eval(feed_dict={dict_model_i['xpT_feed']: XTs_true})
                # Generate 1-step predictions
                psiXT_est_1step = np.concatenate([psiXT_true[0:1,:],np.matmul(psiXT_true[0:-1, :], dict_model_i['KxT_num'])],axis=0)
                # Generate n-step predictions
                psiXT_est_nstep = psiXT_true[0:1,:]
                for step_i in range(XT_true.shape[0] - 1):
                    psiXT_est_nstep = np.concatenate([psiXT_est_nstep, psiXT_est_nstep[-1:, :] @ dict_model_i['KxT_num']], axis=0)
                # Get the states back from the observables
                XTs_est_1step = psiXT_est_1step[:, 0:n_states]
                XTs_est_nstep = psiXT_est_nstep[:, 0:n_states]
                # Reverse scale the data
                XT_est_1step = dict_Scaler['XT'].inverse_transform(XTs_est_1step)
                XT_est_nstep = dict_Scaler['XT'].inverse_transform(XTs_est_nstep)
                dict_data_pred_i = {
                    'XT_true': XT_true,
                    'XT_est_1step': XT_est_1step,
                    'XT_est_nstep': XT_est_nstep,
                    'psiXT_true': psiXT_true,
                    'psiXT_est_1step': psiXT_est_1step,
                    'psiXT_est_nstep': psiXT_est_nstep
                }
                if with_output:
                    YT_true = data_i['YT'][:, dict_data_info['ls_measured_output_indices']]
                    # Get the estimate of the outputs
                    YTs_est_1step = psiXT_est_1step @ dict_model_i['WhT_num'] # 1 - step
                    YTs_est_nstep = psiXT_est_nstep @ dict_model_i['WhT_num'] # n - step
                    # Reverse scale the output data
                    YT_est_1step = dict_Scaler['YT'].inverse_transform(YTs_est_1step)
                    YT_est_nstep = dict_Scaler['YT'].inverse_transform(YTs_est_nstep)
                    dict_data_pred_i['YT_true'] = YT_true
                    dict_data_pred_i['YT_est_1step'] = YT_est_1step
                    dict_data_pred_i['YT_est_nstep'] = YT_est_nstep
                else:
                    dict_data_pred_i['YT_true'] = np.nan
                    dict_data_pred_i['YT_est_1step'] = np.nan
                    dict_data_pred_i['YT_est_nstep'] = np.nan
                ls_data_pred.append(dict_data_pred_i)

            # Record the run statistics
            # *Assumed training, validation and test are split equally
            dict_model_stats[model_no] = {'system': SYSTEM_NO, 'n_delay_embedding': 1, 'system_no': SYSTEM_NO, 'run_no': run_i, 'total_observables': n_states + dict_run_i_info['x_obs']}
            dict_model_stats[model_no].update(dict_run_i_info)
            # Split the data as training, validaiton and test
            dict_data_run_i = {}
            for item in ['train','valid','test']:
                dict_data_run_i[item] = {'x_true': np.empty((0,n_states)),'x_1-step': np.empty((0,n_states)),'x_n-step': np.empty((0,n_states)), 'y_true': np.empty((0,n_outputs)),'y_1-step': np.empty((0,n_outputs)),'y_n-step': np.empty((0,n_outputs))}
            n_datasets = len(ls_data_pred)
            for i in range(n_datasets):
                if i <= (n_datasets/3):
                    item = 'train'
                elif i <= (2*n_datasets/3):
                    item = 'valid'
                else:
                    item = 'test'
                dict_data_run_i[item]['x_true'] = np.concatenate([dict_data_run_i[item]['x_true'], ls_data_pred[i]['XT_true']],axis=0)
                dict_data_run_i[item]['x_1-step'] = np.concatenate([dict_data_run_i[item]['x_1-step'], ls_data_pred[i]['XT_est_1step']], axis=0)
                dict_data_run_i[item]['x_n-step'] = np.concatenate([dict_data_run_i[item]['x_n-step'], ls_data_pred[i]['XT_est_nstep']], axis=0)
                if with_output:
                    dict_data_run_i[item]['y_true'] = np.concatenate([dict_data_run_i[item]['y_true'], ls_data_pred[i]['YT_true']], axis=0)
                    dict_data_run_i[item]['y_1-step'] = np.concatenate([dict_data_run_i[item]['y_1-step'], ls_data_pred[i]['YT_est_1step']], axis=0)
                    dict_data_run_i[item]['y_n-step'] = np.concatenate([dict_data_run_i[item]['y_n-step'], ls_data_pred[i]['YT_est_nstep']], axis=0)
            # Get the full model training, validation and test scores for 1-step and n-step
            for item in ['train','valid','test']:
                if with_output:
                    data_intermediate_true = np.concatenate([dict_data_run_i[item]['x_true'], dict_data_run_i[item]['y_true']], axis = 1)
                    data_intermediate_1step = np.concatenate([dict_data_run_i[item]['x_1-step'], dict_data_run_i[item]['y_1-step']], axis=1)
                    data_intermediate_nstep = np.concatenate([dict_data_run_i[item]['x_n-step'], dict_data_run_i[item]['y_n-step']], axis=1)
                    dict_model_stats[model_no]['r2_' + str(item) + '_1step'] = r2_score(data_intermediate_true, data_intermediate_1step)
                    dict_model_stats[model_no]['r2_' + str(item) + '_nstep'] = r2_score(data_intermediate_true, data_intermediate_nstep)
                else:
                    dict_model_stats[model_no]['r2_' + str(item) + '_1step'] = r2_score(dict_data_run_i[item]['x_true'],dict_data_run_i[item]['x_1-step'])
                    dict_model_stats[model_no]['r2_' + str(item) + '_nstep'] = r2_score(dict_data_run_i[item]['x_true'],dict_data_run_i[item]['x_n-step'])
            # TODO Get the 1-step and n-step prediction errors for states
            # Let us evaluate if we need it sometime later
            # TODO Get the 1-step and n-step prediction errors for individual outputs as well
            # if with_output:
            #     dict_data_run_i_all = {}
            #     for item in ['true','1-step','n-step']:
            #         dict_data_run_i_all[item] = np.concatenate([np.concatenate([dict_data_run_i['train'][item],dict_data_run_i['valid'][item]],axis=0),dict_data_run_i['test'][item]],axis=0)
            #     for i in range(ls_data[0]['YT'].shape[1]):
            #         if i in dict_data_info['ls_measured_output_indices']:
            #             dict_model_stats[model_no]['r2_y' + str(i)+'_1step'] = r2_score(dict_data_run_i_all['true'],dict_data_run_i_all['1-step'])
            #             dict_model_stats[model_no]['r2_y' + str(i) + '_nstep'] = r2_score(dict_data_run_i_all['true'],dict_data_run_i_all['n-step'])
            #         else:
            #             dict_model_stats[model_no]['r2_y' + str(i) + '_1step'] = np.nan
            #             dict_model_stats[model_no]['r2_y' + str(i) + '_nstep'] = np.nan
            model_no = model_no + 1
            # Undo the tensorflow session
            tf.reset_default_graph()
            sess_i.close()


df_results = pd.DataFrame(dict_model_stats).T

# Export the dataframe of results
with open('model_statistics_dataframe.pickle','wb') as handle:
    pickle.dump(df_results,handle)




# plt.figure()
# plt.plot(df_results['total_observables'], df_results['r2_valid_nstep'],'.')
# plt.xlabel('# Observables')
# plt.ylabel('r2_score')
# plt.title('System: ' + dict_system_name[SYSTEM_NO])
# plt.ylim([0,1.05])
# plt.show()
#
# plt.figure(figsize = (10,8))
# for x_obs in range(np.max(df_results['x_obs'])):
#     df_i = df_results.loc[df_results['x_obs'] == x_obs,:]
#     plt.plot(df_i['n_delay_embedding'], df_i['r2_valid_nstep'],'.', markersize = 50-3*x_obs, label=str(x_obs) + ' obs')
# plt.xlabel('# Delay Embeddings')
# plt.ylabel('r2_score')
# plt.legend(ncol=2)
# plt.title('System: ' + dict_system_name[SYSTEM_NO])
# plt.ylim([0,1.05])
# plt.show()

## Find the optimal models for each system

dict_opt_models = {}
for system in list(df_results['system'].unique()):
    # Narrow down to the system of interest
    df_sys = df_results.loc[df_results['system']==system,:]
    # Filter all the data with greater than 98% r2 in training and validation
    if df_sys.loc[df_sys['r2_train_nstep']>0.98,:].shape[0]>0 and df_sys.loc[df_sys['r2_valid_nstep']>0.98,:].shape[0]>0:
        df_sys = df_sys.loc[df_sys['r2_train_nstep']>0.98,:]
        df_sys = df_sys.loc[df_sys['r2_valid_nstep']>0.98,:]
        # Filter all the data with the minimum number of observables
        n_obs_min = np.min(df_sys['total_observables'])
        df_sys = df_sys.loc[df_sys['total_observables']==n_obs_min,:]
    # Narrow down to the minimal error
    min_error = np.min((df_sys['r2_train_nstep'] + df_sys['r2_valid_nstep'])/2)
    df_sys = df_sys.loc[(df_sys['r2_train_nstep'] + df_sys['r2_valid_nstep'])/2 == min_error,:]
    dict_opt_models[system] = {}
    dict_opt_models[system]['system_no'] = np.int(df_sys.iloc[0:1,:].loc[:,'system_no'].to_numpy(dtype=np.int))
    if system>=10:
        dict_opt_models[system]['n_delay_embedding'] = np.int(df_sys.iloc[0:1,:].loc[:,'n_delay_embedding'].to_numpy(dtype=np.int))
    else:
        dict_opt_models[system]['n_delay_embedding'] = 1
    dict_opt_models[system]['run_no'] = np.int(df_sys.iloc[0:1,:].loc[:,'run_no'].to_numpy(dtype=np.int))
    dict_opt_models[system]['r2_train_nstep'] = np.round(np.float(df_sys['r2_train_nstep']),2)
    dict_opt_models[system]['r2_valid_nstep'] = np.round(np.float(df_sys['r2_valid_nstep']),2)
dict_opt_models

##
dict_opt_models = {}
for system in list(df_results['system'].unique()):
    # Narrow down to the system of interest
    df_sys = df_results.loc[df_results['system']==system,:]
    # Narrow down to the minimal error
    min_error = np.min((df_sys['r2_train_nstep'] + df_sys['r2_valid_nstep'])/2)
    df_sys = df_sys.loc[(df_sys['r2_train_nstep'] + df_sys['r2_valid_nstep'])/2 == min_error,:]
    dict_opt_models[system] = {}
    dict_opt_models[system]['system_no'] = np.int(df_sys.iloc[0:1,:].loc[:,'system_no'].to_numpy(dtype=np.int))
    dict_opt_models[system]['n_delay_embedding'] = np.int(df_sys.iloc[0:1,:].loc[:,'n_delay_embedding'].to_numpy(dtype=np.int))
    dict_opt_models[system]['run_no'] = np.int(df_sys.iloc[0:1,:].loc[:,'run_no'].to_numpy(dtype=np.int))

## Correlation between the eigenfunctions of the two systems
for system1 in [5]:
    # system1 = 30
    system2 = 70

# maximum delay estimation
if system1>10:
    delay1 = 1
    sys_meas1 = 'x'
else:
    delay1 = np.int(np.mod(dict_opt_models[system1]['system_no'],10))
    sys_meas1 = 'y'
if system2>10:
    delay2 = 1
    sys_meas2 = 'x'
else:
    delay2 = np.int(np.mod(dict_opt_models[system2]['system_no'],10))
    sys_meas2 = 'y'
max_delay = np.max([delay1,delay2])



system_i = system1
sys_meas_i = sys_meas1
delay_i = delay1

# Load the original unscaled data [The simulated data is common to both]
simulation_data_file = 'System_' + str(dict_opt_models[system_i]['system_no']) + '/System_' + str(dict_opt_models[system_i]['system_no']) + '_SimulatedData.pickle'
with open(simulation_data_file, 'rb') as handle:
    ls_data = pickle.load(handle)

# Delay embedding
sys_infofile_i = 'System_' + str(dict_opt_models[system1]['system_no']) + '/System_' + str(dict_opt_models[system1]['system_no']) + '_SimulatedDataInfo.pickle'
with open(sys_infofile_i, 'rb') as handle:
    sys_info_i = pickle.load(handle)
if system_i <10:
    n_delay_embed_i = 1
    XT_i = np.empty((0, ls_data[0]['XT'].shape[1]))
else:
    n_delay_embed_i = np.int(np.mod(dict_opt_models[system_i]['system_no'], 10))
    XT_i = np.empty((0, n_delay_embed_i * len(sys_info_i['ls_measured_output_indices'])))
















# Identify the delay embedding for each model
n_delay_embed1 = np.int(np.mod(dict_opt_models[system1]['system_no'],10))
n_delay_embed2 = np.int(np.mod(dict_opt_models[system2]['system_no'],10))

# Load the original unscaled data
sys_infofile1 = 'System_' + str(dict_opt_models[system1]['system_no']) + '/System_' + str(dict_opt_models[system1]['system_no']) + '_SimulatedDataInfo.pickle'
with open(sys_infofile1, 'rb') as handle:
    sys_info1 = pickle.load(handle)
sys_infofile2 = 'System_' + str(dict_opt_models[system2]['system_no']) + '/System_' + str(dict_opt_models[system2]['system_no']) + '_SimulatedDataInfo.pickle'
with open(sys_infofile2, 'rb') as handle:
    sys_info2 = pickle.load(handle)


# Organize the data for both


XT1 = np.empty((0,n_delay_embed1*len(sys_info1['ls_measured_output_indices'])))
XT2 = np.empty((0,n_delay_embed2*len(sys_info2['ls_measured_output_indices'])))
for data_i in ls_data:
    for j in range(data_i['YT'].shape[0]- np.max([n_delay_embed1,n_delay_embed2])):
        XT1 = np.concatenate([XT1, data_i['YT'][j:(j+n_delay_embed1),sys_info1[ 'ls_measured_output_indices']].T.reshape(1,-1)],axis=0)
        XT2 = np.concatenate([XT2, data_i['YT'][j:(j + n_delay_embed2), sys_info2['ls_measured_output_indices']].T.reshape(1, -1)],axis=0)

# Scale the data
scaler_file1 = 'System_' + str(dict_opt_models[system1]['system_no']) + '/System_' + str(dict_opt_models[system1]['system_no']) + '_DataScaler.pickle'
with open(scaler_file1, 'rb') as handle:
    scaler1 = pickle.load(handle)
XT1s = scaler1['XT'].transform(XT1)
scaler_file2 = 'System_' + str(dict_opt_models[system2]['system_no']) + '/System_' + str(dict_opt_models[system2]['system_no']) + '_DataScaler.pickle'
with open(scaler_file2, 'rb') as handle:
    scaler2 = pickle.load(handle)
XT2s = scaler2['XT'].transform(XT2)

# Find the observables
sess1 = tf.InteractiveSession()
run_folder1 = 'System_' + str(dict_opt_models[system1]['system_no']) + '/MyMac/RUN_' + str(dict_opt_models[system1]['run_no'])
dict_model1 = get_dict_param(run_folder1, dict_opt_models[system1]['system_no'],sess1)
psiXT1 = dict_model1['psixpT'].eval(feed_dict={dict_model1['xpT_feed']: XT1s})
K1 = dict_model1['KxT_num'].T
tf.reset_default_graph()
sess1.close()

sess2 = tf.InteractiveSession()
run_folder2 = 'System_' + str(dict_opt_models[system2]['system_no']) + '/MyMac/RUN_' + str(dict_opt_models[system2]['run_no'])
dict_model2 = get_dict_param(run_folder2, dict_opt_models[system2]['system_no'],sess2)
psiXT2 = dict_model2['psixpT'].eval(feed_dict={dict_model2['xpT_feed']: XT2s})
K2 = dict_model2['KxT_num'].T
tf.reset_default_graph()
sess2.close()

# Compute all the eigenfunctions for the various datapoints
eval1, W1 = np.linalg.eig(K1)
E1 = np.diag(eval1)
E1, W1, comp_modes1, comp_modes_conj1 = resolve_complex_right_eigenvalues(E1, W1)
Winv1 = np.linalg.inv(W1)
Phi1 = np.matmul(Winv1,psiXT1.T)

eval2, W2 = np.linalg.eig(K2)
E2 = np.diag(eval2)
E2, W2, comp_modes2, comp_modes_conj2 = resolve_complex_right_eigenvalues(E2, W2)
Winv2 = np.linalg.inv(W2)
Phi2 = np.matmul(Winv2,psiXT2.T)

# Cross correlation
np_out = np.corrcoef(np.concatenate([Phi1,Phi2],axis=0))
np_out = np.abs(np_out[0:Phi1.shape[0]-1,Phi1.shape[0]:-1])
np_out[np_out <=0.8]=0
a = sb.heatmap(np.abs(np_out),cmap='Blues')
b, t = a.axes.get_ylim()  # discover the values for bottom and top
b += 0.5  # Add 0.5 to the bottom
t -= 0.5  # Subtract 0.5 from the top
a.axes.set_ylim(b, t)
plt.ylabel('System ' + dict_system_name[system1])
plt.xlabel('System ' + dict_system_name[system2])
plt.show()



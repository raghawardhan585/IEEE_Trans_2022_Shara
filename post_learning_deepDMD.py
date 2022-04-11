import numpy as np
import pandas as pd
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from itertools import product
import random
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


# Next set of functions requried

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
        WhT = tf.get_collection('WhT')[0];
        WhT_num = sess.run(WhT)
        dict_p['WhT_num'] = WhT_num
    except:
        print('No output info found')
    return dict_p



##
sess = tf.InteractiveSession()
SYSTEM_NO = 12
RUN_NO = 1
run_folder_name = 'System_' + str(SYSTEM_NO) + '/MyMac/RUN_' + str(RUN_NO)

dict_model = get_dict_param(run_folder_name,SYSTEM_NO,sess)

# Load the data
simulation_data_file = 'System_' + str(SYSTEM_NO) + '/System_' + str(SYSTEM_NO) + '_SimulatedData.pickle'
simulation_datainfo_file = 'System_' + str(SYSTEM_NO) + '/System_' + str(SYSTEM_NO) + '_SimulatedDataInfo.pickle'
scaler_file = 'System_' + str(SYSTEM_NO) + '/System_' + str(SYSTEM_NO) + '_DataScaler.pickle'
with open(simulation_data_file , 'rb') as handle:
    ls_data = pickle.load(handle)
with open(simulation_datainfo_file , 'rb') as handle:
    dict_data_info = pickle.load(handle)
with open(scaler_file , 'rb') as handle:
    dict_Scaler = pickle.load(handle)

# Generate n-step predictions for all the curves
ls_data_pred =[]
for data_i in ls_data:
    dict_data_i = {}
    # Generate the initial condition and the true dataset
    if dict_data_info['state_measured']:
        x0 = data_i['XT'][0:1,:]
        XT_true = data_i['XT']
    elif dict_data_info['output_measured']:
        n_embeddings = dict_data_info['n_delay_embedding']
        x0 = data_i['YT'][0:n_embeddings,dict_data_info['ls_measured_output_indices']].T.reshape(1,-1)
        XT_true = np.empty((0,x0.shape[1]))
        if dict_data_info['formulate_Koopman_output_data_with_intersection']:
            for j in range(n_embeddings,data_i['YT'].shape[0]):
                XT_true = np.concatenate([XT_true, data_i['YT'][j - n_embeddings:j,dict_data_info['ls_measured_output_indices']].T.reshape(1, -1)], axis=0)
        else:
            n_delay_embedded_points = np.int(np.floor(data_i['YT'].shape[0]/n_embeddings))
            for j in range(n_delay_embedded_points):
                XT_true = np.concatenate([XT_true, data_i['YT'][j*n_embeddings:(j+1)*n_embeddings,dict_data_info['ls_measured_output_indices']].T.reshape(1, -1)], axis=0)
    # Scale the x0
    x0s = dict_Scaler['XT'].transform(x0)
    XTs_true = dict_Scaler['XT'].transform(XT_true)
    psiXT_true = dict_model['psixpT'].eval(feed_dict={dict_model['xpT_feed']: XTs_true})
    # Do n-step prediction on the initial condition
    psiXT_est = dict_model['psixpT'].eval(feed_dict = {dict_model['xpT_feed']: x0s})
    for step_i in range(XT_true.shape[0]-1):
        psiXT_est = np.concatenate([psiXT_est, np.matmul(psiXT_est[-1:,:],dict_model['KxT_num'])],axis=0)
    XTs_est = psiXT_est[:,0:x0.shape[1]]
    XT_est = dict_Scaler['XT'].inverse_transform(XTs_est)
    dict_data_i = {'XT_true': XT_true, 'XT_est': XT_est, 'psiXT_true': psiXT_true, 'psiXT_est': psiXT_est, 'XTs_true': XTs_true, 'XTs_est': XTs_est,}
    if dict_data_info['state_measured'] and dict_data_info['output_measured']:
        YT_true = data_i['YT'][:,dict_data_info['ls_measured_output_indices']]
        YTs_est = np.matmul(psiXT_est, dict_model['WhT_num'])
        dict_data_i['YT_true'] = YT_true
        dict_data_i['YTs_true'] = dict_Scaler['YT'].transform(YT_true)
        dict_data_i['YTs_est'] = YTs_est
        dict_data_i['YT_est'] = dict_Scaler['YT'].inverse_transform(YTs_est)
    ls_data_pred.append(dict_data_i)

#
data_sim_index = 10
t = dict_data_info['t']
plt.figure()
plt.plot(ls_data_pred[data_sim_index]['XT_true'].reshape(-1), '.', linewidth=3, color='tab:blue')
plt.plot(ls_data_pred[data_sim_index]['XT_est'].reshape(-1), color='tab:blue')
plt.show()

tf.reset_default_graph()
sess.close()

##
data_sim_index = 10
t = dict_data_info['t']
f,ax = plt.subplots(3,3,sharex=True)
if dict_data_info['state_measured']:
    for i,j in product(list(range(3)),list(range(2))):
        try:
            ax[i, j].plot(t, ls_data_pred[data_sim_index]['XT_true'][:, 2*i+j], '.', linewidth=3, color='tab:blue')
            ax[i, j].plot(t, ls_data_pred[data_sim_index]['XT_est'][:, 2*i+j], color='tab:blue')
        except:
            print('i = ' + str(i) + ' j = ' + str(j) + 'is not available')
if dict_data_info['output_measured']:
    for i in range(3):
        ax[i, 2].plot(t, ls_data_pred[data_sim_index]['YT_true'][:, i], '.', linewidth=3, color='tab:blue')
        ax[i, 2].plot(t, ls_data_pred[data_sim_index]['YT_est'][:, i], color='tab:blue')

f.show()


## Plot the statistics
# The maximum % error in each
x = np.empty((0))

for i in range(len(ls_data)):
    x = np.concatenate([x,np.array([i])],axis=0)
    y_i = np.empty((0))
    # Max error in each state and output
    y_i = np.concatenate([y_i, r2_score(ls_data_pred[i]['XT_true'], ls_data_pred[i]['XT_est'],multioutput='raw_values')*100],axis=0)
    y_i = np.concatenate([y_i, r2_score(ls_data_pred[i]['YT_true'], ls_data_pred[i]['YT_est'],multioutput='raw_values')*100],axis=0)
    # Concatenate all statistics
    if i>0:
        y = np.concatenate([y,y_i.reshape(1,-1)],axis=0)
    else:
        y = y_i.reshape(1,-1)

f,ax = plt.subplots(2,2,sharex = True,figsize=(10,10))
legend_names_state = ['x1','x2','x3','x4','x5','x6']
legend_names_output = ['y1','y2','y3']
for i in range(len(legend_names_state)):
    if np.max(y[:,i])>100:
        ax[0, 0].plot(x, y[:, i], label=legend_names_state[i])
    else:
        ax[1, 0].plot(x, y[:, i], label=legend_names_state[i])
legend_names_output = ['y1','y2','y3']
for i in range(len(legend_names_output)):
    if np.max(y[:,i])>100:
        ax[0, 1].plot(x, y[:, i], label=legend_names_output[i])
    else:
        ax[1, 1].plot(x, y[:, i], label=legend_names_output[i])
ax[0,0].legend()
ax[0,1].legend()
ax[1,0].legend()
ax[1,1].legend()
f.show()

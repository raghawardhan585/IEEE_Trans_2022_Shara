import numpy as np
import pandas as pd
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import copy
plt.rcParams["font.family"] = "Avenir"
plt.rcParams["mathtext.fontset"] = "cm"
plt.rcParams["font.size"] = 22

# Constant Parameters
# Glycolytic Oscillator
go_N = 1.
go_A = 40.
go_k0 = 10.
go_k1 = 100.
go_k2 = 6.
go_k3 = 1.60
go_k4 = 100.
go_k5 = 1.28
go_k6 = 12.
go_k7 = 1.8
go_K1 = 0.52
go_kappa = 13.
go_mu = 0.1
go_q = 4
u_go_step = 0.
# Activator Repressor
ar_gamma_A = 1.
ar_gamma_B = 0.5
ar_delta_A = 1.
ar_delta_B = 1.
ar_alpha_A0= 0.04
ar_alpha_B0= 0.004
ar_alpha_A = 50.
ar_alpha_B = 30.
ar_K_A = 1.
ar_K_B = 1.5
ar_kappa_A = 0.4
ar_kappa_B = 0.4
ar_n = 2.
ar_m = 2.
u_ar_step = 0.
# Incoherent Feed Forward Loop
iffl_gamma = 0.2
iffl_k0 = 0.4
iffl_k1 = 0.08
iffl_Kd = 1.
u_iffl_step = 0.
# Toggle Switch
ts_beta = 1.
ts_K = 10.
ts_gamma = 0.2
ts_n = 1.
u_ts_step = 0
ts_k0 = 0.01

def incoherent_feed_forward_loop(x, t):
    # TODO - Need to figure out how to simulate the system with stationary input - u
    xdot = np.zeros(len(x))
    xdot[0] = iffl_k0*u_iffl_step - iffl_gamma*x[0]
    xdot[1] = iffl_k1*u_iffl_step/(1 + (x[0]/iffl_Kd)) - iffl_gamma*x[1]
    return xdot

def activator_repressor(x,t):
    xdot = np.zeros(len(x))
    xdot[0] = - ar_gamma_A * x[0] + ar_kappa_A/ar_delta_A * (ar_alpha_A*(x[0]/ar_K_A)**ar_n + ar_alpha_A0)/(1 + (x[0]/ar_K_A)**ar_n + (x[1]/ar_K_B)**ar_m)
    xdot[1] = - ar_gamma_B * x[1] + ar_kappa_B/ar_delta_B*(ar_alpha_B*(x[0]/ar_K_A)**ar_n + ar_alpha_B0)/(1 + (x[0]/ar_K_A)**ar_n)
    return xdot

def glycolytic_oscillator(x,t):
    xdot = np.zeros(len(x))
    xdot[0] = go_k0*u_go_step - go_k1*x[0]*x[5]/(1 +(x[5]/go_K1)**go_q)
    xdot[1] = 2*go_k1*x[0]*x[5]/(1 +(x[5]/go_K1)**go_q) - go_k2*x[1]*(go_N-x[4]) - go_k6*x[1]*x[4]
    xdot[2] = go_k2*x[1]*(go_N-x[4]) - go_k3*x[2]*(go_A-x[5])
    xdot[3] = go_k3*x[2]*(go_A-x[5]) - go_k4*x[3]*x[4] - go_kappa*(x[3]-x[6])
    xdot[4] = go_k2*x[1]*(go_N-x[4]) - go_k4*x[3]*x[4] - go_k6*x[1]*x[4]
    xdot[5] = -2*go_k1*x[0]*x[5]/(1 +(x[5]/go_K1)**go_q) + 2*go_k3*x[2]*(go_A-x[5]) - go_k5*x[5]
    xdot[6] = go_mu*go_kappa*(x[3]-x[6]) -go_k7*x[6]
    return xdot

def full_system(x,t, couple_ar_iffl = 1., couple_iffl_go= 1., couple_iffl_ts = 1.):
    xdot = np.zeros(len(x))
    # Activator Repressor
    xdot[0] = - ar_gamma_A * x[0] + ar_kappa_A / ar_delta_A * (ar_alpha_A * (x[0] / ar_K_A) ** ar_n + ar_alpha_A0) / (1 + (x[0] / ar_K_A) ** ar_n + (x[1] / ar_K_B) ** ar_m)
    xdot[1] = - ar_gamma_B * x[1] + ar_kappa_B / ar_delta_B * (ar_alpha_B * (x[0] / ar_K_A) ** ar_n + ar_alpha_B0) / (1 + (x[0] / ar_K_A) ** ar_n)
    # Incoherent feed forward loop
    u_iffl = u_iffl_step + couple_ar_iffl * x[1]
    xdot[2] = iffl_k0 * u_iffl - iffl_gamma * x[2]
    xdot[3] = iffl_k1 * u_iffl / (1 + (x[2] / iffl_Kd)) - iffl_gamma * x[3]
    # Glycolytic Oscillator
    u_go = u_go_step + couple_iffl_go * x[3]
    xdot[4] = go_k0 * u_go - go_k1 * x[4] * x[9] / (1 + (x[9] / go_K1) ** go_q)
    xdot[5] = 2 * go_k1 * x[4] * x[9] / (1 + (x[9] / go_K1) ** go_q) - go_k2 * x[5] * (go_N - x[8]) - go_k6 * x[5] * x[8]
    xdot[6] = go_k2 * x[5] * (go_N - x[8]) - go_k3 * x[6] * (go_A - x[9])
    xdot[7] = go_k3 * x[6] * (go_A - x[9]) - go_k4 * x[7] * x[8] - go_kappa * (x[7] - x[10])
    xdot[8] = go_k2 * x[5] * (go_N - x[8]) - go_k4 * x[7] * x[8] - go_k6 * x[5] * x[8]
    xdot[9] = -2 * go_k1 * x[4] * x[9] / (1 + (x[9] / go_K1) ** go_q) + 2 * go_k3 * x[6] * (go_A - x[9]) - go_k5 * x[9]
    xdot[10] = go_mu * go_kappa * (x[7] - x[10]) - go_k7 * x[10]
    # Toggle Switch
    u_ts = u_ts_step + couple_iffl_ts * x[3]
    xdot[11] = ts_k0*u_ts + ts_beta / (1 + (x[12] / ts_K) ** ts_n) - ts_gamma * x[11]
    xdot[12] = ts_beta / (1 + (x[11] / ts_K) ** ts_n) - ts_gamma * x[12]
    return xdot

def Ar_IfflTs(x,t, couple_ar_iffl = 1., couple_iffl_ts = 1.):
    xdot = np.zeros(len(x))
    # Activator Repressor
    xdot[0] = - ar_gamma_A * x[0] + ar_kappa_A / ar_delta_A * (ar_alpha_A * (x[0] / ar_K_A) ** ar_n + ar_alpha_A0) / (1 + (x[0] / ar_K_A) ** ar_n + (x[1] / ar_K_B) ** ar_m)
    xdot[1] = - ar_gamma_B * x[1] + ar_kappa_B / ar_delta_B * (ar_alpha_B * (x[0] / ar_K_A) ** ar_n + ar_alpha_B0) / (1 + (x[0] / ar_K_A) ** ar_n)
    # Incoherent feed forward loop
    u_iffl = u_iffl_step + couple_ar_iffl * x[1]
    xdot[2] = iffl_k0 * u_iffl - iffl_gamma * x[2]
    xdot[3] = iffl_k1 * u_iffl / (1 + (x[2] / iffl_Kd)) - iffl_gamma * x[3]
    # Toggle Switch
    u_ts = u_ts_step + couple_iffl_ts * x[3]
    xdot[4] = ts_k0*u_ts + ts_beta / (1 + (x[5] / ts_K) ** ts_n) - ts_gamma * x[4]
    xdot[5] = ts_beta / (1 + (x[4] / ts_K) ** ts_n) - ts_gamma * x[5]
    return xdot

def Ts_IfflAr(x,t, couple_ts_iffl = 1., couple_ts_ar = 1.):
    xdot = np.zeros(len(x))
    # Toggle Switch
    xdot[0] = ts_beta / (1 + (x[1] / ts_K) ** ts_n) - ts_gamma * x[0]
    xdot[1] = ts_beta / (1 + (x[0] / ts_K) ** ts_n) - ts_gamma * x[1]
    # Incoherent feed forward loop
    u_iffl = u_iffl_step + couple_ts_iffl * x[1]
    xdot[2] = iffl_k0 * u_iffl - iffl_gamma * x[2]
    xdot[3] = iffl_k1 * u_iffl / (1 + (x[2] / iffl_Kd)) - iffl_gamma * x[3]
    # Activator Repressor
    u_ar = u_ar_step + couple_ts_ar * x[3]
    xdot[4] = ts_k0 * u_ar - ar_gamma_A * x[4] + ar_kappa_A / ar_delta_A * (ar_alpha_A * (x[4] / ar_K_A) ** ar_n + ar_alpha_A0) / (1 + (x[4] / ar_K_A) ** ar_n + (x[5] / ar_K_B) ** ar_m)
    xdot[5] = - ar_gamma_B * x[5] + ar_kappa_B / ar_delta_B * (ar_alpha_B * (x[4] / ar_K_A) ** ar_n + ar_alpha_B0) / (1 + (x[4] / ar_K_A) ** ar_n)
    return xdot


def Ts_Ar_Iffl(x,t, couple_ts_ar = 1.,couple_ar_iffl = 1.):
    xdot = np.zeros(len(x))
    # Toggle Switch
    xdot[0] = ts_beta / (1 + (x[1] / ts_K) ** ts_n) - ts_gamma * x[0]
    xdot[1] = ts_beta / (1 + (x[0] / ts_K) ** ts_n) - ts_gamma * x[1]
    # Activator Repressor
    u_ar = u_ar_step + couple_ts_ar * x[1]
    xdot[2] = ts_k0 * u_ar - ar_gamma_A * x[2] + ar_kappa_A / ar_delta_A * (
                ar_alpha_A * (x[2] / ar_K_A) ** ar_n + ar_alpha_A0) / (
                          1 + (x[2] / ar_K_A) ** ar_n + (x[3] / ar_K_B) ** ar_m)
    xdot[3] = - ar_gamma_B * x[3] + ar_kappa_B / ar_delta_B * (ar_alpha_B * (x[2] / ar_K_A) ** ar_n + ar_alpha_B0) / (
                1 + (x[2] / ar_K_A) ** ar_n)
    # Incoherent feed forward loop
    u_iffl = u_iffl_step + couple_ar_iffl * x[3]
    xdot[4] = iffl_k0 * u_iffl - iffl_gamma * x[4]
    xdot[5] = iffl_k1 * u_iffl / (1 + (x[4] / iffl_Kd)) - iffl_gamma * x[5]
    return xdot




## Some individual systems

# f,ax = plt.subplots(3,1,sharex=True,figsize=(10,15))
# ax[0].plot(t,X[:,0:2])
# ax[0].set_title('Activator - repressor dynamics')
# ax[1].plot(t,X[:,2:4])
# ax[1].set_title('Incoherent feedforward loop dynamics')
# # ax[2].plot(t,X[:,4:11])
# # ax[2].set_title('Glycolytic oscillator dynamics')
# # ax[2].legend(['x1','x2','x3','x4','x5','x6','x7'])
# ax[2].plot(t,X[:,11:13])
# ax[2].set_title('Toggle Switch')
# f.show()
#
#
# f,ax = plt.subplots(2,1,sharex=True,figsize=(10,15))
# ax[0].plot(t,X[:,0:4])
# ax[0].plot(t,X[:,11:13])
# ax[0].legend(['x1','x2','x3','x4','x5','x6'])
# ax[1].plot(t,X[:,0:4])
# ax[1].plot(t,X[:,11:13])
# ax[1].set_ylim([0,10])
# ax[1].legend(['x1','x2','x3','x4','x5','x6'])
# f.show()
#
# f,ax = plt.subplots(1,3,figsize=(15,5))
# ax[0].plot(X[:,0],X[:,1])
# ax[0].set_title('Activator_Repressor')
# ax[1].plot(X[:,2],X[:,3])
# ax[1].set_title('IFFL')
# ax[2].plot(X[:,11],X[:,12])
# ax[2].set_title('Toggle_Switch')
# # ax[2].set_ylim([0,1])
# # ax[2].set_xlim([0,8])
# f.show()
#



# ## Incoherent feed forward loop
# X = odeint(incoherent_feed_forward_loop, x0_init_iffl, t)
#
# plt.figure()
# plt.plot(t,X)
# plt.title('Incoherent feedforward loop dynamics')
# plt.show()
#
# ## Glycolytic Oscillator
# X = odeint(glycolytic_oscillator, x0_init_go, t)
#
# plt.figure()
# plt.plot(t,X)
# plt.title('Glycolytic oscillator dynamics')
# plt.xlim([0,4])
# plt.ylim([0,4])
# plt.show()
#
#
# ## Activator Repressor
# X = odeint(activator_repressor, x0_init_ar, t)
#
# plt.figure()
# plt.plot(t,X)
# plt.title('Activator - repressor dynamics')
# plt.show()
#




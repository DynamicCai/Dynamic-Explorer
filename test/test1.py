# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 20:34:05 2020

@author: Administrator
"""

import numpy as np
from numpy import pi
from scipy.optimize import least_squares
import matplotlib.pyplot as plt

xhydata = np.genfromtxt("G:\\matlab\\data\\20201100.TXT", delimiter = "\t",skip_header=3) 

x_dat = xhydata[:,0]*2*np.pi
e1_dat = xhydata[:,1]
e2_dat = xhydata[:,2]

def fun_havriliak_negami(p, x, e1, e2):
    fx = ( p[0] / ( 1 + ( 1j * x * 10**p[1] )**p[2])**p[3] + p[4] ) - (e1 - 1j * e2)
    result = np.concatenate((fx.real, fx.imag))
    return result

p0 = np.array([2, 0,  0.5, 0.5, 1])

res_lsq = least_squares(fun_havriliak_negami, p0, bounds = ([0, -np.inf, 0, 0, 0], [np.inf, np.inf, 1, 1, np.inf]) ,args = (x_dat, e1_dat, e2_dat))

E_new = res_lsq.x[0] / ( 1 + ( 1j * x_dat * 10**res_lsq.x[1] )**res_lsq.x[2] )**res_lsq.x[3] + res_lsq.x[4]
    
import matplotlib.pyplot as plt
plt.plot(x_dat, e2_dat, 'o')
plt.plot(x_dat, E_new.imag, 'k', linewidth=2, label='HN fit')
plt.xlabel('$\omega$(rad/s)')
plt.ylabel('$\epsilon$"')
plt.xscale('symlog')
plt.yscale('symlog')
plt.show()
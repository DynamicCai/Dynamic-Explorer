import numpy as np
from lmfit import Model, Parameters
import matplotlib.pyplot as plt

xhydata = np.genfromtxt("G:\\matlab\\data\\20201100.TXT", delimiter = "\t",skip_header=3) 

x_dat = xhydata[:,0]*2*np.pi
e1_dat = xhydata[:,1]
e2_dat = xhydata[:,2]
y = e1_dat - 1j * e2_dat
pars = {}

def havriliak_negami(x, de, logtau0, a, b, einf):
    """1-d HN: HN(x, logf0, de, a, b, einf)"""
    return de / ( 1 + ( 1j * x * 10**logtau0 )**a )**b + einf

p0 = np.array([2, 0,  0.5, 0.5, 1])
D = [True,True,True,False,True]
mod1 = Model(havriliak_negami, prefix='HN1_')
mod2 = Model(havriliak_negami, prefix='HN2_')

pars = Parameters()
pars.add("HN1_de",value=100,min=0)
pars.add('HN1_logtau0',value=-2)
pars.add('HN1_a',value=0.5,min=0,max=1)
pars.add('HN1_b',value=0.5,min=0,max=1)
pars.add('HN1_einf',value=1,min=0)

pars.add("HN2_de",value=100,min=0)
pars.add('HN2_logtau0',value=-2)
pars.add('HN2_a',value=0.5,min=0,max=1)
pars.add('HN2_b',value=0.5,min=0,max=1)
pars.add('HN2_einf',value=1,min=0)
print(pars)
mod = mod1 + mod2
result = mod.fit(y, pars, x=x_dat)

plt.plot(x_dat, e2_dat, 'bo')
plt.plot(x_dat, -result.best_fit.imag, 'k--', linewidth=2, label='best fit')
plt.legend(loc='best')
plt.xlabel('$\omega$(rad/s)')
plt.ylabel('$\epsilon$"')
comps = result.eval_components()
plt.plot(x_dat, -comps['HN1_'].imag, 'g--', label='component1')
plt.plot(x_dat, -comps['HN2_'].imag, 'r--', label='component2')
plt.xscale('symlog')

plt.show()
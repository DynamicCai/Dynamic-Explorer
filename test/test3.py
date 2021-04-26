import numpy as np
from lmfit import Model, Parameters
import matplotlib.pyplot as plt

xhydata = np.genfromtxt("G:\\matlab\\data\\20201100.TXT", delimiter = "\t",skip_header=3) 

x_dat = xhydata[:,0]*2*np.pi
e1_dat = xhydata[:,1]
e2_dat = xhydata[:,2]
y = e1_dat - 1j * e2_dat

def havriliak_negami(x, de, logtau0, a, b, einf):
    """1-d HN: HN(x, logf0, de, a, b, einf)"""

    return de / ( 1 + ( 1j * x * 10**logtau0 )**a )**b + einf

p0 = np.array([2, 0,  0.5, 0.5, 1])
mod1 = Model(havriliak_negami, prefix='HN1_')
mod2 = Model(havriliak_negami, prefix='HN2_')
mod = mod1 + mod2
pars = mod.make_params()
pars['HN1_de'].set(value=2)
pars['HN1_logtau0'].set(value=0)
pars['HN1_a'].set(value=0.5)
pars['HN1_b'].set(value=0.5)
pars['HN1_einf'].set(value=1)
pars['HN2_de'].set(value=2)
pars['HN2_logtau0'].set(value=0)
pars['HN2_a'].set(value=0.5)
pars['HN2_b'].set(value=0.5)
pars['HN2_einf'].set(value=1)

result = mod.fit(y, pars, x=x_dat)

print(result.fit_report)

plt.plot(x_dat, e2_dat, 'bo')
plt.plot(x_dat, result.best_fit.imag, 'k--', linewidth=2, label='best fit')
plt.legend(loc='best')
plt.xlabel('$\omega$(rad/s)')
plt.ylabel('$\epsilon$"')
plt.xscale('symlog')
plt.yscale('symlog')
plt.show()
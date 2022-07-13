import os
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from scipy.sparse import csc_matrix, spdiags
from scipy.sparse.linalg import spsolve

# read e-sers data from txt file
path = 'AgNPs_APTES_FTO_Ket'
files = os.listdir(path)
file_list = []
for file in files:
    file_name = os.path.join(path, file)
    file_list.append(file_name)

df_list = []
for i in range(len(file_list)):
    locals()['df' + str(i)] = pd.read_csv(file_list[i], header=None,
                                          skiprows=range(14), names=['Wave', 'Intst'], sep='\t')
    df_list.append(locals()['df' + str(i)])


# execute ALs baseline correlation
def ALSBaselineCorrection(y, lam=1E6, p=0.001, niter=30):
    m = len(y)
    w = np.ones(m)
    D = csc_matrix(np.diff(np.eye(m), 3))
    for i in range(niter):
        W = spdiags(w, 0, m, m)
        Z = W + lam * D.dot(D.transpose())
        z = spsolve(Z, w * y)
        w = p * (y > z) + (1 - p) * (y < z)
    return z


for i in range(len(file_list)):
    df_list[i]['Baseline'] = ALSBaselineCorrection(df_list[i]['Intst'])
    df_list[i]['CorIntst'] = df_list[i]['Intst'] - df_list[i]['Baseline']


# universal definition
xlabel_str = 'Raman Shift ($\mathregular{cm^{-1}}$)'
ylabel_str = 'Intensity (counts $\mathregular{s^{-1}mW^{-1}}$)'


# plot a set of raw and corrected spectra as example
ax1 = plt.subplot()
ax1.plot(df_list[2]['Wave'], df_list[2]['Intst'])
ax1.plot(df_list[2]['Wave'], df_list[2]['Baseline'])
ax1.plot(df_list[2]['Wave'], df_list[2]['CorIntst'])
ax1.set_title('Example of ALS Baseline Correction spectra', fontsize=14, pad=20)
ax1.set_xlabel(xlabel_str)
ax1.set_ylabel(ylabel_str)
ax1.legend(['Raw Spectra', 'ALS Baseline', 'Corrected Spectra'])
ax1.axis([200, 3200, -100, 1600])   # adjust after trial run
plt.savefig('AgNPs_APTES_FTO_Ket_100uM_NaF_0.1M_1.png')
plt.show()


# plot corrected spectra with a stacked y-axis
ax2 = plt.subplot()
for i in range(len(df_list)):
    ax2.plot(df_list[i]['Wave'], df_list[i]['CorIntst'] + 800*i)
    ax2.annotate('No. '+str(i+1)+' measurement', (1800, 50+800*i))  # adjust after trial run
ax2.set_title('Corrected Spectra with a Stacked Y-Axis', fontsize=14, pad=20)
ax2.set_xlabel(xlabel_str)
ax2.set_ylabel(ylabel_str)
ax2.set_yticks([])
ax2.set_yticklabels([])
ax2.axis([200, 3200, -200, 4200])   # adjust after trial run
plt.savefig('AgNPs_APTES_FTO_Ket_100uM_NaF_0.1M_2.png')
plt.show()


# plot averaging spectrum
df_mean = df_cormean = pd.DataFrame({'Wave': df_list[0]['Wave']})
for i in range(len(df_list)):
    df_mean = df_mean.join(df_list[i][['Wave', 'Intst']].set_index('Wave'), on='Wave', rsuffix='_' + str(i+1))
    df_cormean = df_cormean.join(df_list[i][['Wave', 'CorIntst']].set_index('Wave'), on='Wave', rsuffix='_' + str(i+1))

df_mean['Mean'] = df_mean.drop('Wave', axis=1).apply(np.mean, axis=1)
df_cormean['Mean'] = df_cormean.drop('Wave', axis=1).apply(np.mean, axis=1)

ax3 = plt.subplot()
ax3.plot(df_mean['Wave'], df_mean['Mean'])
ax3.plot(df_cormean['Wave'], df_cormean['Mean'])
ax3.set_title('Averaging Spectra', fontsize=14, pad=20)
ax3.set_xlabel(xlabel_str)
ax3.set_ylabel(ylabel_str)
ax3.legend(['Averaging Raw Spectra', 'Averaging Corrected Spectra'])
ax3.axis([200, 3200, -100, 1700])   # adjust after trial run
plt.savefig('AgNPs_APTES_FTO_Ket_100uM_NaF_0.1M_3.png')
plt.show()

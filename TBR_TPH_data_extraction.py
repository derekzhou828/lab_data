import os
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from scipy.sparse import csc_matrix, spdiags
from scipy.sparse.linalg import spsolve

# read e-sers data from txt file
path = 'raw_data/raman-example'
files = os.listdir(path)
file_list = []
for file in files:
    file_name = os.path.join(path, file)
    file_list.append(file_name)

df_list = []
for i in range(len(file_list)):
    locals()['df'+str(i+1)] = pd.read_csv(file_list[i], header=None, skiprows=[0], names=['Wave', 'Intst'], sep='\t')
    df_list.append(locals()['df'+str(i+1)])


# perform ALS baseline correlation, guided by Tabby, many thanks!
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


for i in range(6):
    df_list[i]['Baseline'] = ALSBaselineCorrection(df_list[i]['Intst'])
    df_list[i]['CorIntst'] = df_list[i]['Intst'] - df_list[i]['Baseline']

# plot separately in subplots
fig1, axs1 = plt.subplots(nrows=6, ncols=2, figsize=(9, 16))
axs1[0, 0].set_title('Raw Spectrum', fontsize=14, pad=20)
axs1[0, 1].set_title('ALS Baseline Corrected Spectrum', fontsize=14, pad=20)

for i in range(6):
    axs1[i, 0].axis([400, 2000, 24000, 51000])
    axs1[i, 0].plot(df_list[i]['Wave'], df_list[i]['Intst'])
    axs1[i, 0].set_xlabel('Raman Shift ($\mathregular{cm^{-1}}$)')
    axs1[i, 0].set_xticks([400, 600, 800, 1000, 1200, 1400, 1600, 1800, 2000])
    axs1[i, 0].set_xticklabels(['400', '600', '800', '1000', '1200', '1400', '1600', '1800', '2000'])
    axs1[i, 0].set_ylabel('Intensity (counts $\mathregular{s^{-1}mW^{-1}}$)')
    axs1[i, 0].set_yticks([25000, 30000, 35000, 40000, 45000, 50000])
    axs1[i, 0].set_yticklabels(['25000', '30000', '35000', '40000', '45000', '50000'])

    axs1[i, 1].axis([400, 2000, -5000, 55000])
    axs1[i, 1].plot(df_list[i]['Wave'], df_list[i]['Intst'])
    axs1[i, 1].plot(df_list[i]['Wave'], df_list[i]['Baseline'], '--')
    axs1[i, 1].plot(df_list[i]['Wave'], df_list[i]['CorIntst'], 'r')
    axs1[i, 1].set_xlabel('Raman Shift ($\mathregular{cm^{-1}}$)')
    axs1[i, 1].set_xticks([400, 600, 800, 1000, 1200, 1400, 1600, 1800, 2000])
    axs1[i, 1].set_xticklabels(['400', '600', '800', '1000', '1200', '1400', '1600', '1800', '2000'])
    axs1[i, 1].set_ylabel('Intensity (counts $\mathregular{s^{-1}mW^{-1}}$)')
    axs1[i, 1].legend(['Raw Spectra', 'ALS Baseline', 'Corrected Spectra'], fontsize=6)

fig1.tight_layout()
plt.savefig('fig_gallery/TBR_TPH_data_extraction_1.png')
plt.show()

# plot separately in single figure
fig2, (axs20, axs21) = plt.subplots(nrows=1, ncols=2, figsize=(16, 6))

for i in range(6):
    axs20.plot(df_list[i]['Wave'], df_list[i]['Intst'])
    axs20.axis([400, 2000, 24000, 51000])
    axs20.set_title('Set of Raw Spectrum', fontsize=14, pad=20)
    axs20.set_xlabel('Raman Shift ($\mathregular{cm^{-1}}$)')
    axs20.set_xticks([400, 600, 800, 1000, 1200, 1400, 1600, 1800, 2000])
    axs20.set_xticklabels(['400', '600', '800', '1000', '1200', '1400', '1600', '1800', '2000'])
    axs20.set_ylabel('Intensity (counts $\mathregular{s^{-1}mW^{-1}}$)')
    axs20.set_yticks([25000, 30000, 35000, 40000, 45000, 50000])
    axs20.set_yticklabels(['25000', '30000', '35000', '40000', '45000', '50000'])

    axs21.plot(df_list[i]['Wave'], df_list[i]['CorIntst']+8000*i)
    axs21.axis([400, 2000, -4000, 48000])
    axs21.set_title('Set of ALS Baseline Corrected Spectrum', fontsize=14, pad=20)
    axs21.set_xlabel('Raman Shift ($\mathregular{cm^{-1}}$)')
    axs21.set_xticks([400, 600, 800, 1000, 1200, 1400, 1600, 1800, 2000])
    axs21.set_xticklabels(['400', '600', '800', '1000', '1200', '1400', '1600', '1800', '2000'])
    axs21.set_ylabel('Intensity Y-offset Schematic')
    axs21.set_yticks([2000, 10000, 18000, 26000, 34000, 42000])
    axs21.set_yticklabels(['Sample 1', 'Sample 2', 'Sample 3', 'Sample 4', 'Sample 5', 'Sample 6'])

fig2.tight_layout()
plt.savefig('fig_gallery/TBR_TPH_data_extraction_2.png')
plt.show()

# plot averaging spectrum
df_ave = df_cor_ave = pd.DataFrame({'Wave': df_list[0]['Wave']})
for i in range(6):
    df_ave = df_ave.join(df_list[i][['Wave', 'Intst']].set_index('Wave'), on='Wave', rsuffix='_' + str(i))
    df_cor_ave = df_cor_ave.join(df_list[i][['Wave', 'CorIntst']].set_index('Wave'), on='Wave', rsuffix='_' + str(i))

df_ave['Ave'] = df_ave.drop('Wave', axis=1).apply(np.mean, axis=1)
df_cor_ave['Ave'] = df_cor_ave.drop('Wave', axis=1).apply(np.mean, axis=1)

fig3, (axs30, axs31) = plt.subplots(nrows=1, ncols=2, figsize=(16, 6))

axs30.plot(df_ave['Wave'], df_ave['Ave'])
axs30.axis([400, 2000, 24000, 51000])
axs30.set_title('Average Raw Spectrum', fontsize=14, pad=20)
axs30.set_xlabel('Raman Shift ($\mathregular{cm^{-1}}$)')
axs30.set_xticks([400, 600, 800, 1000, 1200, 1400, 1600, 1800, 2000])
axs30.set_xticklabels(['400', '600', '800', '1000', '1200', '1400', '1600', '1800', '2000'])
axs30.set_ylabel('Intensity (counts $\mathregular{s^{-1}mW^{-1}}$)')
axs30.set_yticks([25000, 30000, 35000, 40000, 45000, 50000])
axs30.set_yticklabels(['25000', '30000', '35000', '40000', '45000', '50000'])

axs31.plot(df_cor_ave['Wave'], df_cor_ave['Ave'])
axs31.axis([400, 2000, -500, 7500])
axs31.set_title('Average ALS Baseline Corrected Spectrum Spectrum', fontsize=14, pad=20)
axs31.set_xlabel('Raman Shift ($\mathregular{cm^{-1}}$)')
axs31.set_xticks([400, 600, 800, 1000, 1200, 1400, 1600, 1800, 2000])
axs31.set_xticklabels(['400', '600', '800', '1000', '1200', '1400', '1600', '1800', '2000'])
axs31.set_ylabel('Intensity (counts $\mathregular{s^{-1}mW^{-1}}$)')
axs31.set_yticks([0, 1000, 2000, 3000, 4000, 5000, 6000, 7000])
axs31.set_yticklabels(['0', '1000', '2000', '3000', '4000', '5000', '6000', '7000'])

fig3.tight_layout()
plt.savefig('fig_gallery/TBR_TPH_data_extraction_3.png')
plt.show()

import os
import re
import time
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from scipy.sparse import csc_matrix, spdiags
from scipy.sparse.linalg import spsolve


def ALSBaselineCorrection(y, lam=1E6, p=0.0001, niter=30):
    m = len(y)
    w = np.ones(m)
    D = csc_matrix(np.diff(np.eye(m), 3))
    for i in range(niter):
        W = spdiags(w, 0, m, m)
        Z = W + lam * D.dot(D.transpose())
        z = spsolve(Z, w * y)
        w = p * (y > z) + (1 - p) * (y < z)
    return z


# read times v.s. potentials
path_gamry = 'raw_data/AuAgCoreShell_UA_100uM_CRN_0uM_R6G_10uM_Jun23/Potential_Sequence'
files_gamry = os.listdir(path_gamry)
time_potential = {}

for file in files_gamry:
    with open(os.path.join(path_gamry, file), 'r') as f:
        lines = f.readlines()
        potential = lines[10].split('\t')[2].split('\t')[0]
        time_str = '2022-06-23 ' + lines[4].split('\t')[2].split('\t')[0]
        time_array = time.strptime(time_str, '%Y-%m-%d %H:%M:%S')
        time_stamp = int(time.mktime(time_array))
        time_potential[time_stamp] = potential
        time_line = sorted(list(time_potential.keys()))


# data extraction and preprocessing
path_raman = 'raw_data/AuAgCoreShell_UA_100uM_CRN_0uM_R6G_10uM_Jun23/Scan_RamanShift'
files_raman = os.listdir(path_raman)
data_single = []
data_collection = pd.DataFrame()

for file in files_raman:
    UA = int(re.search(r'UA_+([0-9]+uM)', file).group(1).removesuffix('uM'))
    CRN = int(re.search(r'CRN_+([0-9]+uM)', file).group(1).removesuffix('uM'))
    R6G = int(re.search(r'R6G_+([0-9]+uM)', file).group(1).removesuffix('uM'))

    df = pd.read_csv(
        os.path.join(path_raman, file),
        header=None, skiprows=range(122), names=['wave', 'intst'], sep='\t'
    )
    df = df[(df['wave'] > 500) & (df['wave'] < 1800)]
    wave = df['wave']
    df['intst'] -= ALSBaselineCorrection(df['intst'])

    with open(os.path.join(path_raman, file), 'r') as f:
        lines = f.readlines()
        time_str = '2022-06-23 ' + lines[2].split(' ')[4]
        time_array = time.strptime(time_str, '%Y-%m-%d %H:%M:%S')
        time_stamp = int(time.mktime(time_array))

    for i in range(len(time_line)):
        if (time_stamp > time_line[i]) & ((time_stamp+70) < time_line[i] + 300):
            Potential = float(time_potential[time_line[i]])
            data_single.append([file, UA, CRN, R6G, Potential] + df['intst'].tolist())

data_collection = pd.DataFrame(
    data_single,
    columns=['Filename', 'UA', 'CRN', 'R6G', 'Potential'] + ['wave_' + str(int(x)) for x in wave.tolist()]
)

data_collection.to_csv('initial_process/Au@AuCoreShell_UA_Jun23_all.csv', index=False)

# average and plot spectrum
ax = plt.subplot()
ax.set_title('100uM UA + 0.1M NaF + 10uM R6G for Au@AgCoreShell-APTES-FTO')
ax.set_xlabel('Raman Shift ($\mathregular{cm^{-1}}$)')
ax.set_ylabel('Intensity (counts $\mathregular{s^{-1}mW^{-1}}$)')
ax.set_yticks([0, 600, 1200, 1800, 2400, 3000, 3600, 4200])
ax.set_yticklabels(['0', '600', '', '', '', '', '', ''])

data_average = pd.DataFrame()
for p, g in data_collection.groupby(data_collection['Potential']):
    mean = round(g.mean(numeric_only=True), 1)
    df = pd.DataFrame([mean], columns=mean.index)
    data_average = pd.concat([data_average, df], ignore_index=True)

    plt.plot(wave, mean[4:]+6000*abs(mean['Potential']))
    ax.annotate(str(mean['Potential']) + ' V', (1700, 100+6000*abs(mean['Potential'])))

data_average.to_csv('initial_process/Au@AuCoreShell_UA_Jun23_average.csv', index=False)
plt.savefig('fig_gallery/Au@AuCoreShell_UA_Jun23_1.png')
plt.show()

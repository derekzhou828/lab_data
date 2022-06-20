import re
import os
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from scipy.sparse import csc_matrix, spdiags
from scipy.sparse.linalg import spsolve
from sklearn.preprocessing import StandardScaler
from sklearn.cross_decomposition import PLSRegression


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


path = 'raw_data/TBR_TPH_data_regression'
files = os.listdir(path)
data_per_mmt = []

for file in files:

    # collect concentrations through filenames with unit=M
    TBR = re.search(r'([0-9.]+[un]M)(theobr)', file)
    if TBR is not None:
        TBR = TBR.group(1)
        if TBR.endswith('nM'):
            TBR = float(TBR.removesuffix('nM')) * 1E-9
        else:
            TBR = float(TBR.removesuffix('uM')) * 1E-6
    else:
        TBR = 0.0

    TPH = re.search(r'([0-9.]+[un]M)(theophy)', file)
    if TPH is not None:
        TPH = TPH.group(1)
        if TPH.endswith('nM'):
            TPH = float(TPH.removesuffix('nM')) * 1E-9
        else:
            TPH = float(TPH.removesuffix('uM')) * 1E-6
    else:
        TPH = 0.0

    # read Raman data and preprocess
    df = pd.read_csv(os.path.join(path, file), header=None, skiprows=[0], names=['wave', 'intst'], sep='\t')
    df['intst'] -= ALSBaselineCorrection(df['intst'])
    normalised_intst = StandardScaler().fit_transform(df['intst'].values.reshape(-1, 1))
    data_per_mmt.append([file, TBR, TPH] + normalised_intst.flatten().tolist())

data_df = pd.DataFrame(
    data_per_mmt, columns=['filename', 'TBR', 'TPH'] + ['wave_'+str(x+1) for x in range(len(df['intst']))]
)

data_df.to_csv('initial_process/TBR_TPH_data_df.csv', index=False)


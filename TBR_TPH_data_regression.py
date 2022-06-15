import re
import os
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from scipy.sparse import csc_matrix, spdiags
from scipy.sparse.linalg import spsolve
from sklearn.cross_decomposition import PLSRegression


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


path = 'raw_data/TBR_TPH_data_regression'
files = os.listdir(path)

data_as_list = []
data_df = pd.DataFrame()

for file in files:
    # extract txt content as DataFrame
    df = pd.read_csv(os.path.join(path, file), header=None, skiprows=[0], names=['wave', 'intst'], sep='\t')
    df['intst'] -= ALSBaselineCorrection(df['intst'])

    # collect concentrations, unit=uM
    TBR = re.search(r'([0-9.]+[un]M)(theobr)', file)
    if TBR is not None:
        TBR = TBR.group(1)
        if TBR.endswith('nM'):
            TBR = float(TBR.removesuffix('nM')) / 1000
        else:
            TBR = float(TBR.removesuffix('uM'))
    else:
        TBR = 0.0

    TPH = re.search(r'([0-9.]+[un]M)(theophy)', file)
    if TPH is not None:
        TPH = TPH.group(1)
        if TPH.endswith('nM'):
            TPH = float(TPH.removesuffix('nM')) / 1000
        else:
            TPH = float(TPH.removesuffix('uM'))
    else:
        TPH = 0.0

    data_as_list.append([file, np.array(df['intst']), TBR, TPH])

data_df = pd.DataFrame(data_as_list, columns=['file', 'intst', 'TBR', 'TPH'])

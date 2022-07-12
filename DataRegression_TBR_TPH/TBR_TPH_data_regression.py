import re
import os
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from scipy.sparse import csc_matrix, spdiags
from scipy.sparse.linalg import spsolve
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.cross_decomposition import PLSRegression
from sklearn.metrics import mean_squared_error, r2_score


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


# Crate Dataframe for data analysis
path = 'TBR_TPH_data_regression'
files = os.listdir(path)
data_per_mmt = []

for file in files:
    # Collect concentrations through filenames with unit=M
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

    # Read Raman data and preprocess
    df = pd.read_csv(os.path.join(path, file), header=None, skiprows=[0], names=['wave', 'intst'], sep='\t')
    df['intst'] -= ALSBaselineCorrection(df['intst'])
    normalised_intst = StandardScaler().fit_transform(df['intst'].values.reshape(-1, 1))
    data_per_mmt.append([file, TBR, TPH] + normalised_intst.flatten().tolist())

data_df = pd.DataFrame(
    data_per_mmt, columns=['filename', 'TBR', 'TPH'] + ['wave_' + str(x + 1) for x in range(len(df['intst']))]
)
data_df.to_csv('TBR_TPH_data_df.csv', index=False)


# Execute PLSR with selected data and evaluate performance
data_sel_df = data_df[(data_df['TBR'] < 1.5E-6) & (data_df['TPH'] < 1.5E-6)]
TBR_actual = []
TPH_actual = []
TBR_pred = []
TPH_pred = []
r2_list = []

for i in range(1000):
    x_train, x_test, y_train, y_test = train_test_split(
        data_sel_df.iloc[:, 3:], data_sel_df[['TBR', 'TPH']], test_size=0.2
    )
    pls = PLSRegression(n_components=6)
    pls.fit(x_train, y_train)
    y_pred = pls.predict(x_test)

    TBR_actual += y_test['TBR'].tolist()
    TPH_actual += y_test['TPH'].tolist()
    TBR_pred += y_pred[:, 0].tolist()
    TPH_pred += y_pred[:, 1].tolist()

    r2 = r2_score(y_test, y_pred)
    r2_list.append(r2)

mean_r2 = np.mean(r2_list)
std_r2 = np.std(r2_list)
print(f'Execute 1000 loops: r2={mean_r2:.3f}, std={std_r2:.3f}')


# Visualise predicted concentrations
pred_df = pd.DataFrame({
    'TBR_actual': TBR_actual, 'TPH_actual': TPH_actual, 'TBR_pred': TBR_pred, 'TPH_pred': TPH_pred
})

r2_TBR = r2_score(pred_df['TBR_actual'], pred_df['TBR_pred'])
RMSEP_TBR = mean_squared_error(pred_df['TBR_actual'], pred_df['TBR_pred']) ** 0.5
r2_TPH = r2_score(pred_df['TPH_actual'], pred_df['TPH_pred'])
RMSEP_TPH = mean_squared_error(pred_df['TPH_actual'], pred_df['TPH_pred']) ** 0.5

print(f'TBR: r2={r2_TBR:.3f}, RMSEP={RMSEP_TBR}\nTPH: r2={r2_TPH:.3f}, RMSEP={RMSEP_TPH}')

TBR_pred_mean = pred_df.groupby(['TBR_actual'])['TBR_pred'].mean()
TBR_pred_std = pred_df.groupby(['TBR_actual'])['TBR_pred'].std()
TPH_pred_mean = pred_df.groupby(['TPH_actual'])['TPH_pred'].mean()
TPH_pred_std = pred_df.groupby(['TPH_actual'])['TPH_pred'].std()

fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(16, 7))

for ax in [ax1, ax2]:
    ax.plot([0, 1], [0, 1], linewidth=2, color='k', linestyle='--')
    ax.set_xlabel('Actual Concentration ($\mu$M)', fontsize=18)
    ax.set_ylabel('Predicted Concentration ($\mu$M)', fontsize=18)
    ax.axis([-0.05, 1.05, -0.1, 1.1])

ax1.errorbar(
    TBR_pred_mean.index * 1E6, TBR_pred_mean * 1E6,
    yerr=TBR_pred_std * 1E6, fmt='o', color='blue', capsize=5
)

ax1.set_title(
    'Theobromine \nR$^{2}$ = ' + str(format(r2_TBR, '.3f')) +
    '\nRMSEP = ' + str(format(RMSEP_TBR * 1E6, '.3f')) + ' $\mu$M',
    loc='left', y=0.8, x=0.05, color='blue', fontsize=18
)

ax2.errorbar(
    TPH_pred_mean.index * 1E6, TPH_pred_mean * 1E6,
    yerr=TPH_pred_std * 1E6, fmt='o', color='green', capsize=5
)

ax2.set_title(
    'Theophylline \nR$^{2}$ = ' + str(format(r2_TPH, '.3f')) +
    '\nRMSEP = ' + str(format(RMSEP_TPH * 1E6, '.3f')) + ' $\mu$M',
    loc='left', y=0.8, x=0.05, color='green', fontsize=18
)

plt.savefig('TBR_TPH_regression.png')
plt.show()

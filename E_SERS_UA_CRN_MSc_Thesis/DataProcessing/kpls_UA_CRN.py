import numpy as np
import pandas as pd
from E_SERS_UA_CRN_MSc_Thesis.KernelPLS import *
from sklearn.utils import resample
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from matplotlib import pyplot as plt

df_DataTJ = pd.read_csv('../Data_csv/DataTJ.csv')
df_R = df_DataTJ[(df_DataTJ.UA <= 20) & (df_DataTJ.CRN <= 100) & (df_DataTJ.UA != 2) & (df_DataTJ.CRN != 10)]
df_normalised = df_R.iloc[:, 3:].copy()
df_normalised = df_normalised.div(df_normalised['1362.89183'], axis=0)
df_R = pd.concat([df_R.iloc[:, :3], df_normalised], axis=1)

UA_actual = []
CRN_actual = []
UA_pred = []
CRN_pred = []
r2_list = []

for i in range(1000):
    x_train, x_test, y_train, y_test = train_test_split(df_R.iloc[:, 3:], df_R[['UA', 'CRN']], test_size=0.2)

    KPLS_model = KPLS(x_train, y_train, n_components=50, nkernel_components=100, kernel='rbf', preprocess=True)
    KPLS_model.construct_kpls_model()

    xKernel = KPLS_model.convert_to_kernel(x_test)
    y_pred = KPLS_model.kpls_predict(x_test)

    r2 = r2_score(y_test, y_pred)
    r2_list.append(r2)
    UA_actual += y_test['UA'].tolist()
    CRN_actual += y_test['CRN'].tolist()
    UA_pred += y_pred[:, 0].tolist()
    CRN_pred += y_pred[:, 1].tolist()

mean_r2 = np.mean(r2_list)
std_r2 = np.std(r2_list)
print(f'Execute 1000 loops: r2={mean_r2:.3f}, std={std_r2:.3f}')

# Visualisation
df_pred = pd.DataFrame({'UA_actual': UA_actual, 'CRN_actual': CRN_actual, 'UA_pred': UA_pred, 'CRN_pred': CRN_pred})

r2_UA = r2_score(df_pred['UA_actual'], df_pred['UA_pred'])
RMSEP_UA = mean_squared_error(df_pred['UA_actual'], df_pred['UA_pred']) ** 0.5
r2_CRN = r2_score(df_pred['CRN_actual'], df_pred['CRN_pred'])
RMSEP_CRN = mean_squared_error(df_pred['CRN_actual'], df_pred['CRN_pred']) ** 0.5

print(f'UA: r2={r2_UA:.3f}, RMSEP={RMSEP_UA}\nCRN: r2={r2_CRN:.3f}, RMSEP={RMSEP_CRN}')

UA_pred_mean = df_pred.groupby(['UA_actual'])['UA_pred'].mean()
UA_pred_std = df_pred.groupby(['UA_actual'])['UA_pred'].std()
CRN_pred_mean = df_pred.groupby(['CRN_actual'])['CRN_pred'].mean()
CRN_pred_std = df_pred.groupby(['CRN_actual'])['CRN_pred'].std()

fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(16, 7))

for ax in [ax1, ax2]:
    ax.set_xlabel('Actual Concentration ($\mu$M)', fontsize=18)
    ax.set_ylabel('Predicted Concentration ($\mu$M)', fontsize=18)

ax1.plot([0, 20], [0, 20], linewidth=2, color='k', linestyle='--')
ax1.errorbar(UA_pred_mean.index, UA_pred_mean, yerr=UA_pred_std, fmt='o', color='blue', capsize=5)

ax1.set_title('Uric acid \nR$^{2}$ = ' + str(format(r2_UA, '.3f')) +
              '\nRMSEP = ' + str(format(RMSEP_UA, '.3f')) + ' $\mu$M',
              loc='left', y=0.8, x=0.05, color='blue', fontsize=18)

ax2.plot([0, 100], [0, 100], linewidth=2, color='k', linestyle='--')
ax2.errorbar(CRN_pred_mean.index, CRN_pred_mean, yerr=CRN_pred_std, fmt='o', color='green', capsize=5)

ax2.set_title('Creatinine \nR$^{2}$ = ' + str(format(r2_CRN, '.3f')) +
              '\nRMSEP = ' + str(format(RMSEP_CRN, '.3f')) + ' $\mu$M',
              loc='left', y=0.8, x=0.05, color='green', fontsize=18)

plt.savefig('../Data_Fig/KPLS_UA_CRN.png')
plt.show()

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.cross_decomposition import PLSRegression
from sklearn.metrics import mean_squared_error, r2_score

# Processing PLSR @ Potential=-0.6V
df_DataTJ = pd.read_csv('../Data_csv/DataTJ.csv')
df_R = df_DataTJ[(df_DataTJ.Potential == -0.6) & (df_DataTJ.UA <= 10) & (df_DataTJ.CRN <= 100)]
df_normalised = df_R.iloc[:, 3:].copy()
df_normalised = df_normalised.div(df_normalised['1362.89183'], axis=0)
df_R = pd.concat([df_R.iloc[:, :3], df_normalised], axis=1)

UA_actual = []
CRN_actual = []
UA_pred = []
CRN_pred = []
r2_list = []

for i in range(1000):
    x_train, x_test, y_train, y_test = train_test_split(
        df_R.iloc[:, 3:], df_R[['UA', 'CRN']], test_size=0.2)

    pls = PLSRegression(n_components=5)
    pls.fit(x_train, y_train)
    y_pred = pls.predict(x_test)

    UA_actual += y_test['UA'].tolist()
    CRN_actual += y_test['CRN'].tolist()
    UA_pred += y_pred[:, 0].tolist()
    CRN_pred += y_pred[:, 1].tolist()

    r2 = r2_score(y_test, y_pred)
    r2_list.append(r2)

mean_r2 = np.mean(r2_list)
std_r2 = np.std(r2_list)
print(f'Execute 1000 loops: r2={mean_r2:.3f}, std={std_r2:.3f}')

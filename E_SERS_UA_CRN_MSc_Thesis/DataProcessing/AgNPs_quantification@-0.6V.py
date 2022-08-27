import pandas as pd
import numpy as np
from scipy import stats
import matplotlib as mpl
from matplotlib import pyplot as plt

df_plot = pd.read_csv('../Data_csv/UA_quantification_average.csv')

df_plot = df_plot[df_plot.Potential == -0.6].iloc[:, 4:].T.rename(columns=df_plot.UA)
df_plot.index = pd.to_numeric(df_plot.index)

fig = plt.figure(figsize=[6, 7])
ax = plt.subplot()
count = 0
for i, col in df_plot.iteritems():
    plt.plot(col + 400 * count)
    ax.annotate(str(int(i)) + ' uM', (1700, 50 + 400 * count))
    ax.scatter(col.index[33], col.values[33] + 50 + 400 * count, marker='*', color='black')
    ax.scatter(col.index[163], col.values[163] + 50 + 400 * count, marker='+', color='black')
    ax.scatter(col.index[228], col.values[228] + 50 + 400 * count, marker='x', color='black')
    count += 1

ax.set_title('UA + 0.1M NaF + 10uM R6G for AgNPs-APTES-FTO at -0.6V', pad=10)
ax.set_xlabel('Raman Shift ($\mathregular{cm^{-1}}$)')
ax.set_ylabel('Intensity (counts $\mathregular{s^{-1}mW^{-1}}$)')

plt.savefig('../Data_Fig/UA_quantification_1.png')
plt.show()

df_linear = pd.read_csv('../Data_csv/UA_quantification_average.csv')
df_linear = df_linear[df_linear.Potential == -0.6].reset_index(drop=True)
df_normalised = df_linear.iloc[:, 4:].copy()
df_normalised = df_normalised.div(df_normalised['1362.89183'], axis=0)
df_linear = pd.concat([df_linear['UA'], df_normalised['1131.63641']], axis=1)

x = df_linear.drop([0])['UA']
y = df_linear.drop([0])['1131.63641']

slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)

df_all = pd.read_csv('../Data_csv/UA_quantification_all.csv')
df_all = df_all[df_all.Potential == -0.6].reset_index(drop=True)
df_normalised = df_all.iloc[:, 4:].copy()
df_normalised = df_normalised.div(df_normalised['1362.89183'], axis=0)
df_all = pd.concat([df_all['UA'], df_normalised['1131.63641']], axis=1)
df_all = df_all[df_all.UA != 0]
data_mean = df_all.groupby(['UA'])['1131.63641'].mean()
data_std = df_all.groupby(['UA'])['1131.63641'].std()

ax = plt.subplot()
ax.set_title('UA + 0.1M NaF + 10uM R6G for AgNPs-APTES-FTO at -0.6V', fontsize=10)
ax.set_title('Linear relationship: \n\ny = ' + str(format(slope, '.5f')) + 'x + ' + str(format(intercept, '.5f'))
             + '\nR$^{2}$ = ' + str(format(r_value, '.5f')), loc='left', y=0.75, x=0.05)

ax.set_xticks([1, 2, 3, 4, 6, 8, 10, 15])
ax.set_xticklabels(['1', '2', '5', '10', '20', '50', '100', '200'])
ax.set_xlabel('UA Concentration ($\mu$M)')
ax.set_ylabel('Peak Height After R6G Normalisation')

x = [1, 2, 3, 4, 6, 8, 10, 15]
ax.scatter(x, y, color='blue')
ax.errorbar(x, y, yerr=data_std, fmt='o', color='blue', capsize=3)

linear_model = np.polyfit(x, y, 1)
linear_model_fn = np.poly1d(linear_model)
x_s = np.arange(1, 16)
plt.plot(x_s, linear_model_fn(x_s), color='red', linestyle='--')

plt.savefig('../Data_Fig/UA_quantification_2.png')
plt.show()

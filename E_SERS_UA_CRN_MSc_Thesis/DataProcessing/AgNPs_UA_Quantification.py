from E_SERS_UA_CRN_MSc_Thesis.ReadData_Addition import *
from matplotlib import pyplot as plt

path_gamry = '../LabData_Derek/UA_Quantification/UA_EC'
path_raman = '../LabData_Derek/UA_Quantification/UA_SERS'

df_all, df_mean = ReadData(path_gamry, path_raman)

df_all.to_csv('../Data_csv/UA_quantification_all.csv', index=False)
df_mean.to_csv('../Data_csv/UA_quantification_average.csv', index=False)


# Plot different potentials at concentrations of UA = 50uM
df_plot = df_mean[df_mean.UA == 50].T
df_plot.columns = df_plot.iloc[3].tolist()
df_plot.drop(labels=['UA', 'CRN', 'R6G', 'Potential'], inplace=True)

fig = plt.figure(figsize=[6, 6])
ax = plt.subplot()
count = 0
for i, col in df_plot.iteritems():
    plt.plot(col+200*count)
    ax.annotate(str(i) + 'V', (1700, 30+200*count))
    ax.scatter(col.index[33], col.values[33]+30+200*count, marker='*', color='black')
    ax.scatter(col.index[163], col.values[163]+30+200*count, marker='+', color='black')
    ax.scatter(col.index[228], col.values[228]+30+200*count, marker='x', color='black')
    count += 1

ax.set_title('50uM UA + 0.1M NaF + 10uM R6G for AgNPs-APTES-FTO', pad=10)
ax.set_xlabel('Raman Shift ($\mathregular{cm^{-1}}$)')
ax.set_ylabel('Intensity (counts $\mathregular{s^{-1}mW^{-1}}$)')

plt.savefig('../Data_Fig/UA_quantification_50uM.png')
plt.show()


# Plot different concentrations of UA at potential = -0.6V
df_plot = df_mean[df_mean.Potential == -0.6].T
df_plot.columns = df_plot.iloc[0].tolist()
df_plot.drop(labels=['UA', 'CRN', 'R6G', 'Potential'], inplace=True)

fig = plt.figure(figsize=[6, 7])
ax = plt.subplot()
count = 0
for i, col in df_plot.iteritems():
    plt.plot(col+400*count)
    ax.annotate(str(int(i)) + ' uM', (1700, 50+400*count))
    ax.scatter(col.index[33], col.values[33]+50+400*count, marker='*', color='black')
    ax.scatter(col.index[163], col.values[163]+50+400*count, marker='+', color='black')
    ax.scatter(col.index[228], col.values[228]+50+400*count, marker='x', color='black')
    count += 1

ax.set_title('UA + 0.1M NaF + 10uM R6G for AgNPs-APTES-FTO at -0.6V', pad=10)
ax.set_xlabel('Raman Shift ($\mathregular{cm^{-1}}$)')
ax.set_ylabel('Intensity (counts $\mathregular{s^{-1}mW^{-1}}$)')

plt.savefig('../Data_Fig/UA_quantification_-0.6V.png')
plt.show()


# Plot different concentrations of UA at potential = 0.2V
df_plot = df_mean[df_mean.Potential == 0.2].T
df_plot.columns = df_plot.iloc[0].tolist()
df_plot.drop(labels=['UA', 'CRN', 'R6G', 'Potential'], inplace=True)

fig = plt.figure(figsize=[6, 7])
ax = plt.subplot()
count = 0
for i, col in df_plot.iteritems():
    plt.plot(col+400*count)
    ax.annotate(str(int(i)) + ' uM', (1700, 50+400*count))
    ax.scatter(col.index[33], col.values[33]+50+400*count, marker='*', color='black')
    ax.scatter(col.index[163], col.values[163]+50+400*count, marker='+', color='black')
    ax.scatter(col.index[228], col.values[228]+50+400*count, marker='x', color='black')
    count += 1

ax.set_title('UA + 0.1M NaF + 10uM R6G for AgNPs-APTES-FTO at 0.2V', pad=10)
ax.set_xlabel('Raman Shift ($\mathregular{cm^{-1}}$)')
ax.set_ylabel('Intensity (counts $\mathregular{s^{-1}mW^{-1}}$)')

plt.savefig('../Data_Fig/UA_quantification_0.2V.png')
plt.show()

from E_SERS_UA_CRN_MSc_Thesis.ReadData_Addition import *
from matplotlib import pyplot as plt

path_gamry = '../LabData_Derek/AgNPs_Multiplexed/Potential_Sequence'
path_raman = '../LabData_Derek/AgNPs_Multiplexed/Scan_RamanShift'

df_all, df_mean = ReadData(path_gamry, path_raman)

df_all.to_csv('../Data_csv/AgNPs_Multiplexed_all.csv', index=False)
df_mean.to_csv('../Data_csv/AgNPs_Multiplexed_average.csv', index=False)


# Plot different potentials at concentrations of UA = 50uM
df_plot = df_mean[df_mean.UA == 50].T
df_plot.columns = df_plot.iloc[3].tolist()
df_plot.drop(labels=['UA', 'CRN', 'R6G', 'Potential'], inplace=True)

fig = plt.figure(figsize=[6, 7])
ax = plt.subplot()
count = 0
for i, col in df_plot.iteritems():
    plt.plot(col+100*count)
    ax.annotate(str(i) + 'V', (1700, 10+100*count))
    ax.scatter(col.index[33], col.values[33]+10+100*count, marker='*', color='black')
    ax.scatter(col.index[44], col.values[44]+10+100*count, marker='.', color='black')
    ax.scatter(col.index[163], col.values[163]+10+100*count, marker='+', color='black')
    ax.scatter(col.index[228], col.values[228]+10+100*count, marker='x', color='black')
    count += 1

ax.set_title('50uM UA + 500uM CRN + 0.1M NaF + 10uM R6G', pad=10)
ax.set_xlabel('Raman Shift ($\mathregular{cm^{-1}}$)')
ax.set_ylabel('Intensity (counts $\mathregular{s^{-1}mW^{-1}}$)')

plt.savefig('../Data_Fig/UA_50uM_CRN_500uM.png')
plt.show()


# Plot different potentials at concentrations of UA = 5uM
df_plot = df_mean[df_mean.UA == 5].T
df_plot.columns = df_plot.iloc[3].tolist()
df_plot.drop(labels=['UA', 'CRN', 'R6G', 'Potential'], inplace=True)

fig = plt.figure(figsize=[6, 7])
ax = plt.subplot()
count = 0
for i, col in df_plot.iteritems():
    plt.plot(col+1000*count)
    ax.annotate(str(i) + 'V', (1700, 100+1000*count))
    ax.scatter(col.index[33], col.values[33]+100+1000*count, marker='*', color='black')
    ax.scatter(col.index[44], col.values[44]+100+1000*count, marker='.', color='black')
    ax.scatter(col.index[163], col.values[163]+100+1000*count, marker='+', color='black')
    ax.scatter(col.index[228], col.values[228]+100+1000*count, marker='x', color='black')
    count += 1

ax.set_title('50uM UA + 500uM CRN + 0.1M NaF + 10uM R6G', pad=10)
ax.set_xlabel('Raman Shift ($\mathregular{cm^{-1}}$)')
ax.set_ylabel('Intensity (counts $\mathregular{s^{-1}mW^{-1}}$)')

plt.savefig('../Data_Fig/UA_5uM_CRN_500uM.png')
plt.show()

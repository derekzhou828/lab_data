from E_SERS_UA_CRN_MSc_Thesis.ReadData import *
from matplotlib import pyplot as plt

path_gamry = '../LabData_Derek/AgNPs_APTES_FTO_UA_100uM_CRN_0uM_R6G_10uM_Jul11/Potential_Sequence'
path_raman = '../LabData_Derek/AgNPs_APTES_FTO_UA_100uM_CRN_0uM_R6G_10uM_Jul11/Scan_RamanShift'

df_all, df_mean = ReadData(path_gamry, path_raman)

df_all.to_csv('../Data_csv/AgNPs_UA_100uM_Jul11_all.csv', index=False)
df_mean.to_csv('../Data_csv/AgNPs_UA_100uM_Jul11_average.csv', index=False)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))
for ax in [ax1, ax2]:
    ax.set_title('100uM UA + 0.1M NaF + 10uM R6G for AgNPs-APTES-FTO')
    ax.set_xlabel('Raman Shift ($\mathregular{cm^{-1}}$)')
    ax.set_ylabel('Intensity (counts $\mathregular{s^{-1}mW^{-1}}$)')

df_plot = df_mean.iloc[:, 4:].T.rename(columns=df_mean['Potential'])
for i, col in df_plot.iloc[:, :9].iteritems():
    ax1.plot(col+1000*abs(i))
    ax1.annotate(str(i) + ' V', (1700, 10+1000*abs(i)))

for i, col in df_plot.iloc[:, 8:].iteritems():
    ax2.plot(col+1500*abs(i))
    ax2.annotate(str(i) + ' V', (1700, 15+1500*abs(i)))

plt.savefig('../Data_Fig/AgNPs_UA_100uM_Jul11_1.png')
plt.show()

from ReadData import *
from matplotlib import pyplot as plt

path_gamry = 'raw_data/AgNPs_APTES_FTO_UA_50uM_CRN_0uM_R6G_10uM_Jul5/Potential_Sequence'
path_raman = 'raw_data/AgNPs_APTES_FTO_UA_50uM_CRN_0uM_R6G_10uM_Jul5/Scan_RamanShift'

df_all, df_mean = ReadData(path_gamry, path_raman)

df_all.to_csv('initial_process/AgNPs_UA_50uM_Jul5_all.csv', index=False)
df_mean.to_csv('initial_process/AgNPs_UA_50uM_Jul5_average.csv', index=False)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))
for ax in [ax1, ax2]:
    ax.set_title('50uM UA + 0.1M NaF + 10uM R6G for AgNPs-APTES-FTO')
    ax.set_xlabel('Raman Shift ($\mathregular{cm^{-1}}$)')
    ax.set_ylabel('Intensity (counts $\mathregular{s^{-1}mW^{-1}}$)')

df_plot = df_mean.iloc[:, 4:].T.rename(columns=df_mean['Potential'])
for i, col in df_plot.iloc[:, :9].iteritems():
    ax1.plot(col+500*abs(i))
    ax1.annotate(str(i) + ' V', (1700, 5+500*abs(i)))

for i, col in df_plot.iloc[:, 8:].iteritems():
    ax2.plot(col+500*abs(i))
    ax2.annotate(str(i) + ' V', (1700, 5+500*abs(i)))

plt.savefig('fig_gallery/AgNPs_UA50uM_Jul5_1.png')
plt.show()

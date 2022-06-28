from ReadData import *
from matplotlib import pyplot as plt

path_gamry = 'raw_data/AgNPs_APTES_FTO_UA_100uM_CRN_0uM_R6G_10uM_Jun23/Potential_Sequence'
path_raman = 'raw_data/AgNPs_APTES_FTO_UA_100uM_CRN_0uM_R6G_10uM_Jun23/Scan_RamanShift'

df_all, df_mean = ReadData(path_gamry, path_raman)

df_all.to_csv('initial_process/AgNPs_UA_Jun23_all.csv', index=False)
df_mean.to_csv('initial_process/AgNPs_UA_Jun23_average.csv', index=False)


ax = plt.subplot()
df_plot = df_mean.iloc[:, 4:].T.rename(columns=df_mean['Potential'])
for i, col in df_plot.iteritems():
    plt.plot(col+200*abs(i))
    ax.annotate(str(i) + ' V', (1700, 4+200*abs(i)))

ax.set_title('100uM UA + 0.1M NaF + 10uM R6G for AgNPs-APTES-FTO')
ax.set_xlabel('Raman Shift ($\mathregular{cm^{-1}}$)')
ax.set_ylabel('Intensity (counts $\mathregular{s^{-1}mW^{-1}}$)')
ax.set_yticks([0, 20, 40, 60, 80, 100, 120, 140])
ax.set_yticklabels(['0', '20', '', '', '', '', '', ''])

plt.savefig('fig_gallery/AgNPs_UA_Jun23_1.png')
plt.show()

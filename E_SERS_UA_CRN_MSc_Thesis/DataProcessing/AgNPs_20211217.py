from E_SERS_UA_CRN_MSc_Thesis.ReadData_Addition import *
from matplotlib import pyplot as plt

path_gamry = '../E-SERS_UA+CRN+R6G_Addition/20211217/EC'
path_raman = '../E-SERS_UA+CRN+R6G_Addition/20211217/SERS'

df_all, df_mean = ReadData(path_gamry, path_raman)

df_all.to_csv('../Data_csv/20211217_all.csv', index=False)
df_mean.to_csv('../Data_csv/20211217_average.csv', index=False)

# Plot different concentrations of UA at potential = -0.6V
df_plot = df_mean[df_mean.Potential == -0.6].T
df_plot.columns = df_plot.iloc[0].tolist()
df_plot.drop(labels=['UA', 'CRN', 'R6G', 'Potential'], inplace=True)

ax = plt.subplot()
count = 0
for i, col in df_plot.iteritems():
    plt.plot(col+200*count)
    ax.annotate(str(int(i)) + ' uM', (1700, 50+200*count))
    count += 1

ax.set_title('UA + 0.1M NaF + 10uM R6G for AgNPs-APTES-FTO')
ax.set_xlabel('Raman Shift ($\mathregular{cm^{-1}}$)')
ax.set_ylabel('Intensity (counts $\mathregular{s^{-1}mW^{-1}}$)')

plt.savefig('../Data_Fig/UA_CRN_0uM_20211217.png')
plt.show()

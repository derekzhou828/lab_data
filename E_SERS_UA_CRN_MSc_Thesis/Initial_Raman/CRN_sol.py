import pandas as pd
from matplotlib import pyplot as plt
from E_SERS_UA_CRN_MSc_Thesis.ALSBaselineCorrection import *

df = pd.read_csv('../Initial_Raman/CRN_500uM.txt',
                 header=None, names=['wave', 'intst'], skiprows=range(14), sep='\t')
df = df[(df['wave'] > 500) & (df['wave'] < 1800)]
df['intst'] = (df['intst'] - ALSBaselineCorrection(df['intst'], p=0.0001)) / (7 * 22.5)

df.to_csv('../Initial_Raman/CRN_sol.csv', index=False)

wave, intst = df['wave'], df['intst']

ax = plt.subplot()
plt.plot(wave, intst)
plt.ylim(-0.5, 7)
ax.set_title('Raman Spectrum for Creatinine Solution', fontsize=14, pad=12)
ax.set_xlabel('Raman Shift ($\mathregular{cm^{-1}}$)', fontsize=13)
ax.set_ylabel('Intensity (counts $\mathregular{s^{-1}mW^{-1}}$)', fontsize=13)
ax.set_yticks([0, 1, 2, 3, 4, 5])
ax.set_yticklabels(['0', '1', '2', '3', '4', '5'])

plt.savefig('../Initial_Raman/CRN_sol.png')
plt.show()

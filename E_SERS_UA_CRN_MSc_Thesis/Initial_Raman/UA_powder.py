import pandas as pd
from matplotlib import pyplot as plt
from E_SERS_UA_CRN_MSc_Thesis.ALSBaselineCorrection import *

df = pd.read_csv('../Initial_Raman/UA_Powder_RamanShift_2.txt',
                 header=None, names=['wave', 'intst'], skiprows=range(14), sep='\t')
df = df[(df['wave'] > 500) & (df['wave'] < 1800)]
df['intst'] = (df['intst'] - ALSBaselineCorrection(df['intst'])) / (7 * 22.5)

df.to_csv('../Initial_Raman/UA_powder.csv', index=False)

wave, intst = df['wave'], df['intst']

ax = plt.subplot()
plt.plot(wave, intst)
plt.ylim(-2, 50)
ax.set_title('Raman Spectrum for Powder Uric Acid', fontsize=14, pad=12)
ax.set_xlabel('Raman Shift ($\mathregular{cm^{-1}}$)', fontsize=13)
ax.set_ylabel('Intensity (counts $\mathregular{s^{-1}mW^{-1}}$)', fontsize=13)
ax.set_yticks([0, 10, 20, 30, 40])
ax.set_yticklabels(['0', '10', '20', '30', '40'])

plt.savefig('../Initial_Raman/UA_powder.png')
plt.show()

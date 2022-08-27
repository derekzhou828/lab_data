import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from scipy.signal import argrelextrema

# read txt file
AgNP_df = pd.read_csv('UV-Vis-Jun9/AgNP_Absorbance_Jun9.txt', header=None, skiprows=range(35), sep='\t')
wavelen1, abs1 = AgNP_df[0], AgNP_df[1]
Au_Ag_df = pd.read_csv('UV-Vis-Jun9/Au@Ag_Absorbance_Jun9.txt', header=None, skiprows=range(35), sep='\t')
wavelen2, abs2 = Au_Ag_df[0], Au_Ag_df[1]

# plot AgNP spectra
plt.plot(wavelen1, abs1)
plt.xlim(300, 800)
plt.xlabel('Wavelength (nm)', fontsize=16)
plt.ylabel('Absorbance (arb.units)', fontsize=16)
plt.title('UV-Vis spectra of AgNPs', fontsize=16)
# find peak for AgNP
index1 = argrelextrema(abs1.values, np.greater, order=50)[0][1]
peak_x1 = wavelen1.iloc[index1]
peak_y1 = abs1.iloc[index1]
plt.scatter(peak_x1, peak_y1, marker='o', color='red')
xy_str1 = str('('+str(int(peak_x1))+', '+str(round(peak_y1, 2))+')')
plt.annotate(xy_str1, (peak_x1, peak_y1), xycoords='data',
             xytext=(peak_x1+50, peak_y1+0.1), arrowprops=dict(arrowstyle='->'))
plt.savefig('UV-Vis spectra of AgNPs.png')
plt.show()

# plot Au@Ag spectra
plt.plot(wavelen2, abs2)
plt.xlim(300, 800)
plt.xlabel('Wavelength (nm)', fontsize=16)
plt.ylabel('Absorbance (arb.units)', fontsize=16)
plt.title('UV-Vis spectra of Au@Ag', fontsize=16)
index2 = argrelextrema(abs2.values, np.greater, order=50)[0][1]
peak_x2 = wavelen1.iloc[index2]
peak_y2 = abs2.iloc[index2]
plt.scatter(peak_x2, peak_y2, marker='o', color='red')
xy_str2 = str('('+str(int(peak_x2))+', '+str(round(peak_y2, 2))+')')
plt.annotate(xy_str2, (peak_x2, peak_y2), xycoords='data',
             xytext=(peak_x2+100, peak_y2-0.1), arrowprops=dict(arrowstyle='->'))
plt.savefig('UV-Vis spectra of Au@Ag.png')
plt.show()

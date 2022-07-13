from E_SERS_UA_CRN_MSc_Thesis.ReadData_Addition import *
from matplotlib import pyplot as plt

path_gamry = '../E-SERS_UA+CRN+R6G_Addition/20211215/EC'
path_raman = '../E-SERS_UA+CRN+R6G_Addition/20211215/SERS'

df_all, df_mean = ReadData(path_gamry, path_raman, 360)

df_all.to_csv('../Data_csv/20211215_all.csv', index=False)
df_mean.to_csv('../Data_csv/20211215_average.csv', index=False)

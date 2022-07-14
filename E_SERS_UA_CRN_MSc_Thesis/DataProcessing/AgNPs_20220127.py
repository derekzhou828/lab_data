from E_SERS_UA_CRN_MSc_Thesis.ReadData_Addition import *
from matplotlib import pyplot as plt

path_gamry = '../E-SERS_UA+CRN+R6G_Addition/20220127/EC'
path_raman = '../E-SERS_UA+CRN+R6G_Addition/20220127/SERS'

df_all, df_mean = ReadData(path_gamry, path_raman)

df_all.to_csv('../Data_csv/20220127_all.csv', index=False)
df_mean.to_csv('../Data_csv/20220127_average.csv', index=False)

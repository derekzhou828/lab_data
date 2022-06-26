import os
import re
import time
import pandas as pd
from ALSBaselineCorrection import *


def ReadData(path_gamry='', path_raman='', date='2022-6-23'):

    files_gamry = os.listdir(path_gamry)
    time_potential = {}

    for file in files_gamry:
        with open(os.path.join(path_gamry, file), 'r') as f:
            lines = f.readlines()
            potential = lines[10].split('\t')[2].split('\t')[0]
            time_str = date + ' ' + lines[4].split('\t')[2].split('\t')[0]
            time_array = time.strptime(time_str, '%Y-%m-%d %H:%M:%S')
            time_stamp = int(time.mktime(time_array))
            time_potential[time_stamp] = potential
            time_line = sorted(list(time_potential.keys()))

    files_raman = os.listdir(path_raman)
    data_single = []

    for file in files_raman:
        UA = int(re.search(r'UA_+([0-9]+uM)', file).group(1).removesuffix('uM'))
        CRN = int(re.search(r'CRN_+([0-9]+uM)', file).group(1).removesuffix('uM'))
        R6G = int(re.search(r'R6G_+([0-9]+uM)', file).group(1).removesuffix('uM'))

        df = pd.read_csv(
            os.path.join(path_raman, file),
            header=None, skiprows=range(14), names=['wave', 'intst'], sep='\t'
        )
        df = df[(df['wave'] > 500) & (df['wave'] < 1800)]
        df['intst'] -= ALSBaselineCorrection(df['intst'])

        with open(os.path.join(path_raman, file), 'r') as f:
            lines = f.readlines()
            time_str = date + ' ' + lines[2].split(' ')[4]
            time_array = time.strptime(time_str, '%Y-%m-%d %H:%M:%S')
            time_stamp = int(time.mktime(time_array))

        for i in range(len(time_line)):
            if (time_stamp > time_line[i]) & ((time_stamp + 70) < time_line[i] + 300):
                potential = float(time_potential[time_line[i]])
                data_single.append([file, UA, CRN, R6G, potential] + df['intst'].tolist())

    df_all = pd.DataFrame(
        data_single, columns=['Filename', 'UA', 'CRN', 'R6G', 'Potential'] + df['wave'].tolist()
    )

    df_mean = pd.DataFrame()
    for p, g in df_all.groupby(df_all['Potential']):
        mean = round(g.mean(numeric_only=True), 1)
        df = pd.DataFrame([mean], columns=mean.index)
        df_mean = pd.concat([df_mean, df], ignore_index=True)

    return df_all, df_mean

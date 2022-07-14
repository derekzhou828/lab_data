import os
import re
import time
import pandas as pd
from E_SERS_UA_CRN_MSc_Thesis.ALSBaselineCorrection import *


def ReadData(path_gamry='', path_raman='', duration=300, date='2022-6-23'):

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
            time_list = sorted(list(time_potential.keys()))

            time_line = []
            for i in range(len(time_list)-1):
                if time_list[i+1] - time_list[i] > duration:
                    time_line.append(time_list[i])
            time_line.append(time_list[-1])

    files_raman = os.listdir(path_raman)
    data_single = []

    for file in files_raman:
        UA = re.search(r'UA_+([0-9.]+[um][mM])', file)
        if UA is not None:
            UA = UA.group(1)
            if UA.endswith('uM'):
                UA = float(UA.removesuffix('uM'))
            elif UA.endswith('um'):
                UA = float(UA.removesuffix('um'))
            else:
                UA = float(UA.removesuffix('mM')) * 1E+3
        else:
            UA = 0.0

        CRN = re.search(r'CRN_+([0-9.]+[um]M)', file)
        if CRN is not None:
            CRN = CRN.group(1)
            if CRN.endswith('uM'):
                CRN = float(CRN.removesuffix('uM'))
            else:
                CRN = float(CRN.removesuffix('mM')) * 1E+3
        else:
            CRN = 0.0

        R6G = re.search(r'R6G_+([0-9.]+[um]M)', file)
        if R6G is not None:
            R6G = R6G.group(1)
            if R6G.endswith('uM'):
                R6G = float(R6G.removesuffix('uM'))
            else:
                R6G = float(R6G.removesuffix('mM')) * 1E+3
        else:
            R6G = 10.0

        df = pd.read_csv(
            os.path.join(path_raman, file),
            header=None, skiprows=range(14), names=['wave', 'intst'], sep='\t'
        )
        df = df[(df['wave'] > 500) & (df['wave'] < 1800)]
        df['intst'] = (df['intst'] - ALSBaselineCorrection(df['intst'])) / (7*22.5)

        with open(os.path.join(path_raman, file), 'r') as f:
            lines = f.readlines()
            time_str = date + ' ' + lines[2].split(' ')[4]
            time_array = time.strptime(time_str, '%Y-%m-%d %H:%M:%S')
            time_stamp = int(time.mktime(time_array))

        for i in range(len(time_line)):
            if (time_stamp > time_line[i]) & ((time_stamp + 70) <= time_line[i] + duration):
                potential = float(time_potential[time_line[i]])
                data_single.append([file, UA, CRN, R6G, potential] + df['intst'].tolist())

    df_all = pd.DataFrame(data_single, columns=['Filename', 'UA', 'CRN', 'R6G', 'Potential'] + df['wave'].tolist())

    df_mean = pd.DataFrame()
    for i, p in df_all.groupby(['UA', 'CRN', 'Potential']):
        mean = p.mean(numeric_only=True)
        df = pd.DataFrame([mean], columns=mean.index)
        df['Potential'] = round(df['Potential'], 1)
        df_mean = pd.concat([df_mean, df])

    return df_all, df_mean

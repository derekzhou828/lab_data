import pandas as pd

df_20211215 = pd.read_csv('../Data_csv/20211215_all.csv').drop(columns=['Filename', 'R6G'], axis=1)
df_20211217 = pd.read_csv('../Data_csv/20211217_all.csv').drop(columns=['Filename', 'R6G'], axis=1)
df_20211220 = pd.read_csv('../Data_csv/20211220_all.csv').drop(columns=['Filename', 'R6G'], axis=1)
df_20211221 = pd.read_csv('../Data_csv/20211221_all.csv').drop(columns=['Filename', 'R6G'], axis=1)
df_20220127 = pd.read_csv('../Data_csv/20220127_all.csv').drop(columns=['Filename', 'R6G'], axis=1)
df_20220202 = pd.read_csv('../Data_csv/20220202_all.csv').drop(columns=['Filename', 'R6G'], axis=1)
df_20220207 = pd.read_csv('../Data_csv/20220207_all.csv').drop(columns=['Filename', 'R6G'], axis=1)
df_20220210 = pd.read_csv('../Data_csv/20220210_all.csv').drop(columns=['Filename', 'R6G'], axis=1)
df_20220217 = pd.read_csv('../Data_csv/20220217_all.csv').drop(columns=['Filename', 'R6G'], axis=1)
df_20220221 = pd.read_csv('../Data_csv/20220221_all.csv').drop(columns=['Filename', 'R6G'], axis=1)
df_20220324 = pd.read_csv('../Data_csv/20220324_all.csv').drop(columns=['Filename', 'R6G'], axis=1)

df_DataTJ = pd.concat(
    [df_20211215, df_20211217, df_20211220, df_20211221, df_20220127, df_20220202, df_20220207,
     df_20220210, df_20220217, df_20220221, df_20220324], ignore_index=True)

df_DataTJ.to_csv('../Data_csv/DataTJ.csv', index=False)

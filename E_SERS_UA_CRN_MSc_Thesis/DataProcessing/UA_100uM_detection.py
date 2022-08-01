import pandas as pd
from matplotlib import pyplot as plt

df_AgNPs = pd.read_csv('../Data_csv/AgNPs_UA_100uM_Jul11_average.csv')
df_AuAg = pd.read_csv('../Data_csv/Au@AgCoreShell_UA_Jun29_average.csv')

# plot AgNPs
df_plot = df_AgNPs.iloc[:, 4:].T.rename(columns=df_AgNPs['Potential'])
df_plot.index = pd.to_numeric(df_plot.index)

fig = plt.figure(figsize=[6, 7])
ax = plt.subplot()

count = 0
for i, col in df_plot.iteritems():
    ax.plot(col+150*count)
    ax.annotate(str(i) + ' V', (1700, 15+150*count))
    ax.scatter(col.index[33], col.values[33]+15+150*count, marker='*', color='black')
    ax.scatter(col.index[163], col.values[163]+15+150*count, marker='+', color='black')
    ax.scatter(col.index[228], col.values[228]+15+150*count, marker='x', color='black')
    count += 1

ax.set_title('100uM UA + 0.1M NaF + 10uM R6G for AgNPs', pad=10)
ax.set_xlabel('Raman Shift ($\mathregular{cm^{-1}}$)')
ax.set_ylabel('Intensity (counts $\mathregular{s^{-1}mW^{-1}}$)')

plt.savefig('../Data_Fig/UA_detection_AgNPs.png')
plt.show()

# plot Au@Ag Core-shell NPs
df_plot = df_AuAg.iloc[:, 4:].T.rename(columns=df_AuAg['Potential'])
df_plot.index = pd.to_numeric(df_plot.index)

fig = plt.figure(figsize=[6, 7])
ax = plt.subplot()

count = 0
for i, col in df_plot.iloc[:, :-1].iteritems():
    ax.plot(col+25*count)
    ax.annotate(str(i) + ' V', (1700, 3+25*count))
    ax.scatter(col.index[33], col.values[33]+3+25*count, marker='*', color='black')
    ax.scatter(col.index[163], col.values[163]+3+25*count, marker='+', color='black')
    ax.scatter(col.index[228], col.values[228]+3+25*count, marker='x', color='black')
    count += 1

ax.set_title('100uM UA + 0.1M NaF + 10uM R6G for Au@AgNPs', pad=10)
ax.set_xlabel('Raman Shift ($\mathregular{cm^{-1}}$)')
ax.set_ylabel('Intensity (counts $\mathregular{s^{-1}mW^{-1}}$)')

plt.savefig('../Data_Fig/UA_detection_Au@AgNPs.png')
plt.show()

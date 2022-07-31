from E_SERS_UA_CRN_MSc_Thesis.ReadData_Addition import *
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


path_gamry = '../E-SERS_UA+CRN+R6G_Addition/20211217/EC'
path_raman = '../E-SERS_UA+CRN+R6G_Addition/20211217/SERS'

df_all, df_mean = ReadData(path_gamry, path_raman)

df_all.to_csv('../Data_csv/20211217_all.csv', index=False)
df_mean.to_csv('../Data_csv/20211217_average.csv', index=False)

# Plot different concentrations of UA at potential = -0.6V
df_plot = df_mean[df_mean.Potential == -0.6].T
df_plot.columns = df_plot.iloc[0].tolist()
df_plot.drop(labels=['UA', 'CRN', 'R6G', 'Potential'], inplace=True)

fig = plt.figure(figsize=[9, 9])
ax = fig.add_subplot(projection='3d')
xs = list(df_plot.index)

for z in range(df_plot.shape[1]):
    ys = df_plot.iloc[:, z].values
    ax.plot(xs, ys, zs=z, zdir='y', alpha=0.8)
    ax.scatter(xs[33], z, ys[33]+15, marker='*', color='black')
    ax.scatter(xs[228], z, ys[228]+15, marker='x', color='black')

ax.w_xaxis.set_pane_color((1.0, 1.0, 1.0, 1.0))
ax.w_yaxis.set_pane_color((1.0, 1.0, 1.0, 1.0))
#ax.w_zaxis.set_pane_color((1.0, 1.0, 1.0, 1.0))
ax.get_proj = lambda: np.dot(Axes3D.get_proj(ax), np.diag([1.1, 4.5, 0.5, 1]))
ax.view_init(16, 278)

# ax.set_xlabel('Raman Shift ($\mathregular{cm^{-1}}$)', fontsize=12, labelpad=6)
# ax.set_ylabel('Uric acid Concentration ($\mu$M)', fontsize=12, labelpad=15)
ax.set_yticks(range(df_plot.shape[1]))
ax.set_yticklabels(list(df_plot))
# ax.set_zlabel('Intensity (counts $\mathregular{s^{-1}mW^{-1}}$)', fontsize=12, labelpad=10)
ax.set_zticks([100, 200])
ax.set_zticklabels(['100', '200'])
ax.grid(False)

plt.savefig('../Data_Fig/UA_CRN_0uM_20211217_2.png')
plt.show()

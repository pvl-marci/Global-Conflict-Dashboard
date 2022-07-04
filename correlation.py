import pandas as pd
import seaborn as sn
import matplotlib.pyplot as plt

df = pd.read_csv('datasets\owid_conflicts_gni.csv')
df['year'] = pd.to_datetime(df['year'])


matrix = df.corr(method='pearson')
sn.heatmap(matrix, annot=True)
plt.show()

import pandas as pd
import seaborn as sn
import matplotlib.pyplot as plt

df = pd.read_csv('datasets/hiik_conflicts_mil_spendings.csv', sep=';')

df['year'] = pd.to_datetime(df['year'])


matrix = df.corr(method='spearman')
sn.heatmap(matrix, annot=True)
plt.show()

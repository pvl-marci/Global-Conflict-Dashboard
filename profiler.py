
import numpy as np
import pandas as pd
from pandas_profiling import ProfileReport

df = pd.concat(
    map(pd.read_csv, ['ukraine_google_trends.csv', 'afghanistan_google_trends.csv']), ignore_index=True)

df['Woche'] = pd.to_datetime(df['Woche'])


df['Woche'] = pd.to_datetime(df['Woche'])
profile = ProfileReport(df, title='Report')
profile.to_file("your_report.html")

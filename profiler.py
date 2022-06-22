
import numpy as np
import pandas as pd
from pandas_profiling import ProfileReport

df = pd.read_csv('datasets//testtable.csv', sep=';')

df['year'] = pd.to_datetime(df['year'])


profile = ProfileReport(df, title='Report')
profile.to_file("test_report.html")

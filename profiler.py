
import numpy as np
import pandas as pd
from pandas_profiling import ProfileReport

df = pd.read_csv('datasets\owid_conflicts_gni.csv')

df['year'] = pd.to_datetime(df['year'])


profile = ProfileReport(df, title='Report')
profile.to_file("owid_gni_report.html")

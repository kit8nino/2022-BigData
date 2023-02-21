import tensorflow
import pandas as pd

df = pd.read_csv('survey.csv')
df.head()

df.shape
df.info()
df.describe()
df.nunique()

ft_names = df.columns.tolist()
for column in ft_names:
    print(column)
    print(df[column].value_counts(dropna=False))

features = df.drop('treatment', 1)
labels = df['treatment']

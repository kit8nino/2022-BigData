import pandas as pd

df = pd.read_csv('survey.csv')
# https://www.kaggle.com/datasets/osmi/mental-health-in-tech-survey
"""
df.head()

df.shape
df.info()
df.describe()
df.nunique()
"""

ft_names = df.columns.tolist()
for column in ft_names:
    print(column)
    print(df[column].value_counts(dropna=False))

# df.Age - убрать все, что не входит в диапазон от 15 до 100 лет

# df.Gender - почистить на 3 категории: М, Ж и все остальное

# df.work_interfere - перевести в значения от 0 до 3

# df.no_employees - перевести в значения от 0 до 5:
           # ['6-25', 'More than 1000', '26-100', '100-500', '1-5', '500-1000']

# features = df.drop('treatment', 1)
# labels = df['treatment']

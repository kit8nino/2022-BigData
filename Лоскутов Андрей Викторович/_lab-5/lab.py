import pandas as pd
import numpy as np

df = pd.read_csv('.\_lab-5\survey.csv')
# https://www.kaggle.com/datasets/osmi/mental-health-in-tech-survey
"""
df.head()

df.shape
df.info()
df.describe()
df.nunique()
"""

# df.Age - убрать все, что не входит в диапазон от 15 до 100 лет

for i in range(df.shape[0]):
    if df.loc[i, 'Age'] > 100 or df.loc[i, 'Age'] < 15:
        df.loc[i, 'Age'] = np.nan

print('Age\t\tproportion\t\tdispersion\t\tmean')

# df.Gender - почистить на 3 категории: М, Ж и все остальное

df.Gender = df.Gender.str.lower()

for i in range(df.shape[0]):
    if str(df.loc[i, 'Gender']).__contains__('trans'):
        df.loc[i, 'Gender'] = 'o'
    elif str(df.loc[i, 'Gender']).__contains__('female'):
        df.loc[i, 'Gender'] = 'f'
    elif str(df.loc[i, 'Gender']).__contains__('woman'):
        df.loc[i, 'Gender'] = 'f'
    elif str(df.loc[i, 'Gender']).__contains__('fem'):
        df.loc[i, 'Gender'] = 'f'
    elif str(df.loc[i, 'Gender']).__contains__('male'):
        df.loc[i, 'Gender'] = 'm'
    elif str(df.loc[i, 'Gender']).__contains__('man'):
        df.loc[i, 'Gender'] = 'm'
    elif str(df.loc[i, 'Gender']).__contains__('ma'):
        df.loc[i, 'Gender'] = 'm'
    elif str(df.loc[i, 'Gender']) != 'F' and str(df.loc[i, 'Gender']) != 'M':
        df.loc[i, 'Gender'] = 'o'

# df.work_interfere - перевести в значения от 0 до 3
df.work_interfere.replace(['Often', 'Sometimes', 'Rarely', 'Never'], [3, 2, 1, 0], inplace=True)

# df.no_employees - перевести в значения от 0 до 5:
           # ['6-25', 'More than 1000', '26-100', '100-500', '1-5', '500-1000']
df.no_employees.replace(['More than 1000', '500-1000', '100-500', '26-100', '6-25', '1-5'], [5, 4, 3, 2, 1, 0], inplace=True)

# df.self_employed
df.self_employed.replace(['Yes', 'No'], [1, 0], inplace=True)

# df.family_history
df.family_history.replace(['Yes', 'No'], [1, 0], inplace=True)

# df.coworkers
df.coworkers.replace(['Yes', 'Some of them', 'No'], [2, 1, 0], inplace=True)

# df.supervisor
df.supervisor.replace(['Yes', 'Some of them', 'No'], [2, 1, 0], inplace=True)

# df.mental_health_interview
df.mental_health_interview.replace(['Yes', 'Maybe', 'No'], [2, 1, 0], inplace=True)

# df.phys_health_interview
df.phys_health_interview.replace(['Yes', 'Maybe', 'No'], [2, 1, 0], inplace=True)

# df.mental_vs_physical
df.mental_vs_physical.replace(['Yes', 'No', 'Don\'t know'], [1, 0, np.nan], inplace=True)

# df.obs_consequence
df.obs_consequence.replace(['Yes', 'No'], [1, 0], inplace=True)

# features = df.drop('treatment', 1)
# labels = df['treatment']

print(df.head())

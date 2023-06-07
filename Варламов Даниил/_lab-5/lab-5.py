import pandas as pd

df = pd.read_csv(r'Варламов Даниил/_lab-5/survey.csv')
# https://www.kaggle.com/datasets/osmi/mental-health-in-tech-survey
"""
df.head()

df.shape
df.info()
df.describe()
df.nunique()
"""




# ft_names = df.columns.tolist()
# for column in ft_names:
#     print(column)
#     print(df[column].value_counts(dropna=False))


# df.Gender - почистить на 3 категории: М, Ж и все остальное

df.Gender = df.Gender.str.upper()

for i in range(df.shape[0]):
    if str(df.Gender[i]).__contains__('TRANS'):
        df.Gender[i] = 'Other'
    elif str(df.Gender[i]).__contains__('MALE'):
        df.Gender[i] = 'M'
    elif str(df.Gender[i]).__contains__('MAN'):
        df.Gender[i] = 'M'
    elif str(df.Gender[i]).__contains__('MA'):
        df.Gender[i] = 'M'
    elif str(df.Gender[i]).__contains__('FEMALE'):
        df.Gender[i] = 'F'
    elif str(df.Gender[i]).__contains__('WOMAN'):
        df.Gender[i] = 'F'
    elif str(df.Gender[i]).__contains__('FEM'):
        df.Gender[i] = 'F'
    elif str(df.Gender[i]) != 'F' and str(df.Gender[i]) != 'M':
        df.Gender[i] = 'Other'


# df.Age - убрать все, что не входит в диапазон от 15 до 100 лет

df = df.loc[df.Age > 15]

df = df.loc[df.Age < 100]

df = df.reset_index(drop=True)

# df.work_interfere - перевести в значения от 0 до 3
df.work_interfere = df.work_interfere.str.upper()

for i in range (df.shape[0]):
    if str(df.work_interfere[i]) == 'OFTEN':
        df.work_interfere[i] = 3
    elif str(df.work_interfere[i]) == 'RARELY':
        df.work_interfere[i] = 2
    elif str(df.work_interfere[i]) == 'NEVER':
        df.work_interfere[i] = 0
    elif str(df.work_interfere[i]) == 'SOMETIMES':
        df.work_interfere[i] = 1

df = df.loc[(df.work_interfere == 0) | (df.work_interfere == 1) | (df.work_interfere == 2) | (df.work_interfere == 3)]

df = df.reset_index(drop=True)

# df.no_employees - перевести в значения от 0 до 5:
        # ['6-25', 'More than 1000', '26-100', '100-500', '1-5', '500-1000']

df.no_employees = df.no_employees.str.upper()
print(df.no_employees.unique())

for i in range (df.shape[0]):
    if str(df.no_employees[i]) == '1-5':
        df.no_employees[i] = 0
    elif str(df.no_employees[i]) == '6-25':
        df.no_employees[i] = 1
    elif str(df.no_employees[i]) == '26-100':
        df.no_employees[i] = 2
    elif str(df.no_employees[i]) == '100-500':
        df.no_employees[i] = 3 
    elif str(df.no_employees[i]) =='500-1000':
        df.no_employees[i] = 4
    elif str(df.no_employees[i]) == 'MORE THAN 1000':
        df.no_employees[i] = 5




for i in range (df.shape[0]):
    if str(df.leave[i]) == 'Very easy':
        df.leave[i] = 1
    elif str(df.leave[i]) == "Don't know":
        df.leave[i] = 0
    elif str(df.leave[i]) == 'Somewhat easy':
        df.leave[i] = 2
    elif str(df.leave[i]) == 'Somewhat difficult':
        df.leave[i] = 3
    elif str(df.leave[i]) == 'Very difficult':
        df.leave[i] = 4
    




for i in range (df.shape[0]):
    if df.family_history[i] == 'Yes':
        df.family_history[i] = 1
    elif df.family_history[i] == 'No':
        df.family_history[i] = 0


for i in range (df.shape[0]):
    if df.self_employed[i] == 'Yes':
        df.self_employed[i] = 1
    elif df.self_employed[i] == 'No':
        df.self_employed[i] = 0

df = df.loc[(df.self_employed == 1) | (df.self_employed == 0)]

df = df.reset_index(drop=True)

for i in range (df.shape[0]):
    if df.treatment[i] == 'Yes':
        df.treatment[i] = 1
    elif df.treatment[i] == 'No':
        df.treatment[i] = 0




for i in range (df.shape[0]):
    if df.remote_work[i] == 'Yes':
        df.remote_work[i] = 1
    elif df.remote_work[i] == 'No':
        df.remote_work[i] = 0

print(df.tech_company.unique())
# tech_company                   2
# benefits                       3
# care_options                   3
# wellness_program               3
# seek_help                      3
# anonymity                      3
# leave                          5
# mental_health_consequence      3
# phys_health_consequence        3
# coworkers                      3
# supervisor                     3
# mental_health_interview        3
# phys_health_interview          3
# mental_vs_physical             3
# obs_consequence                2
# comments                     137
# df.to_csv(r'Варламов Даниил/_lab-5/survey1.csv',sep=',')

# features = df.drop('treatment', 1)
# labels = df['treatment']

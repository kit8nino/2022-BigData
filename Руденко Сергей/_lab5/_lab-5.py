import scipy as sp
from scipy import stats
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
pd.options.mode.chained_assignment = None
df = pd.read_csv(r'Rudenko-Sergey/_lab-5/survey.csv')
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



# df = df.loc[(df.work_interfere == 0) | (df.work_interfere == 1) | (df.work_interfere == 2) | (df.work_interfere == 3)]

# df = df.reset_index(drop=True)

# df.no_employees - перевести в значения от 0 до 5:
        # ['6-25', 'More than 1000', '26-100', '100-500', '1-5', '500-1000']

df.no_employees = df.no_employees.str.upper()

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
    

for i in df.head():
    for j in range (df.shape[0]):
        if df[f'{i}'][j] == 'Yes':
            df[f'{i}'][j] = 1
        elif df[f'{i}'][j] == 'No':
            df[f'{i}'][j] = 0


dkv = df.copy() # Доля каждого варианта
for i in dkv.head():
    if i != 'Timestamp' and i != 'comments':
        for k,v in dkv[f'{i}'].value_counts(normalize = True).items():
            for j in range (dkv.shape[0]):
                if dkv[f'{i}'][j] == k:
                    dkv[f'{i}'][j] = v

# df.to_csv(r'Варламов Даниил/_lab-5/res.csv')

disp = df.copy() # дисперсия

for i in disp.head():
    if i != 'Timestamp' and i != 'comments':
        try:
            disp[f'{i}'] = disp[f'{i}'].var()
        except Exception:
            pass

avg = df['Age'].mean()

median = df.copy()
median = median.median()




treatment_mean = df['treatment'].mean()
treatment_above_mean = df[df['treatment'] > treatment_mean]
treatment_ratio = len(treatment_above_mean) / len(df)






fig, ax = plt.subplots()
sns.countplot(x="treatment", hue="Gender", data=df, ax=ax)
ax.set_title("Treatment by Gender")
plt.show()

fig, ax = plt.subplots()
sns.countplot(x="treatment", hue="leave", data=df, ax=ax)
ax.set_title("Treatment by Leave")
plt.show()

fig, ax = plt.subplots()
sns.countplot(x="treatment", hue="no_employees", data=df, ax=ax)
ax.set_title("Treatment by No. of Employees")
plt.show()




# for i in dkv.head():
#     if i != 'Timestamp' and i != 'comments':
#         for k,v in dkv[f'{i}'].value_counts(normalize = True).items():
#             for j in range (dkv.shape[0]):
#                 if dkv[f'{i}'][j] == k:
#                     dkv[f'{i}'][j] = v
"""

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


for i in range (df.shape[0]):
    if df.tech_company[i] == 'Yes':
        df.tech_company[i] = 1
    elif df.tech_company[i] == 'No':
        df.tech_company[i] = 0

for i in range (df.shape[0]):
    if df.benefits[i] == 'Yes':
        df.benefits[i] = 1
    elif df.benefits[i] == 'No':
        df.benefits[i] = 0


for i in range (df.shape[0]):
    if df.care_options[i] == 'Yes':
        df.care_options[i] = 1
    elif df.care_options[i] == 'No':
        df.care_options[i] = 0


for i in range (df.shape[0]):
    if df.wellness_program[i] == 'Yes':
        df.wellness_program[i] = 1
    elif df.wellness_program[i] == 'No':
        df.wellness_program[i] = 0



for i in range (df.shape[0]):
    if df.seek_help[i] == 'Yes':
        df.seek_help[i] = 1
    elif df.seek_help[i] == 'No':
        df.seek_help[i] = 0


for i in range (df.shape[0]):
    if df.anonymity[i] == 'Yes':
        df.anonymity[i] = 1
    elif df.anonymity[i] == 'No':
        df.anonymity[i] = 0


for i in range (df.shape[0]):
    if df.mental_health_consequence[i] == 'Yes':
        df.mental_health_consequence[i] = 1
    elif df.mental_health_consequence[i] == 'No':
        df.mental_health_consequence[i] = 0


for i in range (df.shape[0]):
    if df.phys_health_consequence[i] == 'Yes':
        df.phys_health_consequence[i] = 1
    elif df.phys_health_consequence[i] == 'No':
        df.phys_health_consequence[i] = 0

"""





# features = df.drop('treatment', 1)
# labels = df['treatment']

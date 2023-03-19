import pandas as pd
import numpy as np
import re
from functools import partial
import spacy

df = pd.read_csv('_lab-5\survey.csv')
nlp = spacy.load('en_core_web_sm') # для оценки схожести слов (в Gender)
# https://www.kaggle.com/datasets/osmi/mental-health-in-tech-survey

def valueToInt(x, dict, name): # оцифровывание по словарю
    if x in dict:
        df.loc[df[name] == x, name] = dict[x]
        
def valueToIntYesNo(x, name): # оцифровывания по да/нет
    if x != 0 and x!=1:
        df.loc[df[name] == x, name] = 0 if (x=="No") else (1 if (x=="Yes") else np.NaN)

def Age():
    df['Age'].mask((df['Age'] > 100) | (df['Age'] < 15), inplace=True)

def Gender():
    def GenderToInt(row):
        females = ['female', 'women', 'f', 'fem', 'girl']
        males = ['male', 'man', 'm', 'mail', 'guy']
        for i in range(0,len(females)):
            rowChange = re.sub('[^a-zа-я ]', '', str(row).lower().replace('/',' ')).replace('cis','').split()
            if rowChange:
                if rowChange[0] == "trans": df['Gender'].mask(df['Gender']==row, 2, inplace=True)
                elif nlp(rowChange[0]).similarity(nlp(females[i]))>0.7: df['Gender'].mask(df['Gender']==row, 0, inplace=True)
                elif nlp(rowChange[0]).similarity(nlp(males[i]))>0.5: df['Gender'].mask(df['Gender']==row, 1, inplace=True)
                else: df['Gender'].mask(df['Gender']==row, 2, inplace=True)
    pd.Series(map(GenderToInt, df['Gender']), df['Gender'])

def Leave():
    name='leave'
    dict={'Very easy': 0,'Somewhat easy': 1, 'Don\'t know': 2,'Somewhat difficult': 3,'Very difficult': 4}  
    mapfunc = partial(valueToInt, dict=dict, name=name)
    pd.Series(map(mapfunc, df[name]), df[name])

def No_employees():
    name='no_employees'
    dict={'1-5': 0,'6-25': 1, '26-100': 2,'100-500': 3, '500-1000': 4,'More than 1000': 5}
    mapfunc = partial(valueToInt, dict=dict, name=name)
    pd.Series(map(mapfunc, df[name]), df[name])

def Work_interfere():
    name='work_interfere'
    dict={'Never': 0,'Rarely': 1, 'Sometimes': 2,'Often': 3}  
    mapfunc = partial(valueToInt, dict=dict, name=name)
    pd.Series(map(mapfunc, df[name]), df[name])

def YesNo():
    dfNamesYesNo = ['self_employed','family_history', 'treatment', 'remote_work', 'tech_company', 'benefits', 'care_options', 'wellness_program', 'seek_help', 'anonymity', 'mental_health_consequence', 'phys_health_consequence', 'coworkers', 'supervisor', 'mental_health_interview', 'phys_health_interview', 'mental_vs_physical', 'obs_consequence']
    for name in dfNamesYesNo:
        mapfunc = partial(valueToIntYesNo, name=name)
        pd.Series(map(mapfunc, df[name]))

def callFuncs():
    Age()
    Gender()
    Leave()
    No_employees()
    Work_interfere()
    YesNo()

callFuncs()
print(df)

df.to_csv("_lab-5\\newsurvey.csv", mode='a', index= False, encoding='utf-8')


"""
ft_names = df.columns.tolist()

for column in ft_names:
     print(column)
     print(df[column].value_counts(dropna=False))


features = df.drop('treatment', 1)
labels = df['treatment']

df.head()
df.shape
df.info()
df.describe()
df.nunique()
"""
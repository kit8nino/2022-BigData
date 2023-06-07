import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import spacy
import json
from functools import partial
import re

df = pd.read_csv('.\_lab-5\survey.csv')

folder = 'Лоскутов Андрей Викторович\\_lab-5\\'
folderPlots = 'plots\\'
dfName = 'result.csv'
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

df.to_csv(folder+dfName, mode='a', index= False, encoding='utf-8')

print('Saved')

def Statistic():
    df = pd.read_csv(folder+dfName).drop(columns=['Timestamp', 'comments'])
    seek = df[~df['treatment'].isnull() & df['treatment'] == 1]
    dont = df[~df['treatment'].isnull() & df['treatment'] == 0]

    print(df.info())
    print('ВСЕ')
    print(df.describe(include='all'))

    print('БОЛЬНЫЕ')
    print(seek.describe())
    print(seek.value_counts(dropna=False, normalize=True))
    print(seek.var(ddof=1))

    print('ЗДОРОВЫЕ')
    print(dont.describe())
    print(dont.value_counts(dropna=False, normalize=True))
    print(dont.var(ddof=1))

    print('ОБЩАЯ СТАТИСТИКА')
    ft_names= dont.columns.tolist()

    for column in ft_names:
        if column == 'Country' or column == 'state':
            print(str(df[column].value_counts(dropna=False, normalize=True)))
            continue
        avg =  ', avg: '+ str(df['Age'].sum()/df['Age'].value_counts(dropna=False).sum()) if column == 'Age' else ''

        expectedValue =str(sum(df[column].value_counts(dropna=False)*df[column].value_counts(dropna=False, normalize=True)))


        print(str(df[column].value_counts(dropna=False, normalize=True)) + f', dispersion: {df[column].var()}, expected value: {expectedValue}'+avg)

def Correlation(task):
    df = pd.read_csv(folder+dfName)
    df = df.drop(columns=['Country', 'state', 'comments', 'Timestamp'])
    corrmap = df.corr(numeric_only = True)
    cols = corrmap.nlargest(10, 'treatment')['treatment'].index
    corrTreatment = np.corrcoef(corrmap[cols].values, rowvar=False)

    def CorrPlt():
        plt.figure(figsize=(12,8) , dpi=100)
        sns.heatmap(corrmap, vmax=.8, square=True)
        plt.savefig(folder+folderPlots+'2 corr.png')
        plt.show()

    def TreatmentPlt():
        plt.figure(figsize=(12,8) , dpi=100)
        sns.heatmap(corrTreatment, annot=True, vmax=.8, square=True, annot_kws={'size':9}, yticklabels=cols.values, xticklabels=cols.values)
        plt.savefig(folder+folderPlots+'2 treatment.png')
        plt.show()

    def PlotGraphs():
        for i in cols.tolist():
            if i == 'treatment': continue
            dfNew= pd.DataFrame({'seek': pd.Series(df[~df['treatment'].isnull() & df['treatment'] == 1].groupby(i).size()), 'dont': pd.Series(df[~df['treatment'].isnull() & df['treatment'] == 0].groupby(i).size())})
            ax = dfNew.plot(kind='bar', stacked= True , color=['lightcoral', 'lightblue'], mark_right = True)
            for p in ax.patches:
                ax.annotate(str(p.get_height()), (p.get_x() * 1.001, p.get_y() + 5))
            plt.savefig(folder+folderPlots+'3 ' + i+'.png')
            plt.show()

    if (task == 2):
        CorrPlt()
        TreatmentPlt()
    elif (task == 3):
        PlotGraphs()

def Probability():
    df = pd.read_csv(folder+dfName)
    df = df.drop(columns=['Country', 'state', 'comments', 'Timestamp'])
    dfSeek = df[~df['treatment'].isnull() & df['treatment'] == 1]
    corrmap = df.corr(numeric_only = True)
    cols = corrmap.nlargest(10, 'treatment')['treatment'].index

    def СalcP(name):
        P=[]
        tot = []
        maxim = int(df[name].max())+1
        p = list((df.groupby(name).size() / len(df)).tolist())
        pSeek = list((dfSeek.groupby(name).size() / len(dfSeek)).tolist())

        for i in range(0, maxim):
             tot.append(p[i]*pSeek[i])
        for i in range(0, maxim):
            P.append(pSeek[i]/sum(pSeek))
            print(f'При ответе {i}: {round(P[i]*100.0, 2)}%')
        return(P, pSeek)

    print('Выделенные поля: ', cols.tolist()[1:10])
    print('ВЕРОЯТНОСТЬ, что при данном ответе на вопрос человеку будет нужна психологическая помощь')
    prob = {}
    maxPSeek = []
    totPSeek = []
    indexPSeek = []
    for name in cols.tolist()[1:10]:
        print(f'Вопрос: {name}')
        prob[name] = СalcP(name)
        index = prob.get(name)[0].index(max(prob.get(name)[0]))
        indexPSeek.append(f'{name}: {index}')
        maxPSeek.append(prob.get(name)[1][index])
        totPSeek.append(sum(prob.get(name)[1]))
        print()
    
    print(json.dumps(prob, indent=4, sort_keys=False))
    print(f'\nВЕРОЯТНОСТЬ, что при данных ответах на вопросы\n{indexPSeek}\nчеловеку будет нужна психологическая помощь: {sum(maxPSeek)/sum(totPSeek)},\nотносительно других вариантов ответа на эти вопросы')

def WhatToDo():
    return input('0 - переписать newsurvey\n1 - провести статистический анализ данных\n2 - выделить ключевые признаки наличия заболевания\n3 - построить графики для ключевых признаков\n4 - проверка гипотезы с помощью теоремы Байеса\n  Ваш выбор: ')

def RewriteCsv():
    df = pd.read_csv(folder+'survey.csv')
    nlp = spacy.load('en_core_web_sm') # для оценки схожести слов (в Gender)

whatToDo = WhatToDo()
if whatToDo == '0':
    RewriteCsv()
elif whatToDo == '1':
    Statistic()
elif whatToDo == '2':
    Correlation(2)
elif whatToDo == '3':
    Correlation(3)
elif whatToDo == '4':
    Probability()

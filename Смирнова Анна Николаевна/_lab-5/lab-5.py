from functools import partial
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import spacy
import json
import re

# https://www.kaggle.com/datasets/osmi/mental-health-in-tech-survey

folder = 'Смирнова Анна Николаевна\\_lab-5\\'
folderPlots = 'plots\\'
dfName = 'newsurvey.csv'

def WhatToDo():
    return input('0 - переписать newsurvey\n1 - провести статистический анализ данных\n2 - выделить ключевые признаки наличия заболевания\n3 - построить графики для ключевых признаков\n4 - проверка гипотезы с помощью теоремы Байеса\n  Ваш выбор: ')

def RewriteCsv():
    df = pd.read_csv(folder+'survey.csv')
    nlp = spacy.load('en_core_web_sm') # для оценки схожести слов (в Gender)

    def ValueToInt(x, dict, name): # оцифровывание по словарю
        if x in dict:
            df.loc[df[name] == x, name] = dict[x]
            
    def ValueToIntYesNo(x, name): # оцифровывания по да/нет
        if x != 0 and x!=1:
            df.loc[df[name] == x, name] = 0 if (x=='No') else (1 if (x=='Yes') else np.NaN)

    def Age():
        df['Age'].mask((df['Age'] > 100) | (df['Age'] < 15), inplace=True)

    def Gender():
        def GenderToInt(row):
            females = ['female', 'women', 'f', 'fem', 'girl']
            males = ['male', 'man', 'm', 'mail', 'guy']
            for i in range(0,len(females)):
                rowChange = re.sub('[^a-zа-я ]', '', str(row).lower().replace('/',' ')).replace('cis','').split()
                if rowChange:
                    if rowChange[0] == 'trans': df['Gender'].mask(df['Gender']==row, 2, inplace=True)
                    elif nlp(rowChange[0]).similarity(nlp(females[i]))>0.7: df['Gender'].mask(df['Gender']==row, 0, inplace=True)
                    elif nlp(rowChange[0]).similarity(nlp(males[i]))>0.5: df['Gender'].mask(df['Gender']==row, 1, inplace=True)
                    else: df['Gender'].mask(df['Gender']==row, 2, inplace=True)
        pd.Series(map(GenderToInt, df['Gender']), df['Gender'])

    def Leave():
        name='leave'
        dict={'Very easy': 0,'Somewhat easy': 1, 'Don\'t know': 2,'Somewhat difficult': 3,'Very difficult': 4}  
        mapfunc = partial(ValueToInt, dict=dict, name=name)
        pd.Series(map(mapfunc, df[name]), df[name])

    def No_employees():
        name='no_employees'
        dict={'1-5': 0,'6-25': 1, '26-100': 2,'100-500': 3, '500-1000': 4,'More than 1000': 5}
        mapfunc = partial(ValueToInt, dict=dict, name=name)
        pd.Series(map(mapfunc, df[name]), df[name])

    def Work_interfere():
        name='work_interfere'
        dict={'Never': 0,'Rarely': 1, 'Sometimes': 2,'Often': 3}  
        mapfunc = partial(ValueToInt, dict=dict, name=name)
        pd.Series(map(mapfunc, df[name]), df[name])

    def YesNo():
        dfNamesYesNo = ['self_employed','family_history', 'treatment', 'remote_work', 'tech_company', 'benefits', 'care_options', 'wellness_program', 'seek_help', 'anonymity', 'mental_health_consequence', 'phys_health_consequence', 'coworkers', 'supervisor', 'mental_health_interview', 'phys_health_interview', 'mental_vs_physical', 'obs_consequence']
        for name in dfNamesYesNo:
            mapfunc = partial(ValueToIntYesNo, name=name)
            pd.Series(map(mapfunc, df[name]))

    def CallFuncs():
        Age()
        Gender()
        Leave()
        No_employees()
        Work_interfere()
        YesNo()

    CallFuncs()
    print(df)

    df.to_csv(folder+dfName, mode='a', index= False, encoding='utf-8')

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

    

'''
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
'''
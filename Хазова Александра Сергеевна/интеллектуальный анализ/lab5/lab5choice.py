import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import statistics

df = pd.read_csv(r'..\2022-BigData\Хазова Александра Сергеевна\интеллектуальный анализ\lab5\newsurvey.csv')

df = df.drop('Timestamp', axis=1)

def statistic():
    ft_names = df.columns.tolist()
    print(ft_names)
    print(df.describe())

    df1 = pd.DataFrame()
    print("Доля каждого варианта для всех столбцов")
    for i in ft_names:
        print(df.groupby(i).size() / len(df))
        part = pd.DataFrame(df.groupby(i).size() / len(df), columns=[i])
        df1 = pd.concat([df1, part])
        
    #df1.to_csv("info.csv", mode='a', index= True, encoding='utf-8')

    del ft_names[1:4]
    del ft_names[21]

    print("Стандартное отклонение для всех столбцов")
    for i in ft_names:
        print(i)
        print(df[i].std())

    m = pd.DataFrame()
    print("Дисперсия и мат.ожидание")
    for i in ft_names:
        print(i)
        print(df[i].var()) #дисперсия
        print(df[i].mean()) #мат. ожидание
        m[i] = pd.Series(df[i].mean())
    print(m)

    print("Выделение потенциально ключевых признаков:")
    name_major = []
    for i in ft_names:
        #print(df1[i].idxmax()) #надо элемент у которого наибольшая доля
        #print(m[i].max()) 
        dfmajor = str(np.where(df1[i].idxmax() > m[i].max(), i, np.NaN))
        if dfmajor != "nan":
            name_major.append(dfmajor)
        #df1 = df1.where(df1[i] > m[i].max())
    print(name_major) #'treatment', 'work_interfere', 'tech_company', 'benefits', 'coworkers', 'phys_health_interview'

#diagrams

def diagrams():
    #доля каждого варианта в значимых признаках
    plt.figure(figsize=(12,6) , dpi=100)
    dfdiag = pd.DataFrame({'treatment' : pd.Series(df.groupby('treatment').size() / len(df)),
                        'work_interfere': pd.Series(df.groupby('work_interfere').size() / len(df)),
                        'tech_company' : pd.Series(df.groupby('tech_company').size() / len(df)),
                        'benefits' : pd.Series(df.groupby('benefits').size() / len(df)),
                        'coworkers' : pd.Series(df.groupby('coworkers').size() / len(df)),
                        'phys_health_interview' : pd.Series(df.groupby('phys_health_interview').size() / len(df))})
    print(dfdiag)
    sns.heatmap(dfdiag, annot=True)
    plt.xticks(rotation=90)
    plt.title ('Визуализация долей каждого варианта значимых столбцов',
            color = '#29452b',
            weight = 'semibold',
            fontsize = 16,
            alpha = 0.6)
    #plt.savefig("all.png")
    plt.show()

    corr = df.corr()
    mask = np.zeros_like(corr, dtype=np.bool)
    mask[np.triu_indices_from(mask)] = True
    f, ax = plt.subplots(figsize=(15, 15))
    sns.heatmap(corr, mask=mask, cmap='Purples', vmax=.3, center=0,
                square=True, cbar_kws={"shrink": .5}, annot = True, fmt=".3f", annot_kws={"size":6})
    #plt.savefig(r'..\2022-BigData\Хазова Александра Сергеевна\интеллектуальный анализ\lab5\corr.png')
    plt.show()

    plt.grid()
    #print(dfdiagtreat, dfdiagtreat.index)
    for i in dfdiag.columns.tolist():
        plt.grid()
        dfmajor = pd.DataFrame({i : pd.Series(df.groupby(i).size())})
        plots = sns.barplot(x=list(dfmajor.index), y=dfmajor[i], data=dfmajor, width=0.43, palette="plasma") #Purples, magma, nipy_spectral, vlag, twilight_shifted
        plt.xlabel("Varible", size=15)
        plt.ylabel("Iteration", size=15)
        for bar in plots.patches:
            plt.annotate(format(int(bar.get_height()), '.2f'),
                            (bar.get_x() + bar.get_width() / 2,
                            bar.get_height()), ha='center', va='center',
                            size=10, xytext=(0, 5),
                            textcoords='offset points')
        plots.set_title('Количество и вариация элементов в столбцe ' + i)
        #plt.savefig(i+'.png')
        plt.show()
        

def probability():
    print("Вероятность")
    #treatment - обращались ли за лечением? 
    p_treatment = df.groupby('treatment').size() / len(df)
    p_treatment_no = p_treatment.iloc[0] #вероятность что не обращались
    p_treatment_yes = p_treatment.iloc[1] #верояность что обращались
    p_treatment_NaN = 1-p_treatment_no-p_treatment_yes #нет ответа
    p1 = (p_treatment_yes*(p_treatment_yes+p_treatment_no/p_treatment_yes*p_treatment_no))/(p_treatment_no+p_treatment_yes+p_treatment_NaN) #вероятность обращения
    #print(p_treatment_no, p_treatment_yes, p_treatment_NaN)
    print(str(p1)+' - вероятность обращения за лечением(через вероятности)')
    p_treatment = df.groupby('treatment').size()
    p_no = p_treatment.iloc[0] #вероятность что не обращались
    p_yes = p_treatment.iloc[1] #верояность что обращались
    p = ((p_no)+((p_yes+p_no)/(p_yes*p_no)))/(len(df)) #yes
    print(str(p)+' - вероятность что НЕ будут обращаться за лечением(через количества)')
    #work_interfere - мешают ли психические проблемы в работе?
    p_work = df.groupby('work_interfere').size() / len(df)
    p_work_often = p_work.iloc[0] #часто
    p_work_rarely = p_work.iloc[1] #редко
    p_work_never = p_work.iloc[2] #никогда
    p_work_sometimes = p_work.iloc[3] #иногда
    p_work_NaN = p_work.iloc[4] #нет ответа
    p2 = ((p_work_rarely+p_work_never+p_work_sometimes)*(((p_work_rarely*p_work_never*p_work_sometimes*p_work_often)*(p_work_rarely+p_work_never+p_work_sometimes))/p_work_often))/(p_work_often) #часто псих.проблемы мешают в работе
    p3 = ((p_work_often+p_work_never+p_work_sometimes)*(((p_work_often*p_work_never*p_work_sometimes*p_work_rarely)*(p_work_often+p_work_never+p_work_sometimes))/p_work_rarely))/(p_work_rarely) #редко псих.проблемы мешают в работе
    p4 = ((p_work_rarely+p_work_often+p_work_sometimes)*(((p_work_rarely*p_work_never*p_work_sometimes*p_work_often)*(p_work_rarely+p_work_never+p_work_sometimes))/p_work_never))/(p_work_never) #никогда псих.проблемы мешают в работе
    p5 = ((p_work_rarely+p_work_never+p_work_often)*(((p_work_rarely*p_work_never*p_work_sometimes*p_work_often)*(p_work_rarely+p_work_never+p_work_often))/p_work_sometimes))/(p_work_sometimes) #иногда псих.проблемы мешают в работе
    #print(p_work_often, p_work_sometimes, p_work_rarely, p_work_never, p_work_NaN)
    print(str(p2)+" - вероятность что ЧАСТО психические проблемы мешают в работе")
    print(str(p3)+" - вероятность что РЕДКО психические проблемы мешают в работе")
    print(str(p4)+" - вероятность что НИКОГДА психические проблемы мешают в работе")
    print(str(p5)+" - вероятность что ИНОГДА психические проблемы мешают в работе")
    #coworkers - хотели бы обсудить проблему псих.здоровья с коллегами?
    p_coworkers = df.groupby('coworkers').size() / len(df)
    p_coworkers_no = p_coworkers.iloc[0] #нет
    p_coworkers_yes = p_coworkers.iloc[1] #да
    p_coworkers_NaN = 1-p_coworkers_no-p_coworkers_yes #нет ответа
    p5 = (p_coworkers_yes*((p_coworkers_yes+p_coworkers_no)/p_coworkers_yes*p_coworkers_no))/(p_coworkers_no+p_coworkers_yes+p_coworkers_NaN) #вероятность что хотел обсудить псих.проблемы с коллегами
    #print(p_coworkers_no, p_coworkers_yes, p_coworkers_NaN)
    print(str(p5)+" - вероятность того что человек хотел бы обсудить свое психическое здоровье с коллегами")
    
#statistic()
#diagrams()
probability()

#gen_m_bw20_30 = (gen_m+bw20_30)/(gen_m*bw20_30)
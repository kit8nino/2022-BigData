import pandas as pd
import numpy as np
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
    #print(df[column].value_counts(dropna=False))

#print(df.leave.unique())

# df.Age - убрать все, что не входит в диапазон от 15 до 100 лет
d0 = pd.Series(map(lambda x: np.NaN if ((x < 15)or(x > 100)) else int(x), df.Age), dtype=pd.Int64Dtype())
#print(d0)

# df.Gender - почистить на 3 категории: М, Ж и все остальное
d1 = pd.Series(map(lambda x: "М" if ((x == "M")or(x == "Male")or(x=="m")or(x=="male")or(x == "Mal")or(x == "Male ")or(x=="Man")) else x, df.Gender))
d2 = pd.Series(map(lambda x: "W" if ((x=="female")or(x=="F")or(x=="Woman")or(x=="f")or(x=="woman")or(x=="Female ")) else "other", d1))
#print(d2)

# df.work_interfere - перевести в значения от 0 до 3
d3 = pd.Series(map(lambda x: 0 if (x == "Often") else 1 if (x=="Rarely") else 2 if (x=="Never") else 3 if (x=="Sometimes") else 4, df.work_interfere))
#print(d3)

# df.no_employees - перевести в значения от 0 до 5:
           # ['6-25', 'More than 1000', '26-100', '100-500', '1-5', '500-1000']
d4 = pd.Series(map(lambda x: 0 if (x == "6-25") else 1 if (x=="More than 1000") else 2 if (x=="26-100") else 3 if (x=="100-500") else 4 if (x=="1-5") else 5, df.no_employees))
#print(d4)

# изменение столбца leave ['Somewhat easy' "Don't know" 'Somewhat difficult' 'Very difficult' 'Very easy']
d22 = pd.Series(map(lambda x: 0 if (x=="Somewhat easy") else 1 if (x=="Don't know") else 2 if (x=="Somewhat difficult") else 3 if (x=="Very difficult") else 4 if (x=="Very easy") else 5, df.leave))

# features = df.drop('treatment', 1)
# labels = df['treatment']

# изменение столбцов с ответом да, нет, не знаю
func = lambda x: int(0) if (x=="No") else int(1) if (x=="Yes") else np.NaN
d5 = pd.Series(map(func, df.family_history), dtype=pd.Int64Dtype())
d6 = pd.Series(map(func, df.treatment), dtype=pd.Int64Dtype())
d7 = pd.Series(map(func, df.remote_work), dtype=pd.Int64Dtype())
d8 = pd.Series(map(func, df.tech_company), dtype=pd.Int64Dtype())
d9 = pd.Series(map(func, df.benefits), dtype=pd.Int64Dtype())
d10 = pd.Series(map(func, df.care_options), dtype=pd.Int64Dtype())
d11 = pd.Series(map(func, df.wellness_program), dtype=pd.Int64Dtype())
d12 = pd.Series(map(func, df.seek_help), dtype=pd.Int64Dtype())
d13 = pd.Series(map(func, df.anonymity), dtype=pd.Int64Dtype())
d14 = pd.Series(map(func, df.mental_health_consequence), dtype=pd.Int64Dtype())
d15 = pd.Series(map(func, df.phys_health_consequence), dtype=pd.Int64Dtype())
d16 = pd.Series(map(func, df.coworkers), dtype=pd.Int64Dtype())
d17 = pd.Series(map(func, df.supervisor), dtype=pd.Int64Dtype())
d18 = pd.Series(map(func, df.mental_health_interview), dtype=pd.Int64Dtype())
d19 = pd.Series(map(func, df.phys_health_interview), dtype=pd.Int64Dtype())
d20 = pd.Series(map(func, df.mental_vs_physical), dtype=pd.Int64Dtype())
d21 = pd.Series(map(func, df.obs_consequence), dtype=pd.Int64Dtype())

#print(d14)

df1 = pd.DataFrame({ft_names[0] : df.Timestamp, 
        ft_names[1] : d0, 
        ft_names[2] : d2, 
        ft_names[3] : df.Country, 
        ft_names[4] : df.state, 
        ft_names[5] : df.self_employed, 
        ft_names[6] : d5, 
        ft_names[7] : d6, 
        ft_names[8] : d3, 
        ft_names[9] : d4, 
        ft_names[10] : d7, 
        ft_names[11] : d8, 
        ft_names[12] : d9, 
        ft_names[13] : d10,
        ft_names[14] : d11, 
        ft_names[15] : d12, 
        ft_names[16] : d13, 
        ft_names[16] : d22, 
        ft_names[17] : d14, 
        ft_names[18] : d15, 
        ft_names[19] : d16, 
        ft_names[20] : d17, 
        ft_names[21] : d18, 
        ft_names[22] : d19, 
        ft_names[23] : d20, 
        ft_names[24] : d21, 
        ft_names[25] : df.comments})

#print(df1)

df1.to_csv("newsurvey.csv", mode='a', index= False, encoding='utf-8')

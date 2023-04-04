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


def Bayes():
    return False


ft_names = df.columns.tolist()
for column in ft_names:
    print(column)
    print(df[column].value_counts(dropna=False))


num_emp = 1000
age_le20 = 250
age_bw31_45 = 400
age_bw20_30 = 300
age_gt45 = 50

gen_m = 500
gen_f = 400
gen_x = 100

com_le500 = 700
com_gt500 = 300

# условно решим, что когда вероятность > .5, то все так и есть
p_m_a30_le500 = gen_m / num_emp * age_bw20_30 / num_emp * com_le500 / num_emp
norm_c = (gen_m + age_bw20_30 + com_le500 - gen_m_bw20_30
          - age_bw20_30_com_le500 - com_le500_gen_m
          - age_bw20_30_gen_m_com_le500) / num_emp

# df.Age - убрать все, что не входит в диапазон от 15 до 100 лет

# df.Gender - почистить на 3 категории: М, Ж и все остальное

# df.work_interfere - перевести в значения от 0 до 3

# df.no_employees - перевести в значения от 0 до 5:
           # ['6-25', 'More than 1000', '26-100', '100-500', '1-5', '500-1000']

# features = df.drop('treatment', 1)
# labels = df['treatment']

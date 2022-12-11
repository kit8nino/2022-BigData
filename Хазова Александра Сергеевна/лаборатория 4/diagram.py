import pandas as pd
import matplotlib.pyplot as plt

data = []
data1 = []
w = lambda x: (x.replace('.','').replace('"', "").replace("?", "").replace(")", "").replace("(", "").replace(":", "").replace("!", "").replace("»", "").replace("«", ""))

df = pd.read_csv("res.csv", converters={'0':w})
df1 = df.sort_values(by=['0'], ascending=False)
s = df['0'].loc[df.index[0]]

plt.text(0, 350,"Самое распространненое слово: " + s)

plt.grid()
#data = list(df1['0'])
#data1 = list(df1['1'])

words = list(filter(lambda x:x>=50, df1['1']))
k = df.loc[lambda df: df['1'] >= 50, "0"]

plt.title("Повторение слов в файле(>=50)")
plt.xlabel("Слова")
plt.ylabel("Количество повторений")
plt.tick_params(axis='x', rotation=90)

#plt.plot(data1)
plt.plot(k , words, 'm')
#plt.pie(words)
#plt.plot(data, data1)
plt.show()

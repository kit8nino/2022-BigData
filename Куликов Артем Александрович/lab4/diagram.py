import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statistics

w = lambda x: (x.replace('.','').replace('"', "").replace("?", "").replace(")", "").replace("(", "").replace(":", "").replace("!", "").replace("»", "").replace("«", ""))

df = pd.read_csv("result.csv", converters={'0':w})
df1 = df.sort_values(by=["0"], ascending=False)
s = df["0"].loc[df.index[0]]

plt.text(0, 355,"Самое распространненое слово: " + s)

plt.grid()

words = list(filter(lambda x:x>=100, df1['1']))
k = df1.loc[lambda df: df['1'] >= 100, "0"]

plt.title("Повторение слов в файле(>=100)")
plt.xlabel("Слова")
plt.ylabel("Количество повторений")
plt.tick_params(axis='x', rotation=90)
plt.plot(k , words, 'm')
plt.show()

print("Среднее количество повторений слова: ")
print(statistics.mean(list(df["1"])))

print("Медианное количество повторений слова: ")
print(statistics.median(list(df["1"])))

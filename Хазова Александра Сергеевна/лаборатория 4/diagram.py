import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import statistics

w = lambda x: (x.replace('.','').replace('"', "").replace("?", "").replace(")", "").replace("(", "").replace(":", "").replace("!", "").replace("»", "").replace("«", ""))

df = pd.read_csv("res.csv", converters={'0':w})
df1 = df.sort_values(by=["0"], ascending=False)
s = df["0"].loc[df.index[0]]

plt.text(0, 350,"Самое распространненое слово: " + s)

plt.grid()

words = list(filter(lambda x:x>=50, df1['1']))
k = df1.loc[lambda df1: df1['1'] >= 50, "0"]

plt.title("Повторение слов в файле(>=50)")
plt.xlabel("Слова")
plt.ylabel("Количество повторений")
plt.tick_params(axis='x', rotation=90)

#plt.plot(data1)
plt.plot(k, words, 'm')
#plt.pie(words)
#plt.plot(data, data1)
plt.show()

words05 = list(filter(lambda x:x>=100, df1['1']))
k05 = df1.loc[lambda df1: df1['1'] >= 100, "0"]
df2 = pd.DataFrame()
df2["words"] = [float(i) for i in words05]
df2["labels"] = k05

plt.grid()
plt.pie(df2["words"], labels=words05)
plt.legend(loc = 'center right', bbox_to_anchor=(0, 0.5), labels = df2["labels"])
plt.show()

data = df["0"]
data = data.str.len()
freq = list(df["1"])

print("Среднее количество повторений слова: ")
print(statistics.mean(list(df["1"])))

print("Медианное количество повторений слова: ")
print(statistics.median(list(df["1"])))

print("Корреляция длин слов и количества повторений слова: ")
df3 = pd.DataFrame()
df3["len"] = data
df3["freq"] = pd.Series(freq)
print(df3.corr())

df4 = pd.DataFrame()
df4 = pd.read_csv("books.csv", converters={'0':w})

plt.grid()
plt.title("Взаимосвязь длин слов и количества повторений слова:")
plt.bar(df3["len"], df3["freq"], color='m')
plt.show()

print("Дисперсия длин слов и количества их повторений: ")
print(df3.var())

print("Ковариация длин названий и года издания: ")
print(df3.cov())

plt.grid()
plt.title("Взаимосвязь длин слов и логарифмического количества повторений слова:")
plt.bar(df3["len"], np.log(df3["freq"]))
plt.show()

plt.grid()
plt.title("Взаимосвязь длин слов и количества повторений слова:")
plt.scatter(df3["len"], df3["freq"], c='purple') 
plt.show()

plt.grid()
plt.title("Взаимосвязь логарифмических длин слов и логарифмического количества повторений слова:")
plt.scatter(np.log(df3["len"]), np.log(df3["freq"])) 
plt.show()

plt.grid()
plt.title("Взаимосвязь длин названий и год издания:")
names_len = list(df4["books_name"].str.len())
plt.scatter(df4["year"], names_len) 
plt.tick_params(axis='x', rotation=90)
plt.show()

df5 = pd.DataFrame()
df5["names_len"] = names_len
#min = np.min(df4["year"])
#print(min)
#n = df4["year"].apply(lambda x: 2030 if x == "No data" else x)
df5["year"] = df4["year"]
index = df5[df5["year"] == 'No data'].index
df5.drop(index, inplace=True)
index1 = df5[df5["year"] == '101'].index
df5.drop(index1, inplace=True)
index1 = df5[df5["year"] == 'year'].index
df5.drop(index1, inplace=True)
index1 = df5[df5["year"] == '22010'].index
df5.drop(index1, inplace=True)
index1 = df5[df5["year"] == '19821982'].index
df5.drop(index1, inplace=True)
index1 = df5[df5["year"] == '19984'].index
df5.drop(index1, inplace=True)
print(df5)

plt.grid()
plt.title("Взаимосвязь длин названий и года издания(без мусора):")
plt.scatter(df5["year"], df5["names_len"], c='purple')
plt.tick_params(axis='x', rotation=90)
plt.show()

df5["year"] = pd.to_numeric(df5["year"])
print(df5.dtypes)

print("Ковариация длин названий и года издания: ")
print(df5.cov())

print("Корреляция длин названий и года издания: ")
print(df5.corr())

sns.pairplot(df3)
plt.show()
sns.jointplot(df3)
plt.show()
sns.heatmap(df3.corr())
plt.show()
sns.pairplot(df5)
plt.show()
sns.jointplot(df5)
plt.show()
sns.heatmap(df5.corr())
plt.show()

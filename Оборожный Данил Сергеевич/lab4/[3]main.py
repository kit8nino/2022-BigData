import pandas as pd
import matplotlib.pyplot as plt
import statistics

def clean_string(x):
    return x.replace('.','').replace('"', "").replace("?", "").replace(")", "").replace("(", "").replace(":", "").replace("!", "").replace("»", "").replace("«", "")

dataFrame = pd.read_csv("result.csv", converters={'0':clean_string}, encoding="windows-1251")
#Пропускаем топ 1 т.к. это предлоги и т.п.
labels = list(dataFrame["Word"].loc[1:16])
values = list(map(int, dataFrame["Count"].loc[1:16]))

print(f"Pretext/TOP1: {dataFrame['Word'].loc[0]} - {dataFrame['Count'].loc[0]}")

print(f"Most common word/TOP2: {labels[0]} - {values[0]}")

plt.grid()
plt.title("Top 15")
plt.pie(values, labels=labels)
plt.show()

data = dataFrame["Word"].str.len()
freq = list(dataFrame["Count"])

print("Average number of repetitions of the top word: ")
print(statistics.mean(list(dataFrame["Count"])))

print("Median value of repetitions of the top word: ")
print(statistics.median(list(dataFrame["Count"])))

print("Correlation between word lengths and number of repetitions of the word: ")
dataFrame2 = pd.DataFrame()
dataFrame2["length"] = data
dataFrame2["frequency"] = pd.Series(freq)
print(dataFrame2.corr())

dataFrame3 = pd.read_csv("data3.csv", converters={'0':clean_string}, encoding="windows-1251")
dataFrame3 = dataFrame3.sort_values(by=["year"], ascending=True)

print("Variance of word lengths and their repetition: ")
print(dataFrame2.var())

print("Covariance of book titles lengths and publication year: ")
print(dataFrame2.cov())

plt.grid()
plt.title("Relationship between word lengths and number of repetitions:")
plt.scatter(dataFrame2["length"], dataFrame2["frequency"], c='purple')
plt.ylim(0, 130)
plt.show()

plt.grid()
plt.title("Relationship between book titles lengths and publication year:")
names_len = list(dataFrame3["books_name"].str.len())
plt.scatter(dataFrame3["year"], names_len)
plt.tick_params(axis='x', rotation=90)
plt.show()

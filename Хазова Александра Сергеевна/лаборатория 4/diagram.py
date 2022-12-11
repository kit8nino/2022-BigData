import pandas as pd
import matplotlib.pyplot as plt

data = []
data1 = []
#for l in open(r'C:\Users\Сергей\Documents\parsing\res.csv', 'r', encoding="utf8").readlines()[1:]:
    #d = str(l.split(',')[0])
    #d = d.replace('"', '')
    #d = d.replace(".", "")
    #d = d.replace("?", "")
    #d = d.replace(")", "")
    #d = d.replace("(", "")
    #d = d.replace(":", "")
    #d = d.replace("!", "")
    #d = d.replace("»", "")
    #d = d.replace("«", "")
    #d = d.replace("\\n","")
    #data.append(d)

df = pd.read_csv("res.csv")
df1 = df.sort_values(by=['0'], ascending=False)
s = df['0'].loc[df.index[0]]
plt.text(0, 350,"Самое распространненое слово: " + s)
plt.grid()
data = list(df1['0'])
data1 = list(df1['1'])
plt.title("Повторение слов в файле")
plt.xlabel("Слова")
plt.plot(data1)
#plt.pie(data1)
#plt.plot(data, data1)
plt.show()
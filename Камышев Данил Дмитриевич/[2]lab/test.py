from functools import reduce

f_data = []
s_data = []
for l in open('flavors_of_cacao.csv').readlines()[1:]:
    f_data.append(l.split(',')[5])
for l in open('flavors_of_cacao_2.csv').readlines()[1:]:
    s_data.append(l.split(',')[5])
f_data += s_data
data = list(map(lambda x: (x, 1), f_data))
data.sort()
i = 0
d = {}
f_data.sort()
while i < len(f_data):
    d[f_data[i]] = data.count(data[i])
    i += data.count(data[i])
print(d)

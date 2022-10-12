import csv

files = ("flavors_of_cacao.csv", "flavors_of_cacao_2.csv")

def topCountry():
    d = {}
    for file in files:
        with open('2022-BigData/_lab-2/' + file, 'r') as File:
            reader = [row[5] for row in csv.reader(File)][1:]
        data = list(map(lambda x: (x), reader))
        data.sort()
        i = 0
        while i < len(data):
            if data[i] in d:
                d[data[i]] += data.count(data[i])
            else:
                d[data[i]] = data.count(data[i])
            i += data.count(data[i])
    return str(sorted(d.items(), key=lambda i: i[1], reverse=True)).replace('),', ')\n')

print(topCountry())
import pandas as pd

if __name__ == '__main__':
    data = pd.read_csv('./_lab-2/flavors_of_cacao.csv').sort_values(by=['Broad Bean Origin'])
    count = data.pivot_table(columns=['Broad Bean Origin'], aggfunc='size')
    print(count)

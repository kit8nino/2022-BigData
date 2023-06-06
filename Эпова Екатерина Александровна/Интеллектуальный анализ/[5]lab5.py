import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import seaborn

df = pd.read_csv('survey1.csv')


def data_corrector():
    df = pd.read_csv('survey.csv')

    df['Age'] = pd.Series(map(lambda x: np.NaN if ((x < 15) or (x > 100))
                              else int(x), df.Age), dtype=pd.Int64Dtype())

    gender = df['Gender'].to_list()
    gender_males = set(filter(lambda x: x.startswith('m') or x.startswith('M'),
                              gender))
    gender_females = set(filter(lambda x: (x.startswith('f')
                                           or x.startswith('F')
                                           or x.startswith('w')
                                           or x.startswith('W')), gender))
    gender_others = set(filter(lambda x: not (x.startswith('f')
                                              or x.startswith('F')
                                              or x.startswith('w')
                                              or x.startswith('W')
                                              or x.startswith('m')
                                              or x.startswith('M')), gender))

    df.loc[df['Gender'].isin(gender_males), 'Gender'] = 0
    df.loc[df['Gender'].isin(gender_females), 'Gender'] = 1
    df.loc[df['Gender'].isin(gender_others), 'Gender'] = 2


    df['work_interfere'] = df['work_interfere'].map({'Never': int(0),
                                                     'Sometimes': int(1),
                                                     'Rarely': int(2),
                                                     'Often':  int(3)})

    df['no_employees'] = df['no_employees'].map({'6-25': 1,
                                                 'More than 1000': 5,
                                                 '26-100': 2, '100-500': 3,
                                                 '1-5': 0, '500-1000': 4})


    names_cols = df.columns.to_list()[10:-1]
    names_cols += 'family_history', 'treatment', 'self_employed'
    print(names_cols)
    print(set(df['leave'].to_list()))
    for name_col in names_cols:
        list_nan = ['Not sure', 'Maybe', 'Some of them']
        list_zero = ['No', 'Somewhat easy']
        list_one = ['Yes', "Don't know"]
        list_two = ['Somewhat difficult']
        list_three = ['Very difficult']
        list_four = ['Very easy']

        df.loc[df[name_col].isin(list_zero),
               name_col] = int(0)
        df.loc[df[name_col].isin(list_one),
               name_col] = int(1)
        df.loc[df[name_col].isin(list_two),
               name_col] = int(2)
        df.loc[df[name_col].isin(list_three),
               name_col] = int(3)
        df.loc[df[name_col].isin(list_four),
               name_col] = int(4)
        df.loc[df[name_col].isin(list_nan),
               name_col] = np.NaN

    df.to_csv(r'survey1.csv', sep=',')


def statistic_analyze():
    mean_for_columns = pd.DataFrame()
    share_of_options_for_columns = pd.DataFrame()
    for col in df.columns.values[2:-1]:
        if col in ('Country', 'state'):
            continue
        res = df.groupby(col).size() / len(df)
        part = pd.DataFrame(res, columns=[col])
        variance = np.var(df[col])
        mean = df[col].mean()
        print(res)
        print("Дисперсия:", variance)
        print("Среднее: {:.2f}".format(mean)+'\n')
        mean_for_columns[col] = pd.Series(mean)
        share_of_options_for_columns = pd.concat([share_of_options_for_columns,
                                                  part])
    key_features = []

    for col in df.columns.values[2:-1]:
        if col in ('Country', 'state'):
            continue
        dfmajor = str(
               np.where(
                    share_of_options_for_columns[col].idxmax() >
                    mean_for_columns[col].max(),
                    col,
                    np.NaN,
                    )
               )
        if dfmajor != "nan":
            key_features.append(dfmajor)

    print(key_features)
    return key_features


def create_diagrams():
    plt.figure(figsize=(12, 15))
    key_features = statistic_analyze()
    data_frame_diagram = pd.DataFrame(
        {
            field: pd.Series(df.groupby(field).size() / len(df))
            for field in key_features
        }
    )
    print(data_frame_diagram)
    seaborn.heatmap(data_frame_diagram, annot=True)
    plt.xticks(rotation=90)
    plt.title('Визуализация долей каждого варианта значимых столбцов',
              color='#29452b',
              weight='semibold',
              fontsize=16,
              alpha=0.6)
    plt.savefig("key_features.png")
    plt.show()

    plt.grid()
    for column in data_frame_diagram.columns.tolist():
        plt.grid()
        field_data_frame = pd.DataFrame(
            {column: pd.Series(df.groupby(column).size())}
        )
        plots = seaborn.barplot(
            x=list(field_data_frame.index),
            y=field_data_frame[column],
            data=field_data_frame,
            width=0.43,
            palette="plasma",
        )
        plt.xlabel("Variable", size=15)
        plt.ylabel("Iteration", size=15)
        for bar in plots.patches:
            plt.annotate(
                format(int(bar.get_height()), ".2f"),
                (bar.get_x() + bar.get_width() / 2, bar.get_height()),
                ha="center",
                va="center",
                size=10,
                xytext=(0, 5),
                textcoords="offset points",
            )
        plots.set_title(f"Количество и вариация элементов в столбцe {column}")
        plt.savefig(f"{column}.png")
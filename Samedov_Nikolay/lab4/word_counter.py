import json
import string

import numpy as np
import pymorphy2
from collections import Counter

import matplotlib.pyplot as plt
import pathlib


translation = str.maketrans("", "", string.punctuation + "–«»")


def get_books_data() -> list[dict[str, str]]:
    return json.loads(pathlib.Path("books_data.json").read_text(encoding="utf-8"))


def get_top_words(count: int = 20, with_year: bool = False):
    books_data = get_books_data()
    all_words = []
    analyzer = pymorphy2.MorphAnalyzer()
    for book_data in books_data:
        year = book_data["publication_year"]
        words = book_data["title"].translate(translation).split()
        for word in words:
            if len(word) < 2:
                continue
            if with_year and year is None:
                continue
            pos = analyzer.parse(word)[0].tag.POS
            if pos in ("INTJ", "PRCL", "CONJ", "PREP"):
                continue
            all_words.append(word.lower())

    words_counter = Counter(all_words)
    return words_counter.most_common(count)


def show_top(count: int = 20):
    top_words = get_top_words(count)
    _, axes = plt.subplots()

    words = [top_word[0] for top_word in top_words]
    counts = [top_word[1] for top_word in top_words]

    axes.barh(words, counts)
    axes.invert_yaxis()
    axes.set_title("Количество слов в названии книг за все время")
    plt.tight_layout()
    plt.show()


def show_popularity_by_year(count: int = 10):
    _, axes = plt.subplots()
    top_words = [top_word[0] for top_word in get_top_words(count=count, with_year=True)]
    words_popularity = {}
    books_data = get_books_data()
    for book_data in books_data:
        year = book_data["publication_year"]
        if year is None:
            continue
        words = book_data["title"].translate(translation).split()
        for word in words:
            word = word.lower()
            if word not in top_words:
                continue
            if word not in words_popularity:
                words_popularity[word] = {}
            if year not in words_popularity[word]:
                words_popularity[word][year] = 0
            words_popularity[word][year] += 1

    result = []
    for word, word_data in words_popularity.items():
        result.append((word, sorted(list(word_data.keys())), list(word_data.values())))

    for word_result in result:
        word, years, counts = word_result
        axes.plot(years, counts, label=word)
    axes.set_xlim(1930, 2020)
    axes.set_xlabel("Годы")
    axes.set_ylabel("Количество выпущенных книг")
    axes.grid(True)
    plt.legend(loc='center left', bbox_to_anchor=(1.1, 0.5))

    plt.tight_layout()
    plt.show()


def show_book_count():
    fig, axes = plt.subplots()
    books_data = get_books_data()
    data = {}
    for book_data in books_data:
        year = book_data["publication_year"]
        if year is None:
            continue
        year = int(year)
        if year > 2023:
            continue
        if year not in data:
            data[year] = 0
        data[year] += 1

    years = list(data.keys())
    counts = list(data.values())

    axes.bar(years, counts)
    axes.set_xlim(1900, 2020)

    axes.set_ylabel('Количество')
    axes.set_title('Количество выпускаемых книг по годам')

    plt.show()


def show_book_year_word_count():
    fig, axes = plt.subplots()
    fig.set_size_inches(10, 4.8)
    books_data = get_books_data()
    years = {}
    data = []
    for book_data in books_data:
        year = book_data["publication_year"]
        if year is None:
            continue
        year = int(year)
        if year > 2023:
            continue
        if year not in years:
            years[year] = year - 0.5
        years[year] += 0.5
        data.append((len(book_data["title"]), years[year]))
    data.sort(key=lambda book_: book_[-1])

    axes.plot([b_data[-1] for b_data in data], [b_data[0] for b_data in data])
    axes.set_xlim(1900, 2020)

    axes.set_ylabel('Количество')
    axes.set_title('Количество слов в названии книги по годам')

    plt.show()


if __name__ == "__main__":
    show_top(20)
    show_popularity_by_year(20)
    show_book_count()
    show_book_year_word_count()


"""
show_top(20) -> топ популярных слов. логично лидирует слово энциклопедия
и советская, тк там на каждую букву по книге))
show_popularity_by_year(20) -> популярные слова по годам. хотелось на примере слова советский
увидеть статистику падения после 1991, но очень много книг оказалось без указания даты выпуска
и получилась каша. мне кажется это самая адекватная статистика которую можно нарисовать, и 
на реально больших данных можно будет найти кучу закономерностей, связанных с историческим этапом
show_book_count() -> количество выпускаемых книг по годам
show_book_year_word_count() -> количество слов в названии относительно года xddd
"""
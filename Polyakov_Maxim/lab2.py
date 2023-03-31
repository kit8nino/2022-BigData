import csv


def sposob_1(countries: list[str]) -> dict:
    return {val: countries.count(val) for val in sorted(set(countries))}


def sposob_2(countries: list[str]) -> dict:
    from collections import Counter

    return dict(Counter(countries))


if __name__ == "__main__":
    with open("data.csv", "r", encoding="utf-8", newline="") as file:
        part1 = [row[5] for row in csv.reader(file)][1:]
    with open("data1.csv", "r", encoding="utf-8", newline="") as file:
        part2 = [row[5] for row in csv.reader(file)]
    _countries = part1 + part2
    _countries.sort()
    data1 = sposob_1(countries=_countries)
    print(f"{data1=}")
    data2 = sposob_2(countries=_countries)
    print(f"{data2=}")

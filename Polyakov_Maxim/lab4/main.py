import csv
from dataclasses import dataclass, field
import os
from numpy import median
import matplotlib.pyplot as plt

INPUT_FILES_PATH = "files"


@dataclass
class Employer:
    name: str
    link: str = ""
    img_link: str = ""


@dataclass
class Vacancy:
    area_title: str
    title: str
    link: str
    employer: Employer
    respond_link: str = ""
    salary: int = 0


def read_file(file_name: str) -> list[tuple[str]]:
    with open(file_name, "r", encoding="utf-8", newline="") as file:
        return list(csv.reader(file))[1:]


class Currencies:
    RUB = "RUB"
    USD = "USD"
    EUR = "EUR"


EXCHANGE_RATES = {
    "RUB": 1,
    "USD": 72.5,
    "EUR": 77.3,
}


def count_salary_for_currency(clear_str: str,
                              currency: str = Currencies.RUB) -> int:
    clear_str = clear_str.replace(currency, "")
    if "–" in clear_str:
        items = map(int, clear_str.split("–"))
        return sum(item * EXCHANGE_RATES[currency] for item in items) // 2
    return int(clear_str) * EXCHANGE_RATES[currency]


def get_salary_from_str(salary_str: str | None) -> int | None:
    if not salary_str:
        return
    clear_str = (
        salary_str.replace("от", "")
        .replace(" ", "")
        .replace("руб.", "")
        .replace("\'", "")
        .replace("до", "")
        .strip()
    )
    if Currencies.USD in clear_str:
        return count_salary_for_currency(
            clear_str=clear_str,
            currency=Currencies.USD
        )
    if Currencies.EUR in clear_str:
        return count_salary_for_currency(
            clear_str=clear_str,
            currency=Currencies.EUR
        )
    return count_salary_for_currency(clear_str=clear_str)


def get_vacancy_from_csv(csv_row: tuple[str]) -> Vacancy:
    employer = Employer(
        name=csv_row[3],
        link=csv_row[4],
        img_link=csv_row[5]
    )
    return Vacancy(
        area_title=csv_row[0],
        title=csv_row[1],
        link=csv_row[2],
        employer=employer,
        respond_link=csv_row[6],
        salary=get_salary_from_str(csv_row[7])
    )


def get_vacancies_from_files() -> list[Vacancy]:
    vacancies = []
    for file in os.listdir(INPUT_FILES_PATH):
        vacancies.extend(
            get_vacancy_from_csv(row) for row in read_file(f"{INPUT_FILES_PATH}/{file}")
        )
    return vacancies


@dataclass
class AreaInfo:
    area_title: str
    max_salary: int = 0
    min_salary: int = 0
    average_salary = 0
    vacancies_count: int = 0
    _salaries: list[int] = field(default_factory=list)

    def add_salary(self, salary: int):
        if not salary:
            return
        self._salaries.append(salary)

    def inc_vacancy_counter(self):
        self.vacancies_count += 1

    def count_average_salary(self):
        self.average_salary = int(median(self._salaries))
        print(f"{self.area_title} total vacs = {len(self._salaries)}")
        return self.average_salary

    def count_min_salary(self):
        self.min_salary = int(min(self._salaries))
        return self.min_salary

    def count_max_salary(self):
        self.max_salary = int(max(self._salaries))
        return self.max_salary


def parse_data(vacancies: list[Vacancy]):
    areas = {}
    for vacancy in vacancies:
        if vacancy.area_title not in areas:
            areas[vacancy.area_title] = AreaInfo(
                area_title=vacancy.area_title
            )
        areas[vacancy.area_title].inc_vacancy_counter()
        areas[vacancy.area_title].add_salary(vacancy.salary)
    for area in areas:
        areas[area].count_max_salary()
        areas[area].count_min_salary()
        areas[area].count_average_salary()
    return areas


def _show_data(x: list, y: list, title: str, reverse: bool = True):
    _, axes = plt.subplots()
    axes.barh(x, y)
    if reverse:
        axes.invert_yaxis()
    axes.set_title(title)
    plt.tight_layout()
    plt.show()


def show_min_salaries(data):
    area_titles = [item.area_title for item in data.values()]
    min_salaries = [item.min_salary for item in data.values()]
    _show_data(x=area_titles,
               y=min_salaries,
               title="Минимальная зп в регионах")


def show_max_salaries(data):
    area_titles = [item.area_title for item in data.values()]
    max_salaries = [f"{item.max_salary // 1000}к"for item in data.values()]
    print(max_salaries)
    _show_data(x=area_titles,
               y=max_salaries,
               title="Максимальная зп в регионах")


def show_avg_salaries(data):
    area_titles = [item.area_title for item in data.values()]
    avg_salaries = [item.average_salary for item in data.values()]
    _show_data(x=area_titles,
               y=avg_salaries,
               title="Средняя зп в регионах")


def show_total_vac_count(data):
    area_titles = [item.area_title for item in data.values()]
    vac_count = [item.vacancies_count for item in data.values()]
    _show_data(
        x=area_titles,
        y=vac_count,
        title="Всего вакансий в регионах"
    )

def main():
    vacancies = get_vacancies_from_files()
    data = parse_data(vacancies)
    show_min_salaries(data)
    show_max_salaries(data)
    show_avg_salaries(data)
    show_total_vac_count(data)


if __name__ == "__main__":
    main()

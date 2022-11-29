from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from structs import Employer, Vacancy
import concurrent.futures
import csv


CHROMEDRIVER_PATH = "chromedriver107.exe"
WINDOW_SIZE = "1920,1080"

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)


def get_page_source(link: str, page: int = 0) -> str:
    driver = webdriver.Chrome(
        chrome_options=chrome_options, executable_path=CHROMEDRIVER_PATH
    )
    link = f"{link}&page={page}"
    driver.get(link)
    html = driver.page_source
    driver.close()
    return html


def get_last_page(html: str) -> int | None:
    soup = BeautifulSoup(html, "html.parser")
    try:
        pages = soup.find("div", class_="pager", attrs={"data-qa": "pager-block"})
        last_page = (
            pages.find_all("span", class_="pager-item-not-in-short-range")[-1]
        ).find("a", class_="bloko-button", attrs={"data-qa": "pager-page"})
    except AttributeError:
        return
    return int(last_page.get_text())


def concat_links(url: str, base_url: str = "https://nn.hh.ru"):
    return base_url + url


def get_page_vacancies(link: str, page: int, file_name: str) -> list:
    source = get_page_source(link, page)
    vacancies = parse_vacancies(source)
    with open(file_name, "a", encoding="utf-8", newline="") as file:
        for vacancy in vacancies:
            writer = csv.writer(file)
            writer.writerow(vacancy.get_csv_row())
    print(f"Page {page} completed with {len(vacancies)} items")
    return vacancies


def parse_vacancies(html: str) -> list:
    soup = BeautifulSoup(html, "html.parser")
    vacancies_container = soup.find("div", attrs={"data-qa": "vacancy-serp__results"})
    items = vacancies_container.find_all("div", class_="serp-item")
    vacancies = []
    for item in items:
        title_item = item.find(
            "a", class_="serp-item__title", attrs={"data-qa": "serp-item__title"}
        )
        title_text = title_item.get_text()
        vacancy_link = title_item.get("href").split("?")[0]
        company_item = (item.find("div", class_="vacancy-serp-item-company")).find(
            "a", attrs={"data-qa": "vacancy-serp__vacancy-employer"}
        )
        if company_item is None:
            employer_link = None
            employer_name = None
        else:
            employer_link = concat_links(company_item.get("href").split("?")[0])
            employer_name = company_item.get_text().replace("\u202f", " ")
        employer_logo_item = item.find(
            "a", attrs={"data-qa": "vacancy-serp__vacancy-employer-logo"}
        )

        employer_img = (
            employer_logo_item.find("img", class_="vacancy-serp-item-logo").get("src")
            if employer_logo_item
            else None
        )
        salary_item = item.find(
            "span", attrs={"data-qa": "vacancy-serp__vacancy-compensation"}
        )

        salary = salary_item.get_text().replace("\u202f", " ") if salary_item else None
        respond_link_item = item.find("div", class_="vacancy-serp-actions").find(
            "a", attrs={"data-qa": "vacancy-serp__vacancy_response"}
        )
        respond_link = (
            concat_links(respond_link_item.get("href")) if respond_link_item else None
        )
        employer = Employer(
            name=employer_name, link=employer_link, img_link=employer_img
        )
        vacancy = Vacancy(
            title=title_text,
            link=vacancy_link,
            employer=employer,
            respond_link=respond_link,
            salary=salary,
        )
        vacancies.append(vacancy)
    return vacancies


def main():
    link = "https://nn.hh.ru/search/vacancy?area=66&items_on_page=100"
    last_page = get_last_page(get_page_source(link, page=0)) or 1
    result_file_name = "result.csv"
    with open(result_file_name, "w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(
            (
                "title",
                "'link'",
                "'employer_name'",
                "'employer_link'",
                "'employer_img'",
                "'respond_link'",
                "'salary'",
            )
        )

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        res = [
            executor.submit(get_page_vacancies, link, page, result_file_name)
            for page in range(last_page)
        ]
        concurrent.futures.wait(res)


if __name__ == "__main__":
    main()

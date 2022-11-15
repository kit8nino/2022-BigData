import datetime
import json
import pathlib
from typing import Optional

import requests
import tqdm
from bs4 import BeautifulSoup, Tag


class Book:
    def __init__(self, title: str, publication_year: Optional[int]):
        self.title = title
        self.publication_year = publication_year

    def to_dict(self) -> dict:
        return {"title": self.title, "publication_year": self.publication_year}

    def __repr__(self) -> str:
        return f"Book({self.title=}, {self.publication_year=})"


def parse_book(book_link: str):
    title_field = "Название:"
    publication_year_field = "Год издания:"

    html = requests.get(f"http:{book_link}").text
    soup = BeautifulSoup(html, "html.parser")
    content = soup.find("td", attrs={"style": "padding-left: 8px"})
    fields = content.find_all("td")

    title = None
    publication_year = None
    for field in fields:
        field = field.text.strip().replace("\n", "").replace("\t", "")
        if field.startswith(title_field):
            title = field.lstrip(title_field)
        elif field.startswith(publication_year_field):
            publication_year = field.lstrip(publication_year_field)
            if publication_year.isdigit():
                publication_year = int(publication_year)
            else:
                publication_year = None
    return Book(title=title, publication_year=publication_year)


def parse_page(data_link: str):
    html = requests.get(f"http:{data_link}").text
    soup = BeautifulSoup(html, "html.parser")
    content = soup.find("div", class_="content")
    books: list[Tag] = list(
        filter(lambda link: "book" in link.get("href"), content.find_all("a"))
    )

    return [parse_book(book.get("href")) for book in tqdm.tqdm(books)]


def parse_by_topic(
    topic: str, save_path: str = "books_data.json", page_limit: Optional[int] = None
):
    url = "http://royallib.com"
    genres_html = requests.get(f"{url}/genres.html").text
    soup = BeautifulSoup(genres_html, "html.parser")
    main_div = soup.find("div", attrs={"style": "width:100%"})
    links: list[Tag] = main_div.find_all("a")
    topic_link = list(
        filter(
            lambda link_data: link_data[0].lower().strip() == topic.lower().strip(),
            [(link.text, link.get("href")) for link in links],
        )
    )
    if not topic_link:
        raise ValueError("Такой темы нет")
    _, topic_url = topic_link[0]  # //royallib.com/genre/spravochnaya_literatura/
    topic_html = requests.get(f"http:{topic_url}").text
    soup = BeautifulSoup(topic_html, "html.parser")
    data_links = [
        link.get("href") for link in soup.find("div", class_="well").find_all("a")
    ]
    # RU: А	Б В Г Д Е Ж З И Й К Л М Н О П Р С Т У Ф Х Ц Ч Ш Щ Э Ю Я итд
    if page_limit is not None:
        data_links = data_links[:page_limit]

    pages_data = []
    for i, data_link in enumerate(data_links):
        print(f"page {i + 1}/{len(data_links)}")
        pages_data.extend(parse_page(data_link))

    json_data = json.dumps([book.to_dict() for book in pages_data], ensure_ascii=False)
    pathlib.Path(save_path).write_text(json_data, encoding="utf-8")
    print("final.")


def main():
    topics = {
        1: "Любовные романы",
        2: "Религия и духовность",
        3: "Справочная литература",
        4: "Детское",
        5: "Наука, Образование",
    }

    variant = (
        len("Самедов Николай Юсифович")
        * (
            datetime.date(year=2003, month=2, day=27)
            - datetime.date(year=1997, month=11, day=27)
        ).days
        % 5
    ) + 1

    parse_by_topic(topics[variant])


if __name__ == "__main__":
    main()

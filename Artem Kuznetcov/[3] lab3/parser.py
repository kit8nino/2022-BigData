
import datetime
import json
import asyncio
import pathlib
import time
from typing import Optional

import aiohttp
from bs4 import BeautifulSoup, Tag


class Book:
    def __init__(self, title: str, publication_year: Optional[int]):
        self.title = title
        self.publication_year = publication_year

    def to_dict(self) -> dict:
        return {"title": self.title, "publication_year": self.publication_year}

    def __repr__(self) -> str:
        return f"Book({self.title=}, {self.publication_year=})"


async def parse_book(session: aiohttp.ClientSession, book_link: str) -> Optional[Book]:
    title_field = "Название:"
    publication_year_field = "Год издания:"

    html = await ((await session.get(f"http:{book_link}")).text())
    soup = BeautifulSoup(html, "html.parser")
    content = soup.find("td", attrs={"style": "padding-left: 8px"})
    if content is None:
        return
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


async def parse_page(
    session: aiohttp.ClientSession, data_link: str
) -> list[Optional[Book]]:
    html = await (await session.get(f"http:{data_link}")).text()
    soup = BeautifulSoup(html, "html.parser")
    content = soup.find("div", class_="content")
    books: list[Tag] = list(
        filter(lambda link: "book" in link.get("href"), content.find_all("a"))
    )
    result = [*await asyncio.gather(
        *[parse_book(session, book.get("href")) for book in books]
    )]
    print(f"parsed page {data_link}. count - {len(result)}")
    return result


def get_topic_links(main_div: Tag, topic: str) -> list[str]:
    for div in main_div.find_all("div"):  # type: Tag
        title = div.find("b").text
        if title.lower().strip() != topic.lower().strip():
            continue
        return [link.get("href") for link in div.find_all("a")]
    return []


async def parse_subtopic(
    session: aiohttp.ClientSession, topic_url: str
) -> list[Optional[Book]]:
    topic_html = await (await session.get(f"http:{topic_url}")).text()
    soup = BeautifulSoup(topic_html, "html.parser")

    pages = soup.find("div", class_="well")
    if pages is not None:
        data_links = [
            link.get("href") for link in soup.find("div", class_="well").find_all("a")
        ]

        pages_data = await asyncio.gather(
            *[parse_page(session, data_link) for data_link in data_links]
        )
        pages_data = [data for sub_list in pages_data for data in sub_list]
    else:
        pages_data = await parse_page(session, topic_url)

    print(f"parsed topic {topic_url}. count - {len(pages_data)}")
    return pages_data


async def parse_by_topic(topic: str, save_path: str = "booksData.json"):
    start = time.time()
    url = "http://royallib.com"
    session = aiohttp.ClientSession()
    genres_html = await (await session.get(f"{url}/genres.html")).text()
    soup = BeautifulSoup(genres_html, "html.parser")
    main_div = soup.find("div", attrs={"style": "width:100%"})

    subtopics_links = get_topic_links(
        main_div, topic
    )
    if not subtopics_links:
        raise ValueError("Такой темы нет")

    result_data = await asyncio.gather(
        *[parse_subtopic(session, subtopic) for subtopic in subtopics_links]
    )
    result_data = [data for sub_list in result_data for data in sub_list]

    json_data = json.dumps(
        [book.to_dict() for book in result_data if book is not None], ensure_ascii=False
    )
    pathlib.Path(save_path).write_text(json_data, encoding="utf-8")
    await session.close()
    print(f"final. {time.time() - start}. count - {len(result_data)}")


async def main():
    topics = {
        1: "Любовные романы",
        2: "Религия и духовность",
        3: "Справочная литература",
        4: "Детское",
        5: "Наука, Образование",
    }

    variant = (
        len("Кузнецов Артём Андрианович")
        * (
            datetime.date(year=2002, month=2, day=21)
            - datetime.date(year=1997, month=11, day=27)
        ).days
        % 5
    ) + 1

    await parse_by_topic(topics[variant])


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())

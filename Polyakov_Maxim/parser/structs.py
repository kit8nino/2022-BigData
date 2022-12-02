from dataclasses import dataclass


@dataclass
class Employer:
    name: str
    link: str | None = None
    img_link: str | None = None


@dataclass
class Vacancy:
    title: str
    link: str
    employer: Employer
    respond_link: str | None = None
    salary: str | None = None

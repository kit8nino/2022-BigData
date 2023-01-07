from dataclasses import dataclass


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
    salary: str = ""

    def get_csv_row(self):
        return (
            self.area_title,
            self.title,
            self.link,
            self.employer.name,
            self.employer.link,
            self.employer.img_link,
            self.respond_link,
            self.salary,
        )

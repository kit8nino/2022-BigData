from dataclasses import dataclass


@dataclass
class Employer:
    name: str
    link: str = ""
    img_link: str = ""


@dataclass
class Vacancy:
    title: str
    link: str
    employer: Employer
    respond_link: str = ""
    salary: str = ""

    def get_csv_row(self):
        return (
            self.title,
            f"'{self.link}'",
            f"'{self.employer.name}'",
            f"'{self.employer.link}'",
            f"'{self.employer.img_link}'",
            f"'{self.respond_link}'",
            f"'{self.salary}'",
        )

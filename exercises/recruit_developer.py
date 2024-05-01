# recruit_developer.py
from dataclasses import dataclass
from typing import List
import click

@dataclass
class Applicant:
    name: str
    programming_languages: List[str]
    years_of_experience: int
    has_degree: bool
    email_address: str

def schedule_interview(applicant: Applicant):
    print(f"Scheduled interview with {applicant.name}")

@click.command()
def main():
    applicants: List[Applicant] = [
        Applicant(
            name="Devon Smith",
            programming_languages=["c++", "ada"],
            years_of_experience=1,
            has_degree=False,
            email_address="devon@email.com",
        ),
        Applicant(
            name="Susan Jones",
            programming_languages=["python", "javascript"],
            years_of_experience=2,
            has_degree=False,
            email_address="susan@email.com",
        ),
        Applicant(
            name="Sam Hughes",
            programming_languages=["java"],
            years_of_experience=4,
            has_degree=True,
            email_address="sam@email.com",
        ),
    ]

    for applicant in applicants:
        knows_python = "python" in applicant.programming_languages
        experienced_dev = applicant.years_of_experience >= 5
        meets_criteria = (
            knows_python
            or experienced_dev
            or applicant.has_degree
        )

        if meets_criteria:
            schedule_interview(applicant)

if __name__ == "__main__":
    main()

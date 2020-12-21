import datetime

import selenium
import selenium.webdriver
import selenium.common.exceptions
from typing import Sequence, Set
import person
from batch import BatchInfo

BROWSER = selenium.webdriver.Firefox
PINNACLE_URL = "https://outcomes4health.org/o4h/"


class RecentlyVaccinated(Exception):
    def __init__(self, date):
        self.date = date
        self.message = f"Already vaccinated on {date:%m-%d-%Y}"
        super().__init__(self.message)


class Uploader:
    def __init__(self):
        self.browser = BROWSER()
        self.browser.get(PINNACLE_URL)

    def is_logged_in(self):
        pass

    def check_vaccinator(self, vaccinator: str) -> bool:
        return False

    def check_vaccinators(self, vaccinators: Sequence[str]) -> Set[str]:
        return {v for v in vaccinators if not self.check_vaccinator(v)}

    def upload_person(self, p: person.Person):
        pass

    def upload_people(self, people: Sequence[person.Person], batch: BatchInfo):
        for p in people:
            try:
                self.upload_person(p)
                p.status = "uploaded"
            except selenium.common.exceptions.WebDriverException:
                p.status = "error"
                p.error_type = "Error occurred during Pinnacle upload"
            except RecentlyVaccinated as e:
                p.status = "error"
                p.error_type = e.message


class TestUploader(Uploader):
    valid_vaccinators = ["Underwood", "Cobley"]
    logged_in = False

    # noinspection PyMissingConstructor
    def __init__(self):
        pass

    def is_logged_in(self):
        return self.logged_in

    def check_vaccinator(self, vaccinator: str) -> bool:
        return vaccinator in self.valid_vaccinators

    def upload_person(self, p: person.Person):
        last_digit = str(p.nhs)[-1]
        if last_digit == "3":
            raise selenium.common.exceptions.WebDriverException("Bad upload")
        elif last_digit == "7":
            raise RecentlyVaccinated(datetime.date(2021, 1, 1))

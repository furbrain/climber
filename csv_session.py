import csv
import re
import subprocess

from bs4 import BeautifulSoup

import sessions
import dateutil.parser


class CSVSession(sessions.Session):
    def __init__(self, fname):
        super().__init__()
        self.load(fname)

    def load(self, fname):
        with open(fname, "r") as f:
            reader = csv.DictReader(f,['time', 'name', 'dob', 'nhs'])
            self.people = list(reader)
            self.people = self.people[1:]
        for person in self.people:
            person['dob'] = dateutil.parser.parse(person['dob'])
            person['nhs'] = str(person['nhs']).replace(" ", "")

        return self.people

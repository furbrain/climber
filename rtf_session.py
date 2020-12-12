import re
import subprocess

from bs4 import BeautifulSoup

import sessions
import dateutil.parser


class RTFSession(sessions.Session):
    DOB_REGEX = r"Date Of Birth: (\S+)"
    NHS_REGEX = r"NHS Number: ([0-9 ]{10,12})"

    def __init__(self, fname):
        super().__init__()
        self.load(fname)

    @staticmethod
    def find_regex(strings, regex):
        for s in strings:
            result = re.match(regex, s)
            if result:
                return result.group(1)
        return None

    def get_person(self, row):
        cells = [list(x.strings) for x in row.find_all("td")]
        if len(cells) < 4:
            return None
        time = cells[0][0]
        if time == "TIME":
            return None
        print(cells)
        # data = [x.strip() for x in cells[1]]
        data = ''.join(cells[1])
        data = data.splitlines()
        name = data[0]
        dob = self.find_regex(data, self.DOB_REGEX)
        dob = dateutil.parser.parse(dob)
        nhs = self.find_regex(data, self.NHS_REGEX)
        return {'name': name, 'dob': dob, 'nhs': nhs, 'time': time}

    def load(self, fname):
        with open(fname, "r") as f:
            rtf = f.read()
            html_text = subprocess.run(["unrtf", "--html"], input=rtf, capture_output=True, text=True).stdout
        print(html_text)
        doc = BeautifulSoup(html_text, 'html.parser')
        self.people = []
        for row in doc.find_all("tr"):
            person = self.get_person(row)
            if person is not None:
                self.people.append(person)
        return self.people

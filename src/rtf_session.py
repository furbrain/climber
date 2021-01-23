import re
import subprocess
from typing import List

import wx
from bs4 import BeautifulSoup

from .person import Person

DOB_REGEX = r"Date Of Birth: (\S+)"
NHS_REGEX = r"NHS Number: ([0-9 ]{10,12})"


def find_regex(strings, regex):
    for s in strings:
        result = re.match(regex, s)
        if result:
            return result.group(1)
    return None


def get_person(row):
    cells = [list(x.strings) for x in row.find_all("td")]
    if len(cells) < 3:
        return None
    time = cells[0][0]
    if time == "TIME":  # this is a header row - ignore
        return None
    data = ''.join(cells[1])
    if data == '':  # no name, a blank entry
        return None
    data = data.splitlines()
    name = data[0]
    name = re.sub(r"\(.*\)", "", name)
    if len(cells[2]) == 0:
        return None
    dob = cells[2][0]
    nhs = find_regex(data, NHS_REGEX)
    p = Person(time=time, name=name, dob=dob, nhs=nhs)
    return p


def load(fname: str) -> List[Person]:
    wx.LogStatus(f"Reading RTF file {fname}")
    with open(fname, "r") as f:
        rtf = f.read()
        # noinspection SpellCheckingInspection
        html_text = subprocess.run(["unrtf", "--html"], input=rtf, capture_output=True, text=True).stdout
    doc = BeautifulSoup(html_text, 'html.parser')
    people = [get_person(row) for row in doc.find_all("tr")]
    people = [p for p in people if p is not None]
    return people

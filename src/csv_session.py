import csv
from typing import Dict

import wx

from .person import Person, DEFAULT_HEADINGS

FIELDNAMES = {'starttime': 'time',
              'time': 'time',
              'nhsnumber': 'nhs',
              'nhs': 'nhs',
              'name': 'name',
              'dateofbirth': 'dob',
              'dob': 'dob',
              }


def clean_dict(dct: Dict[str, str]):
    """remove dict entries with None ie not relevant"""
    result = {}
    for key, value in dct.items():
        key = key.lower()
        if key in FIELDNAMES:
            result[FIELDNAMES[key]] = value
    return result


def load(fname):
    wx.LogStatus(f"Reading CSV file {fname}")
    with open(fname, "r") as f:
        reader = csv.DictReader(f)
        people = list(reader)
    people = people[1:]
    people = [Person(**clean_dict(p)) for p in people]
    return people


def save(fname, people):
    with open(fname, "w") as f:
        writer = csv.writer(f)
        writer.writerow(DEFAULT_HEADINGS)
        for p in people:
            writer.writerow(p.get_texts())

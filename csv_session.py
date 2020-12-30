import csv

import wx

from person import Person, DEFAULT_HEADINGS

FIELDNAMES = ('time', 'name', 'dob', 'nhs')


def clean_dict(dct):
    """remove dict entries with None ie not relevant"""
    keys = list(dct.keys())
    for key in keys:
        if key not in FIELDNAMES:
            del dct[key]
    return dct


def load(fname):
    wx.LogStatus(f"Reading CSV file {fname}")
    with open(fname, "r") as f:
        reader = csv.DictReader(f, FIELDNAMES)
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

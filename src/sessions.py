import sys
from typing import List

from . import rtf_session
from . import csv_session
from .person import Person


def load_people(fname: str) -> List[Person]:
    if fname.lower().endswith(".rtf"):
        return rtf_session.load(fname)
    if fname.lower().endswith(".csv"):
        return csv_session.load(fname)


if __name__ == "__main__":
    people = rtf_session.load(sys.argv[1])
    csv_session.save(sys.argv[2], people)

from typing import List

import rtf_session
import csv_session
from person import Person

def load_people(fname: str) -> List[Person]:
    if fname.lower().endswith(".rtf"):
        return rtf_session.load(fname)
    if fname.lower().endswith(".csv"):
        return csv_session.load(fname)


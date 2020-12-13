import numpy as np

from form import PDF



class Session:
    def __init__(self):
        self.people = []

    @staticmethod
    def fromFile(fname: str):
        from rtf_session import RTFSession
        from csv_session import CSVSession
        if fname.lower().endswith(".rtf"):
            return RTFSession(fname)
        if fname.lower().endswith(".csv"):
            return CSVSession(fname)

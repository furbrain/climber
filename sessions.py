import numpy as np

from form import PDF



class Session:
    def __init__(self):
        self.people = []

    @staticmethod
    def fromFile(fname: str):
        from rtf_session import RTFSession
        if fname.lower().endswith(".rtf"):
            return RTFSession(fname)

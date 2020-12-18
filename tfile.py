import os
import tempfile
from typing import List
import atexit


class TFile:
    """This class generates secure temporary filenames, which will be deleted on program exit"""
    filelist: List[str] = []

    @classmethod
    def get(cls, suffix=""):
        _, fname = tempfile.mkstemp(suffix=suffix)
        cls.filelist.append(fname)
        return fname

    @classmethod
    def delete_all(cls):
        for fname in cls.filelist:
            try:
                os.remove(fname)
            except IOError:
                pass


atexit.register(TFile.delete_all)

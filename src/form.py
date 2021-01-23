from itertools import groupby
from operator import attrgetter
from typing import List, Sequence

import numpy as np
from fpdf import FPDF

from . import person
from .tfile import TFile

NUM_ROWS_PER_PDF = 20
COLUMN_WIDTHS = [15, 55, 25, 30] + [8] * 7


class DataEntryPDF(FPDF):
    def __init__(self, vaccinators, people):
        super().__init__(orientation="P", unit="mm", format="A4")
        # add some decorations here...
        self.set_mono_font()
        self.vaccinators = [''] * 7
        self.set_vaccinators(vaccinators)
        self.add_people(people)

    def set_mono_font(self):
        self.set_font("Courier", "B", 10)

    def set_vaccinators(self, vaccinators):
        self.vaccinators = vaccinators[:7]
        if len(vaccinators) < 7:
            self.vaccinators += [''] * (7 - len(vaccinators))

    def new_page(self):
        self.add_page()
        self.set_top_margin(25)
        self.set_left_margin(15)
        self.set_fill_color(0)
        xs = [10, self.w - 10 - 8]
        ys = [10, self.h - 10 - 8]
        for x in xs:
            for y in ys:
                self.ellipse(x, y, 8, 8, style="F")
        self.set_xy((self.w / 2 - 50), 10)
        self.set_font("Times", "B", 16)
        self.set_fill_color(255)
        self.cell(100, 8, "Covid19 Vaccinations", align="C")
        self.set_mono_font()
        self.set_xy(self.l_margin, self.t_margin)
        columns = ['Time', 'Name', 'DoB', 'NHS#'] + self.vaccinators
        self.add_line(columns)

    def add_line(self, contents=None) -> List[List[int]]:
        if contents is None:
            contents = [''] * 11
        widths = COLUMN_WIDTHS
        bounds = []
        y = self.get_y()
        for w, c in zip(widths, contents):
            x = self.get_x()
            self.cell(w, 8, c, border=1, fill=True)
            bounds.append([x, y, x + w, y + 8])
        self.ln(12)
        return bounds

    def add_person(self, p: person.Person):
        contents = p.get_texts() + [''] * 7
        self.add_line(contents)

    def add_people(self, people):
        self.new_page()
        person_count = 0
        for p in people:
            self.add_person(p)
            person_count += 1
            if person_count >= NUM_ROWS_PER_PDF:
                self.new_page()
                person_count = 0
        while person_count < NUM_ROWS_PER_PDF:
            self.add_line()
            person_count += 1

    def save(self, fname):
        self.output(fname, dest="F")

    @staticmethod
    def get_bounds():
        pdf = DataEntryPDF([], [])
        pdf.new_page()
        pdf.set_xy(pdf.l_margin, pdf.t_margin)
        # noinspection PyUnusedLocal
        bounds = [pdf.add_line() for i in range(NUM_ROWS_PER_PDF + 1)]
        bounds = np.array(bounds, dtype="float64")
        return bounds


class ErrorReportPDF(FPDF):
    LINE_SPACING = 9

    def __init__(self, people: Sequence[person.Person]):
        super().__init__(orientation="P", unit="mm", format="A4")
        self.set_font("Arial", "B", 10)
        # add some decorations here...
        self.add_page()
        self.set_top_margin(25)
        self.set_left_margin(15)
        self.set_xy(self.l_margin, self.t_margin)
        self.add_groups(people)

    def print_line(self, text, image=None):
        if not image:
            self.cell(w=0, h=5, txt=text, ln=1)
        else:
            fname = TFile.get(suffix=".png")
            with open(fname, "wb") as f:
                f.write(image)
            self.cell(w=self.w // 2 - self.l_margin, h=5, txt=text)
            self.image(fname, w=self.w // 2 - self.r_margin, h=5)
            self.ln()

    def print_group(self, reason, people: Sequence[person.Person]):
        self.set_font("Arial", "B", 12)
        self.print_line(reason)
        self.set_font("Arial", "", 10)
        for p in people:
            text = ' '.join(p.get_texts())
            self.print_line(text, p.image)

    def add_groups(self, people: Sequence[person.Person]):
        people = sorted(people, key=attrgetter("error_type"))
        for error_reason, p in groupby(people, key=attrgetter("error_type")):
            self.print_group(error_reason, p)

    def save(self, fname):
        self.output(fname, dest="F")


if __name__ == "__main__":
    data_entry_form = DataEntryPDF([], [])
    data_entry_form.save("blank.pdf")

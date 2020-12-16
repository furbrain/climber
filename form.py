import numpy as np
from fpdf import FPDF
from typing import List
import person

NUM_ROWS_PER_PDF = 20
COLUMN_WIDTHS = [15, 55, 25, 30] + [8] * 7


class PDF(FPDF):
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
        xs = [10, self.w - 10 - 8]
        ys = [10, self.h - 10 - 8]
        for x in xs:
            for y in ys:
                self.ellipse(x, y, 8, 8, style="F")
        self.set_xy((self.w / 2 - 50), 10)
        self.set_font("Times", "B", 16)
        self.cell(100, 8, "Covid19 Vaccinations", align="C")
        self.set_mono_font()
        self.set_top_margin(25)
        self.set_left_margin(15)
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
            self.cell(w, 8, c, border=1)
            bounds.append([x, y, x + w, y + 8])
        self.ln(12)
        return bounds

    def add_person(self, p: person.Person):
        contents = [
                       f"{p.time:%H:%M}",
                       p.name[:25],
                       f"{p.dob:%d-%m-%Y}",
                       f"{p.nhs:010}"
                   ] + [''] * 7
        self.add_line(contents)

    def add_people(self, people):
        self.new_page()
        person_count = 0
        for person in people:
            self.add_person(person)
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
        pdf = PDF([], [])
        pdf.new_page()
        pdf.set_xy(pdf.l_margin, pdf.t_margin)
        bounds = [pdf.add_line() for i in range(NUM_ROWS_PER_PDF + 1)]
        bounds = np.array(bounds, dtype="float64")
        return bounds

if __name__=="__main__":
    f = PDF([], [])
    f.save("blank.pdf")
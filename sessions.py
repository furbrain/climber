import subprocess
import re
import numpy as np
import dateutil.parser
from bs4 import BeautifulSoup
from fpdf import FPDF


DOB_REGEX = r"Date Of Birth: (\S+)"
NHS_REGEX = r"NHS Number: ([0-9 ]{10,12})"

NUM_ROWS_PER_PDF = 20
COLUMN_WIDTHS = [15, 55, 25, 30] + [8] * 7

class PDF(FPDF):
    def __init__(self):
        super().__init__(orientation="P", unit="mm", format="A4")
        #add some decorations here...
        self.set_mono_font()
        self.vaccinators = [''] * 7

    def set_mono_font(self):
        self.set_font("Courier", "B", 10)

    def set_vaccinators(self, vaccinators):
        self.vaccinators = vaccinators[:7]
        if len(vaccinators)<7:
            self.vaccinators += [''] * (7-len(vaccinators))

    def new_page(self):
        self.add_page()
        xs = [10, self.w-10-8]
        ys = [10, self.h-10-8]
        for x in xs:
            for y in ys:
                self.ellipse(x,y,8,8,style="F")
        self.set_xy((self.w/2-50), 10)
        self.set_font("Times","B",16)
        self.cell(100, 8, "Covid19 Vaccinations", align="C")
        self.set_mono_font()
        self.set_top_margin(25)
        self.set_left_margin(15)
        self.set_xy(self.l_margin, self.t_margin)
        columns = ['Time', 'Name', 'DoB', 'NHS#'] + self.vaccinators
        self.add_line(columns)

    def add_line(self, contents=None):
        if contents is None:
            contents = ['']*11
        widths = COLUMN_WIDTHS
        bounds = []
        y = self.get_y()
        for w, c in zip(widths, contents):
            x = self.get_x()
            self.cell(w,8,c,border=1)
            bounds.append([x,y,x+w,y+8])
        self.ln(12)
        return bounds

    def get_bounds(self):
        self.new_page()
        self.set_xy(self.l_margin, self.t_margin)
        bounds = [self.add_line() for i in range(NUM_ROWS_PER_PDF+1)]
        return bounds

    def add_person(self, person):
        contents = [
            person['time'],
            person['name'][:25],
            person['dob'].strftime("%d-%m-%Y"),
            person['nhs'] or ""
        ] + [''] * 7
        self.add_line(contents)

    def add_people(self, people):
        self.new_page()
        person_count=0
        for person in people:
            self.add_person(person)
            person_count += 1
            if person_count >= NUM_ROWS_PER_PDF:
                self.new_page()
                person_count=0
        while person_count < NUM_ROWS_PER_PDF:
            self.add_line()
            person_count += 1

def find_regex(strings, regex):
    for s in strings:
        result = re.match(regex, s)
        if result:
            return result.group(1)
    return None


def get_person(row):
    cells = [list(x.strings) for x in row.find_all("td")]
    if len(cells)<4:
        return None
    time = cells[0][0]
    if time=="TIME":
        return None
    print(cells)
    #data = [x.strip() for x in cells[1]]
    data = ''.join(cells[1])
    data = data.splitlines()
    name = data[0]
    dob = find_regex(data, DOB_REGEX)
    dob = dateutil.parser.parse(dob)
    nhs = find_regex(data, NHS_REGEX)
    return {'name':name, 'dob': dob, 'nhs': nhs, 'time': time}

def get_people(fname):
    with open(fname, "r") as f:
        rtf = f.read()
        html_text = subprocess.run(["unrtf", "--html"], input=rtf, capture_output=True, text=True).stdout
    print(html_text)
    doc = BeautifulSoup(html_text, 'html.parser')
    people = []
    for row in doc.find_all("tr"):
        person = get_person(row)
        if person is not None:
            people.append(person)
    return people

def make_pdf(vaccinators, people, fname):
    pdf = PDF()
    print (people)
    pdf.set_vaccinators(vaccinators)
    pdf.add_people(people)
    pdf.output(fname, dest="F")

def get_bounds():
    pdf = PDF()
    bounds = np.array(pdf.get_bounds(), dtype="float64")
    return bounds

if __name__ == "__main__":
    pdf = PDF()
    bounds = np.array(pdf.get_bounds())
    print(bounds)
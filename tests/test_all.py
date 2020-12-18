import unittest
import webbrowser

import form
import ocr
import person
import sessions
from tfile import TFile

VACCINATORS = ["PU", "JC", "DB", "PJW", "SK"]


class MyTestCase(unittest.TestCase):
    def test_all(self):
        # load data
        register = person.Everyone()
        people = sessions.load_people("test_data1.csv")

        for p in people:
            register.append(p)

        name = TFile.get(".pdf")
        pdf = form.DataEntryPDF(VACCINATORS, register.filter(status="imported"))
        pdf.save(name)
        webbrowser.open(name)

        for page in ("completed-1.jpg", "completed-2.jpg"):
            updates = ocr.ocrreader.get_all_details(page, VACCINATORS)
            for p in updates:
                register.update(p)

        name = TFile.get(".pdf")
        pdf = form.ErrorReportPDF(register.filter(status="error"))
        pdf.save(name)
        webbrowser.open(name)


if __name__ == '__main__':
    unittest.main()

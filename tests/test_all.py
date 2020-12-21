import time
import unittest
import webbrowser

import form
from ocr import OCR
import person
import sessions
import upload
from tfile import TFile

VACCINATORS = ["PU", "JC", "DB", "PJW", "SK"]

MAIN_RESULTS = {
    "Too many boxes ticked": [9095410581, 5151943173, 3994464768, 1751230875],
    "Invalid box ticked": [2077450598, 2007447605, 1202362096],
    "No boxes ticked (DNA?)": [2616381722, 2858131467, 2242795231],
    "Error occurred during Pinnacle upload": [3396620143],
    "Already vaccinated on 01-01-2021": [5368278577],
}

class MyTestCase(unittest.TestCase):
    display = True

    def test_all(self):
        # load data
        register = person.Everyone()
        people = sessions.load_people("test_data1.csv")

        for p in people:
            register.append(p)

        pdf = form.DataEntryPDF(VACCINATORS, register.filter(status="imported"))
        if self.display:
            name = TFile.get(".pdf")
            pdf.save(name)
            webbrowser.open(name)

        for page in ("test_scan.jpg", "completed-2.jpg"):
            updates = OCR.process_form(page, VACCINATORS)
            for p in updates:
                register.update(p)

        uploader = upload.TestUploader()
        uploader.upload_people(register.filter(status="scanned"), None)
        errors_found = register.filter(status="error")
        pdf = form.ErrorReportPDF(errors_found)
        if self.display:
            name = TFile.get(".pdf")
            pdf.save(name)
            webbrowser.open(name)
        time.sleep(1)
        num_errors_expected = sum(len(x) for x in MAIN_RESULTS.values())
        print("expected errors: ", num_errors_expected)
        for error in errors_found:
            print(f"Checking {error}")
            self.assertIn(error.nhs, MAIN_RESULTS[error.error_type])
        self.assertEqual(len(errors_found), num_errors_expected)

    def test_check_vaccinators(self):
        combos = [
            (("Underwood", "Cobley"), True),
            (("Cobley", "Underwood"), True),
            (("Weeks", "Underwood"), False),
            (("Underwood",), True),
            (("Kaye", "Weeks"), False),
        ]
        uploader = upload.TestUploader()
        for vaccinators, result in combos:
            self.assertEqual(uploader.check_vaccinators(vaccinators), result)

if __name__ == '__main__':
    unittest.main()

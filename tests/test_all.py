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
    "Selenium error: Bad upload": [3396620143],
    "RecentlyVaccinated: Already vaccinated on 01-01-2021": [5368278577],
    "Invalid DOB read": [3105416501],
}


class MyTestCase(unittest.TestCase):
    display = False

    def run_all_tests(self, fname):
        # load data
        register = person.Everyone()
        people = sessions.load_people(fname)

        for p in people:
            register.append(p)

        pdf = form.DataEntryPDF(VACCINATORS, register.filter(status="imported"))
        if self.display:
            name = TFile.get(".pdf")
            pdf.save(name)
            webbrowser.open(name)

        for page in ("test_scan1.jpg", "test_scan2.jpg"):
            updates = OCR.process_form(page, VACCINATORS)
            for p in updates:
                register.update(p)

        uploader = upload.TestUploader()
        # noinspection PyTypeChecker
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
            (("Underwood", "Cobley"), set()),
            (("Cobley", "Underwood"), set()),
            (("Weeks", "Underwood"), {"Weeks"}),
            (("Underwood",), set()),
            (("Kaye", "Weeks"), {"Kaye", "Weeks"}),
        ]
        uploader = upload.TestUploader
        for vaccinators, result in combos:
            self.assertEqual(uploader.check_vaccinators(vaccinators), result)

    def test_old_csv(self):
        self.run_all_tests("test_data1.csv")

    def test_new_csv(self):
        self.run_all_tests("test_data2.csv")


if __name__ == '__main__':
    unittest.main()

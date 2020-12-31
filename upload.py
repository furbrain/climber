import datetime
import time
from typing import Sequence, Set, Optional

import selenium
from selenium.common.exceptions import WebDriverException
import selenium.webdriver
import selenium.webdriver.common
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
# noinspection PyPep8Naming
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import batch
import person
from batch import BatchInfo

import platform
import wx

if platform.system() == "Windows":
    import winreg

    edge_version_key = r"Software\Microsoft\Edge\BLBeacon"
    key1 = winreg.OpenKey(winreg.HKEY_CURRENT_USER, edge_version_key, 0, winreg.KEY_READ)
    edge_version = winreg.QueryValueEx(key1, "version")[0]
    BROWSER = lambda: selenium.webdriver.Edge(f"drivers/{edge_version}.exe")
else:
    BROWSER = selenium.webdriver.Firefox
PINNACLE_URL = "https://outcomes4health.org/o4h/"


class UploadException(Exception):
    pass


class RecentlyVaccinated(UploadException):
    def __init__(self, date):
        self.date = date
        self.message = f"Already vaccinated on {date:%m-%d-%Y}"
        super().__init__(self.message)


class ElementNotFound(UploadException):
    pass


class TooManyElementsFound(UploadException):
    pass


class VaccinationNotExpected(UploadException):
    pass


class NotLoggedIn(UploadException):
    pass


def as_date(dt):
    return f"{dt:%d-%b-%Y}"


class Uploader:
    instance = None

    def __init__(self):
        self.browser = BROWSER()
        self.browser.get(PINNACLE_URL)

    @classmethod
    def get_instance(cls):
        if cls.instance is None:
            cls.instance = cls()
            return cls.instance
        try:
            cls.instance.browser.title
        except selenium.common.exceptions.WebDriverException:
            # browser has been closed - restart
            cls.instance = cls()
        return cls.instance

    def get_unique_element_from_xpath(self,
                                      xpath: str,
                                      description: str,
                                      element: Optional[WebElement] = None) -> WebElement:
        if element is None:
            element = self.browser
        element_list = element.find_elements_by_xpath(xpath)
        if len(element_list) == 0:
            raise ElementNotFound(f"Could not find {description}")
        elif len(element_list) > 1:
            for i in element_list:
                print(i.get_attribute("outerHTML"))
            raise TooManyElementsFound(f"Found more than one {description}")
        return element_list[0]

    def get_control_from_label(self, text):
        label = self.get_unique_element_from_xpath(f"//label[ contains (text(), '{text}')]", f"Label for {text}")
        id_text = label.get_attribute("for")
        return self.get_unique_element_from_xpath(f"//*[@id='{id_text}']", f"Control for {text}")

    def get_fieldset(self, legend: str):
        xpath = f"//legend[ contains (text(), '{legend}')]/.."
        return self.get_unique_element_from_xpath(xpath, f"Field set: {legend}")

    def get_radio_button(self, element: WebElement, value: str, exact=False):
        if exact:
            xpath = f".//input[@type='radio' and @value='{value}']"
        else:
            xpath = f".//input[@type='radio' and contains(@value, '{value}')]"
        return self.get_unique_element_from_xpath(xpath, f"Radio button '{value}'", element)

    def assert_logged_in(self):
        try:
            self.get_unique_element_from_xpath("//h3[contains(text(), 'COVID Vaccine - 2020/21')]", "title")
        except ElementNotFound:
            raise NotLoggedIn

    def check_vaccinator(self, vaccinator: str) -> bool:
        try:
            self.select_clinician("Pre-Screener", vaccinator, "ui-id-1")
        except UploadException:
            return False
        return True

    @classmethod
    def check_vaccinators(cls, vaccinators: Sequence[str]) -> Set[str]:
        inst = cls.get_instance()
        inst.assert_logged_in()
        return {v for v in vaccinators if not inst.check_vaccinator(v)}

    @classmethod
    def upload_people(cls, people: Sequence[person.Person], batch_info: BatchInfo, save=False):
        inst = cls.get_instance()
        inst.assert_logged_in()
        for p in people:
            try:
                inst.upload_person(p, batch_info, save)
                wx.LogVerbose(f"{p.name} successfully uploaded")
                p.status = "uploaded"
            except selenium.common.exceptions.WebDriverException as e:
                p.status = "error"
                wx.LogVerbose(f"{p.name} upload failed: {str(e.msg)}")
                p.error_type = f"Selenium error: {str(e.msg)}"
            except UploadException as e:
                p.status = "error"
                wx.LogVerbose(f"{p.name} upload failed: {str(e)}")
                p.error_type = f"{type(e).__name__}: {str(e)}"

    def click_radio_button(self, group: str, value: str, exact=False):
        if group.startswith("f:"):
            ctrl = self.get_fieldset(group[2:])
        elif group.startswith("x:"):
            ctrl = self.get_unique_element_from_xpath(group[2:], "radio button control")
        else:
            ctrl = self.get_control_from_label(group)
        radio_button = self.get_radio_button(ctrl, value, exact)
        radio_button.click()

    def enter_text(self, label, text, description=""):
        if label.startswith('x:'):
            if description == "":
                description = f"Unnamed xpath: {label[2:]}"
            ctrl = self.get_unique_element_from_xpath(label[2:], description)
        else:
            ctrl = self.get_control_from_label(label)
        ctrl.clear()
        ctrl.send_keys(text, Keys.TAB)

    def select_clinician(self, role, user, menu_id):
        ctrl = self.get_control_from_label(role)
        ctrl.clear()
        ctrl.send_keys(user)
        time.sleep(1)
        ul = WebDriverWait(self.browser, 10).until(EC.visibility_of_element_located((By.ID, menu_id)))
        screener = self.get_unique_element_from_xpath(f".//a", f"user for {role}", ul)
        screener.click()

    def setup_clinic(self, clinic_date, vaccinator):
        self.click_radio_button("Clinic Type", "Staged Service")
        self.select_clinician("Pre-Screener", vaccinator, "ui-id-1")
        self.enter_text("Vaccination Date", as_date(clinic_date))

    def find_patient(self, p: person.Person) -> str:
        if p.nhs == -1:
            self.find_patient_by_dob(p)
        else:
            self.find_patient_by_nhs(p)
        self.click_radio_button("Consent for email", "No")
        self.click_radio_button("Emergency contact", "No")
        time.sleep(2)
        recommendation = self.get_unique_element_from_xpath("//span[@id='nims_status_when_saved']/strong",
                                                            "dose recommendation")
        recommendation = recommendation.get_attribute('innerHTML')
        return recommendation

    def find_patient_by_nhs(self, p):
        try:
            self.get_unique_element_from_xpath("//input[@value='Search by patient NHS Number']",
                                               "NHS number search button").click()
            time.sleep(1)
        except (WebDriverException, ElementNotFound):
            pass
        self.enter_text("x://input[contains(@id,'pds_dob_entry')]", as_date(p.dob), "DOB entry")
        self.enter_text("x://input[contains(@id,'pds_nhsnumber_entry')]", p.get_text('nhs'), "NHS number")
        # run search
        self.get_unique_element_from_xpath("//input[@value='Lookup via PDS']", "Search PDS button").click()
        # wait for results and confirm
        demographics_table: WebElement = WebDriverWait(self.browser, 2).until(
            EC.presence_of_element_located((By.XPATH, "//table[@class='results-table']")))
        # get highlighted rows, check two entries
        correct_entries = demographics_table.find_elements_by_css_selector(".highlight-data-ok")
        if len(correct_entries) != 2:
            raise UploadException("Incorrect demographics?")
        # click the confirm button
        self.get_unique_element_from_xpath("//input[@value='Confirm Patient']", "Confirm demographics button").click()

    def find_patient_by_dob(self, p: person.Person):
        try:
            self.get_unique_element_from_xpath("//input[@value='Search by patient details']",
                                               "Patient details button").click()
            time.sleep(1)
        except (WebDriverException, ElementNotFound):
            pass
        self.enter_text("x://input[contains(@id,'pds_dob_entry')]", as_date(p.dob), "DOB entry")
        self.click_radio_button("x://label[contains(text(),'Sex')]/..", "female", exact=True)
        last_name, first_name = p.name.split(", ")[:2]
        first_name = first_name.split()[0]
        self.enter_text("x://input[contains(@id,'pds_lastname_entry')]", last_name, "Last name entry")
        self.enter_text("x://input[contains(@id,'pds_firstname_entry')]", first_name, "First name entry")
        # run search
        self.get_unique_element_from_xpath("//input[@value='Lookup via PDS']", "Search PDS button").click()
        # wait for results and confirm
        try:
            demographics_table: WebElement = WebDriverWait(self.browser, 2).until(
                EC.presence_of_element_located((By.XPATH, "//table[@class='results-table']")))
        except WebDriverException:
            self.click_radio_button("x://label[contains(text(),'Sex')]/..", "male", exact=True)
            self.get_unique_element_from_xpath("//input[@value='Lookup via PDS']", "Search PDS button").click()
            try:
                demographics_table: WebElement = WebDriverWait(self.browser, 2).until(
                    EC.presence_of_element_located((By.XPATH, "//table[@class='results-table']")))
            except WebDriverException:
                raise UploadException("Incorrect demographics?")
        # get highlighted rows, check two entries
        correct_entries = demographics_table.find_elements_by_css_selector(".highlight-data-ok")
        if len(correct_entries) < 3:
            raise UploadException("Incorrect demographics?")
        # click the confirm button
        self.get_unique_element_from_xpath("//input[@value='Confirm Patient']", "Confirm demographics button").click()
        time.sleep(2)


    def do_vaccination(self, recommendation: str, batch_info: batch.BatchInfo, p: person.Person):
        if batch_info.drawer == "":
            drawer = p.vaccinator
        else:
            drawer = batch_info.drawer
        self.click_radio_button("Clinically suitable", "Yes")
        self.click_radio_button("f:Vaccination consent", "1")
        self.click_radio_button("f:Consent given by", "Patient")
        self.select_clinician("Drawn up by", drawer, "ui-id-6")
        self.select_clinician("Vaccinator", p.vaccinator, "ui-id-7")
        if "Expect FIRST" in recommendation:
            self.click_radio_button("f:Vaccination Sequence", "First Vaccination")
        elif "Expect SECOND" in recommendation:
            self.click_radio_button("f:Vaccination Sequence", "Second Vaccination")
        else:
            raise VaccinationNotExpected(recommendation)
        if batch_info.manufacturer == "Pfizer":
            vax_type = "BNT162b2"
        else:
            raise UploadException(f"Unknown manufacturer: {batch_info.manufacturer}")
        self.click_radio_button("f:Vaccine Type", vax_type)
        self.enter_text("Batch number", batch_info.batch)
        self.enter_text("Manufacturer expiry", as_date(batch_info.expiry_date))
        self.enter_text("Use by date", as_date(batch_info.use_by_date))
        self.click_radio_button("f:Injection site", "Left deltoid")
        self.click_radio_button("f:Vaccination route", "Intramuscular")
        self.enter_text("Time of vaccination", p.get_text('time'))
        advice_set = self.get_fieldset("Advice provided")
        self.get_unique_element_from_xpath(".//input[@value='Yes']", "Advice Checkbox", advice_set).click()

    def check_success(self):
        try:
            success_box: WebElement = WebDriverWait(self.browser, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.mbsuccess")))
            print(success_box)
            if "successfully entered" in success_box.get_attribute("InnerHTML"):
                return True
            else:
                return False
        except WebDriverException:
            return False

    def upload_person(self, p: person.Person, batch_info: batch.BatchInfo, save=False):
        self.browser.get("https://outcomes4health.org/o4h/services/enter?id=137334&xid=137334&xact=provisionnew")
        time.sleep(2)
        body = self.browser.find_element_by_tag_name('body')
        body.send_keys(Keys.CONTROL + Keys.HOME)
        self.assert_logged_in()
        self.setup_clinic(batch_info.clinic_date, p.vaccinator)
        recommendation = self.find_patient(p)
        self.do_vaccination(recommendation, batch_info, p)

        self.get_unique_element_from_xpath("//input[@type='checkbox' and @name='inContinuousEntry']",
                                           "Do another checkbox").click()
        big_red_button = self.get_unique_element_from_xpath("//input[@type='submit' and @value='Save']", "Submit data")
        if save:
            big_red_button.click()


class TestUploader(Uploader):
    valid_vaccinators = ["Underwood", "Cobley"]
    logged_in = False
    instance = None

    # noinspection PyMissingConstructor
    def __init__(self):
        self.browser = self
        self.title = ""

    def assert_logged_in(self):
        pass

    def check_vaccinator(self, vaccinator: str) -> bool:
        return vaccinator in self.valid_vaccinators

    def upload_person(self, p: person.Person, batch_info: batch.BatchInfo, save=False):
        last_digit = str(p.nhs)[-1]
        if last_digit == "3":
            raise selenium.common.exceptions.WebDriverException("Bad upload")
        elif last_digit == "7":
            raise RecentlyVaccinated(datetime.date(2021, 1, 1))

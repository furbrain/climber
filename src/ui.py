import os
import queue
import time
import unittest
import webbrowser
import threading
from typing import List, Sequence

import wx

import src.batch_manager
from . import person
from . import sessions
from . import form
from .batch import BatchInfo
from .form import ErrorReportPDF
from .gui import MyFrame, GetUploadData
from .ocr import OCR
from .tfile import TFile
from .upload import Uploader, NotLoggedIn
from .tests import test_all


class UploadThread(threading.Thread):
    def __init__(self, q: queue.Queue):
        super().__init__()
        self.stop = False
        self.queue: queue.Queue = q
        self.busy = False

    def time_to_stop(self):
        return self.stop and self.queue.empty()

    def run(self):
        while not self.time_to_stop():
            try:
                batch_info, p = self.queue.get(timeout=0.3)
            except queue.Empty:
                pass
            else:
                self.busy = True
                Uploader.upload_people([p], batch_info, save=True)
                self.busy = False

    def stop(self):
        if self.queue.empty():
            self.stop = True
            return True
        else:
            return False


class ClimberFrame(MyFrame):
    def __init__(self):
        super().__init__(None, wx.ID_ANY, "")
        self.people = person.Everyone()
        self.logger = wx.LogTextCtrl(self.log_info)
        self.bm = src.batch_manager.BatchManager(self)
        wx.Log.SetActiveTarget(self.logger)
        self.upload_queue = queue.Queue()
        self.upload_thread = UploadThread(self.upload_queue)
        self.upload_thread.start()

    def populate_list(self, ctrl: wx.ListCtrl, people: List[person.Person], headings: Sequence[str]):
        for index, p in enumerate(people):
            texts = p.get_texts(headings)
            for col, text in enumerate(texts):
                if col == 0:
                    ctrl.InsertItem(index, text)
                else:
                    ctrl.SetItem(index, col, text)
            ctrl.SetItemData(index, self.people.index(p))

    def get_selected_people(self, ctrl: wx.ListCtrl):
        index = ctrl.GetFirstSelected()
        result = []
        while index != -1:
            person_index = ctrl.GetItemData(index)
            result.append(self.people[person_index])
            index = ctrl.GetNextSelected(index)
        return result

    def update_list(self, list_ctrl: wx.ListCtrl, count_ctrl: wx.StaticText, status: str,
                    headings=person.DEFAULT_HEADINGS):
        list_ctrl.DeleteAllItems()
        filtered_people = sorted(self.people.filter(status=status), key=lambda x: x.time)
        self.populate_list(list_ctrl, filtered_people, headings)
        resize_list_ctrl(list_ctrl)
        count_ctrl.SetLabel(str(len(filtered_people)))

    def update_all_lists(self):
        self.update_list(self.imported_data_list, self.imported_count_label, "imported")
        self.update_list(self.scanned_data_list, self.scanned_count_label,
                         "scanned", person.DEFAULT_HEADINGS + ('vaccinator',))
        self.update_list(self.error_data_list, self.error_count_label, "error",
                         person.DEFAULT_HEADINGS + ('error_type', 'image'))
        self.update_list(self.completed_data_list, self.completed_count_label, "uploaded")

    def import_session(self, event):  # wxGlade: MyFrame.<event_handler>
        with wx.FileDialog(self,
                           "Open Session files",
                           wildcard="Session files (*.rtf; *.csv)|*.rtf;*.csv",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST | wx.FD_MULTIPLE) as fd:
            if fd.ShowModal() != wx.ID_OK:
                return
            paths = fd.GetPaths()
            for path in paths:
                people = sessions.load_people(path)
                self.people.extend(people)
        self.update_all_lists()

    def clear_data(self, event):  # wxGlade: MyFrame.<event_handler>
        if wx.MessageBox("Clear All Data?", style=wx.OK | wx.CANCEL) == wx.OK:
            self.people = person.Everyone()
            self.update_all_lists()

    def create_forms(self, event):  # wxGlade: MyFrame.<event_handler>
        name = TFile.get(".pdf")
        row_count = self.vaccinator_data.GetNumberRows()
        vaccinator_initials = [self.vaccinator_data.GetCellValue(i, 0) for i in range(row_count)]
        pdf = form.DataEntryPDF(vaccinator_initials, self.people.filter(status="imported"))
        pdf.save(name)
        webbrowser.open(name)

    def load_scanned_forms(self, event):  # wxGlade: MyFrame.<event_handler>
        with wx.FileDialog(self,
                           "Open Scanned Forms",
                           wildcard="Image files (*.tif; *.png; *.jpeg; *.jpg)|*.tif;*.png;*.jpeg;*.jpg",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST | wx.FD_MULTIPLE) as fd:
            if fd.ShowModal() != wx.ID_OK:
                return
            paths = fd.GetPaths()
            progress = wx.ProgressDialog("Scanning forms", "Scanning now" + " " * 30, maximum=len(paths))
            wx.Yield()
            OCR.initialise()
            for count, path in enumerate(paths):
                fname = os.path.basename(path)
                if not progress.Update(count, f"Scanning {fname}"):
                    break
                wx.Yield()
                try:
                    scanned_people = OCR.process_form(path, self.get_vaccinators())
                except Exception as e:
                    wx.LogError(str(e))
                    continue
                for p in scanned_people:
                    self.people.update(p)
            progress.Destroy()
            self.update_all_lists()

    def get_vaccinators(self):
        vaccinators = [self.vaccinator_data.GetCellValue(i, 1) for i in range(7)]
        vaccinators = [x for x in vaccinators if x]
        return vaccinators

    def upload_data(self, event):
        # check system is logged in
        if self.scanned_data_list.GetSelectedItemCount() == 0:
            people_to_upload = self.people.filter(status="scanned")
        else:
            people_to_upload = self.get_selected_people(self.scanned_data_list)
        vaccinators = {p.vaccinator for p in people_to_upload}
        wx.LogStatus(f"checking vaccinators: {vaccinators}")
        if not self.vaccinator_list_valid(vaccinators):
            return
        # Get batch and drawer details
        dlg = GetUploadData(self)
        if dlg.ShowModal() != wx.ID_OK:
            return
        batch_info = BatchInfo.from_dialog(dlg)
        if dlg.drawer_is_vaccinator.GetValue():
            for p in people_to_upload:
                p.drawer = p.vaccinator
        else:
            drawer = dlg.drawer_name.GetValue()
            for p in people_to_upload:
                p.drawer = drawer

        progress = wx.ProgressDialog("Uploading records", "Connecting" + " " * 30, maximum=len(people_to_upload))

        def callback(message, number):
            progress.Update(number, message)
            wx.Yield()

        Uploader.upload_people(people_to_upload, batch_info, save=True, callback=callback)
        # update views
        self.update_all_lists()

    def ensure_logged_in(self):
        while True:
            try:
                inst = Uploader.get_instance()
                inst.assert_logged_in()
                break
            except NotLoggedIn:
                dlg = wx.MessageDialog(self,
                                       "Please log in to Pinnacle and go to the Covid 20/21 service",
                                       style=wx.OK | wx.CANCEL)
                if dlg.ShowModal() != wx.ID_OK:
                    return False
        return True

    def vaccinator_list_valid(self, vaccinators):
        success = True
        if not self.ensure_logged_in():
            return False
        failed_vaccinators = Uploader.check_vaccinators(vaccinators)
        if len(failed_vaccinators) > 0:
            success = False
            error_msg = "Unknown vaccinators: " + ', '.join(failed_vaccinators)
            wx.LogError(error_msg)
            wx.MessageBox(error_msg + "\nThis needs to be fixed before uploading")
        return success

    def print_errors(self, event):  # wxGlade: MyFrame.<event_handler>
        errors = self.people.filter(status="error")
        report = ErrorReportPDF(errors)
        fname = TFile.get(suffix=".pdf")
        report.save(fname)
        webbrowser.open(fname)

    def create_summary(self, event):
        print("Event handler 'createSummary' not implemented!")
        event.Skip()

    def check_vaccinators(self, event):  # wxGlade: MyFrame.<event_handler>
        if self.vaccinator_list_valid(self.get_vaccinators()):
            wx.MessageBox("All vaccinators recognised")

    def self_test(self, event):  # wxGlade: MyFrame.<event_handler>
        wx.LogVerbose("Running tests")
        # noinspection PyTypeChecker
        all_tests = unittest.TestLoader().loadTestsFromModule(test_all)
        results = unittest.TestResult()
        results = all_tests.run(results)
        fails = results.errors + results.failures
        if fails:
            fails = '\n'.join(x[1] for x in fails)
            wx.MessageBox(fails, "Errors in self-test")
        else:
            wx.MessageBox(f"No errors found in {results.testsRun} tests", "Success")

    def page_changed(self, event):
        self.update_all_lists()
        if self.notebook_1.GetCurrentPage() == self.notebook_1_Checkin:
            vaccinators = self.get_vaccinators()
            current = self.check_in_drawer.GetCurrentSelection()
            self.check_in_drawer.Set(['Vaccinator'] + vaccinators)
            self.check_in_drawer.SetSelection(current)
            current = self.check_in_vaccinator.GetCurrentSelection()
            self.check_in_vaccinator.Set(vaccinators)
            self.check_in_vaccinator.SetSelection(current)

    def check_in_search_activity(self, event: wx.Event):  # wxGlade: MyFrame.<event_handler>
        event_type = event.GetEventType()
        if event_type == wx.wxEVT_KEY_DOWN:
            assert (isinstance(event, wx.KeyEvent))
            keycode = event.GetKeyCode()
            index = self.check_in_data_list.GetFirstSelected()
            list_size = self.check_in_data_list.GetItemCount()
            if keycode == wx.WXK_DOWN:
                if index == -1:
                    if list_size > 0:
                        self.check_in_data_list.Select(0)
                else:
                    if list_size > index + 1:
                        self.check_in_data_list.Select(index + 1)
                    else:
                        self.check_in_data_list.Select(0)
            elif keycode == wx.WXK_UP:
                if index == -1:
                    if list_size > 0:
                        self.check_in_data_list.Select(list_size - 1)
                else:
                    if index > 0:
                        self.check_in_data_list.Select(index - 1)
                    else:
                        self.check_in_data_list.Select(list_size - 1)
            else:
                event.Skip()
        elif event_type == wx.wxEVT_TEXT:
            # get candidates
            name = self.check_in_search.GetValue()
            candidates = self.people.get_name_matches(name)
            self.check_in_data_list.DeleteAllItems()
            self.populate_list(self.check_in_data_list, candidates, person.DEFAULT_HEADINGS)
        else:
            event.Skip()

    def check_in_upload_clicked(self, event):
        # get person first
        person_count = self.check_in_data_list.GetItemCount()
        index = self.check_in_data_list.GetFirstSelected()
        if person_count == 1:
            person_index = self.check_in_data_list.GetItemData(0)
            p = self.people[person_index]
        elif person_count > 1 and index >= 0:
            p = self.get_selected_people(self.check_in_data_list)[0]
        else:
            wx.MessageBox("You must select a person to upload")
            self.check_in_search.SetFocus()
            return
        p.vaccinator = self.check_in_vaccinator.get_current_string()
        drawer = self.check_in_drawer.get_current_string()
        if drawer == "Vaccinator":
            p.drawer = p.vaccinator
        else:
            p.drawer = drawer
        if len(self.bm.batches) == 0:
            wx.MessageBox("You must specify some batches before uploading. Click 'Manage Batches'")
            return
        batch_index = self.check_in_batch.GetSelection()
        this_batch = self.bm.batches[batch_index]
        if self.upload_thread.busy or self.ensure_logged_in():
            self.upload_queue.put((this_batch, p))
            self.check_in_search.Clear()
            self.check_in_search.SetFocus()

    def manage_batches_clicked(self, event):
        self.bm.ShowModal()
        self.check_in_batch.SetItems([b.batch for b in self.bm.batches])
        if len(self.bm.batches) > 0:
            self.check_in_batch.SetSelection(0)


class MyApp(wx.App):
    # noinspection PyAttributeOutsideInit,PyPep8Naming
    def OnInit(self):
        self.locale = wx.Locale(wx.LANGUAGE_ENGLISH_UK)
        # locale.setlocale(locale.LC_ALL, "en_GB")
        self.Climber = ClimberFrame()
        self.SetTopWindow(self.Climber)
        self.Climber.Show()
        return True


def resize_list_ctrl(ctrl):
    width = ctrl.ColumnCount
    length = ctrl.ItemCount
    if length == 0:
        resize_by = wx.LIST_AUTOSIZE_USEHEADER
    else:
        resize_by = wx.LIST_AUTOSIZE
    for i in range(width):
        ctrl.SetColumnWidth(i, resize_by)

#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# generated by wxGlade 0.9.4 on Fri Dec 11 23:03:44 2020
#
import os
import platform
import unittest
import webbrowser
from typing import Sequence, List
import tests.test_all

import wx
import wx.adv
# begin wxGlade: extracode
import wx.grid
import wx.adv
# end wxGlade
import form
import person
import sessions
from batch import BatchInfo, BatchValidator
from form import ErrorReportPDF
from ocr import OCR
from tfile import TFile
# begin wxGlade: dependencies
# end wxGlade
from upload import Uploader, NotLoggedIn
import ctypes


def resize_list_ctrl(ctrl):
    width = ctrl.ColumnCount
    length = ctrl.ItemCount
    if length == 0:
        resize_by = wx.LIST_AUTOSIZE_USEHEADER
    else:
        resize_by = wx.LIST_AUTOSIZE
    for i in range(width):
        ctrl.SetColumnWidth(i, resize_by)




# noinspection PyPep8Naming,PyUnusedLocal

class GetUploadData(wx.Dialog):
    def __init__(self, *args, **kwds):
        # begin wxGlade: GetUploadData.__init__
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER
        wx.Dialog.__init__(self, *args, **kwds)
        self.clinic_date = wx.adv.DatePickerCtrl(self, wx.ID_ANY)
        self.drawer_is_vaccinator = wx.RadioButton(self, wx.ID_ANY, "Vaccinator draws up")
        self.drawer_is_specified = wx.RadioButton(self, wx.ID_ANY, "Specific drawer: ")
        self.drawer_name = wx.TextCtrl(self, wx.ID_ANY, "")
        self.manufacturer = wx.Choice(self, wx.ID_ANY, choices=["Pfizer", "AstraZeneca 10 dose", "AstraZeneca 8 dose"])
        self.batch = wx.TextCtrl(self, wx.ID_ANY, "")
        self.use_by_date = wx.adv.DatePickerCtrl(self, wx.ID_ANY)
        self.expiry_date = wx.adv.DatePickerCtrl(self, wx.ID_ANY)
        self.ok_button = wx.Button(self, wx.ID_OK, "")
        self.cancel_button = wx.Button(self, wx.ID_CANCEL, "")

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_RADIOBUTTON, lambda x: self.drawer_name.Disable(), self.drawer_is_vaccinator)
        self.Bind(wx.EVT_RADIOBUTTON, lambda x: self.drawer_name.Enable(), self.drawer_is_specified)
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: GetUploadData.__set_properties
        self.SetTitle("Start upload")
        self.drawer_is_vaccinator.SetValue(1)
        self.drawer_name.SetMinSize((300, -1))
        self.drawer_name.Enable(False)
        self.manufacturer.SetSelection(0)
        # end wxGlade
        self.clinic_date.SetValidator(BatchValidator())

    def __do_layout(self):
        # begin wxGlade: GetUploadData.__do_layout
        sizer_10 = wx.BoxSizer(wx.VERTICAL)
        sizer_11 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_12 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, "Vaccine details"), wx.VERTICAL)
        grid_sizer_1 = wx.FlexGridSizer(4, 2, 6, 6)
        sizer_13 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, "Drawer"), wx.VERTICAL)
        sizer_14 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_15 = wx.BoxSizer(wx.HORIZONTAL)
        label_8 = wx.StaticText(self, wx.ID_ANY, "Clinic Date: ", style=wx.ALIGN_RIGHT)
        sizer_15.Add(label_8, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 3)
        sizer_15.Add(self.clinic_date, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 3)
        sizer_10.Add(sizer_15, 0, wx.ALL | wx.EXPAND, 6)
        sizer_13.Add(self.drawer_is_vaccinator, 0, wx.ALL, 3)
        sizer_14.Add(self.drawer_is_specified, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 3)
        sizer_14.Add(self.drawer_name, 1, wx.ALL | wx.EXPAND, 3)
        sizer_13.Add(sizer_14, 1, wx.EXPAND, 0)
        sizer_10.Add(sizer_13, 0, wx.ALL | wx.EXPAND, 6)
        label_5 = wx.StaticText(self, wx.ID_ANY, "Manufacturer: ", style=wx.ALIGN_RIGHT)
        grid_sizer_1.Add(label_5, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT, 0)
        grid_sizer_1.Add(self.manufacturer, 0, 0, 0)
        label_6 = wx.StaticText(self, wx.ID_ANY, "Batch: ", style=wx.ALIGN_RIGHT)
        grid_sizer_1.Add(label_6, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT, 0)
        grid_sizer_1.Add(self.batch, 0, wx.EXPAND, 0)
        label_7 = wx.StaticText(self, wx.ID_ANY, "Use by: ", style=wx.ALIGN_RIGHT)
        grid_sizer_1.Add(label_7, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT, 0)
        grid_sizer_1.Add(self.use_by_date, 0, 0, 0)
        Expires = wx.StaticText(self, wx.ID_ANY, "Expires: ", style=wx.ALIGN_RIGHT)
        grid_sizer_1.Add(Expires, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT, 0)
        grid_sizer_1.Add(self.expiry_date, 0, 0, 0)
        grid_sizer_1.AddGrowableCol(1)
        sizer_12.Add(grid_sizer_1, 1, wx.ALL | wx.EXPAND, 3)
        sizer_10.Add(sizer_12, 0, wx.ALL | wx.EXPAND, 6)
        sizer_11.Add(self.ok_button, 0, wx.ALL, 3)
        sizer_11.Add(self.cancel_button, 0, wx.ALL, 3)
        sizer_10.Add(sizer_11, 0, wx.ALIGN_RIGHT | wx.ALL, 6)
        self.SetSizer(sizer_10)
        sizer_10.Fit(self)
        self.Layout()
        # end wxGlade
# end of class GetUploadData
# noinspection PyPep8Naming, PyUnusedLocal
class MyFrame(wx.Frame):
    # noinspection PyPep8
    def __init__(self, *args, **kwds):
        # begin wxGlade: MyFrame.__init__
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.SetSize((800, 600))
        self.notebook_1 = wx.Notebook(self, wx.ID_ANY)
        self.vaccinators = wx.Panel(self.notebook_1, wx.ID_ANY)
        self.vaccinator_data = wx.grid.Grid(self.vaccinators, wx.ID_ANY, size=(1, 1))
        self.button_8 = wx.Button(self.vaccinators, wx.ID_ANY, "Check vaccinators")
        self.make_forms = wx.Panel(self.notebook_1, wx.ID_ANY)
        self.imported_data_list = wx.ListCtrl(self.make_forms, wx.ID_ANY, style=wx.LC_HRULES | wx.LC_REPORT | wx.LC_VRULES)
        self.imported_count_label = wx.StaticText(self.make_forms, wx.ID_ANY, "0")
        self.button_1 = wx.Button(self.make_forms, wx.ID_ANY, "Import Session")
        self.button_2 = wx.Button(self.make_forms, wx.ID_ANY, "Clear Data")
        self.button_3 = wx.Button(self.make_forms, wx.ID_ANY, "Create Forms")
        self.notebook_1_pane_3 = wx.Panel(self.notebook_1, wx.ID_ANY)
        self.scanned_data_list = wx.ListCtrl(self.notebook_1_pane_3, wx.ID_ANY, style=wx.LC_HRULES | wx.LC_REPORT | wx.LC_VRULES)
        self.scanned_count_label = wx.StaticText(self.notebook_1_pane_3, wx.ID_ANY, "0")
        self.button_4 = wx.Button(self.notebook_1_pane_3, wx.ID_ANY, "Load Forms")
        self.button_5 = wx.Button(self.notebook_1_pane_3, wx.ID_ANY, "Clear Data")
        self.button_6 = wx.Button(self.notebook_1_pane_3, wx.ID_ANY, "Upload Data")
        self.notebook_1_pane_4 = wx.Panel(self.notebook_1, wx.ID_ANY)
        self.completed_data_list = wx.ListCtrl(self.notebook_1_pane_4, wx.ID_ANY, style=wx.LC_HRULES | wx.LC_REPORT | wx.LC_VRULES)
        self.completed_count_label = wx.StaticText(self.notebook_1_pane_4, wx.ID_ANY, "0")
        self.button_10 = wx.Button(self.notebook_1_pane_4, wx.ID_ANY, "Print Summary")
        self.notebook_1_pane_1 = wx.Panel(self.notebook_1, wx.ID_ANY)
        self.error_data_list = wx.ListCtrl(self.notebook_1_pane_1, wx.ID_ANY, style=wx.LC_HRULES | wx.LC_REPORT | wx.LC_VRULES)
        self.error_count_label = wx.StaticText(self.notebook_1_pane_1, wx.ID_ANY, "0")
        self.button_7 = wx.Button(self.notebook_1_pane_1, wx.ID_ANY, "Print Errors")
        self.notebook_1_Logs = wx.Panel(self.notebook_1, wx.ID_ANY)
        self.log_info = wx.TextCtrl(self.notebook_1_Logs, wx.ID_ANY, "", style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_RICH)
        self.notebook_1_About = wx.Panel(self.notebook_1, wx.ID_ANY)
        self.hyperlink_1 = wx.adv.HyperlinkCtrl(self.notebook_1_About, wx.ID_ANY, "Website: http://github.com/furbrain/climber", "http://github.com/furbrain/climber", style=wx.adv.HL_ALIGN_CENTRE)
        self.button_9 = wx.Button(self.notebook_1_About, wx.ID_HELP, "")
        self.button_11 = wx.Button(self.notebook_1_About, wx.ID_ANY, "Self test")

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_BUTTON, self.check_vaccinators, self.button_8)
        self.Bind(wx.EVT_BUTTON, self.importSession, self.button_1)
        self.Bind(wx.EVT_BUTTON, self.clearData, self.button_2)
        self.Bind(wx.EVT_BUTTON, self.createForms, self.button_3)
        self.Bind(wx.EVT_BUTTON, self.loadForms, self.button_4)
        self.Bind(wx.EVT_BUTTON, self.clearData, self.button_5)
        self.Bind(wx.EVT_BUTTON, self.uploadData, self.button_6)
        self.Bind(wx.EVT_BUTTON, self.createSummary, self.button_10)
        self.Bind(wx.EVT_BUTTON, self.print_errors, self.button_7)
        self.Bind(wx.EVT_BUTTON, self.self_test, self.button_11)
        # end wxGlade
        self.people = person.Everyone()
        self.logger = wx.LogTextCtrl(self.log_info)
        wx.Log.SetActiveTarget(self.logger)

    def __set_properties(self):
        # begin wxGlade: MyFrame.__set_properties
        self.SetTitle("Covid Climber")
        self.vaccinator_data.CreateGrid(7, 2)
        self.vaccinator_data.SetColLabelValue(0, "Initials")
        self.vaccinator_data.SetColSize(0, 100)
        self.vaccinator_data.SetColLabelValue(1, "Name")
        self.vaccinator_data.SetColSize(1, 550)
        self.imported_data_list.AppendColumn("Time", format=wx.LIST_FORMAT_LEFT, width=-1)
        self.imported_data_list.AppendColumn("Name", format=wx.LIST_FORMAT_LEFT, width=-1)
        self.imported_data_list.AppendColumn("Dob", format=wx.LIST_FORMAT_LEFT, width=-1)
        self.imported_data_list.AppendColumn("NHS Number", format=wx.LIST_FORMAT_LEFT, width=-1)
        self.scanned_data_list.AppendColumn("Time", format=wx.LIST_FORMAT_LEFT, width=-1)
        self.scanned_data_list.AppendColumn("Name", format=wx.LIST_FORMAT_LEFT, width=-1)
        self.scanned_data_list.AppendColumn("DoB", format=wx.LIST_FORMAT_LEFT, width=-1)
        self.scanned_data_list.AppendColumn("NHS number", format=wx.LIST_FORMAT_LEFT, width=-1)
        self.scanned_data_list.AppendColumn("Vaccinator", format=wx.LIST_FORMAT_LEFT, width=-1)
        self.completed_data_list.AppendColumn("Time", format=wx.LIST_FORMAT_LEFT, width=-1)
        self.completed_data_list.AppendColumn("Name", format=wx.LIST_FORMAT_LEFT, width=-1)
        self.completed_data_list.AppendColumn("Dob", format=wx.LIST_FORMAT_LEFT, width=-1)
        self.completed_data_list.AppendColumn("NHS Number", format=wx.LIST_FORMAT_LEFT, width=-1)
        self.error_data_list.AppendColumn("Time", format=wx.LIST_FORMAT_LEFT, width=-1)
        self.error_data_list.AppendColumn("Name", format=wx.LIST_FORMAT_LEFT, width=-1)
        self.error_data_list.AppendColumn("DoB", format=wx.LIST_FORMAT_LEFT, width=-1)
        self.error_data_list.AppendColumn("NHS number", format=wx.LIST_FORMAT_LEFT, width=-1)
        self.error_data_list.AppendColumn("Error", format=wx.LIST_FORMAT_LEFT, width=-1)
        self.error_data_list.AppendColumn("Has Image", format=wx.LIST_FORMAT_LEFT, width=-1)
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: MyFrame.__do_layout
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_16 = wx.BoxSizer(wx.VERTICAL)
        sizer_18 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_17 = wx.BoxSizer(wx.VERTICAL)
        sizer_19 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_7 = wx.BoxSizer(wx.VERTICAL)
        sizer_8 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_10 = wx.BoxSizer(wx.VERTICAL)
        sizer_11 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_4 = wx.BoxSizer(wx.VERTICAL)
        sizer_5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_2 = wx.BoxSizer(wx.VERTICAL)
        sizer_3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_6 = wx.BoxSizer(wx.VERTICAL)
        sizer_9 = wx.BoxSizer(wx.HORIZONTAL)
        label_2 = wx.StaticText(self.vaccinators, wx.ID_ANY, "Please enter initials and names for all people who may be vaccinating this group", style=wx.ALIGN_LEFT)
        sizer_6.Add(label_2, 0, wx.ALL, 3)
        sizer_6.Add(self.vaccinator_data, 1, wx.ALL | wx.EXPAND, 3)
        sizer_9.Add(self.button_8, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 3)
        sizer_6.Add(sizer_9, 0, wx.ALIGN_RIGHT | wx.ALL, 6)
        self.vaccinators.SetSizer(sizer_6)
        sizer_2.Add(self.imported_data_list, 2, wx.ALL | wx.EXPAND, 3)
        label_1 = wx.StaticText(self.make_forms, wx.ID_ANY, "People:")
        sizer_3.Add(label_1, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 3)
        sizer_3.Add(self.imported_count_label, 2, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 3)
        sizer_3.Add(self.button_1, 0, wx.ALL, 3)
        sizer_3.Add(self.button_2, 0, wx.ALL, 3)
        sizer_3.Add(self.button_3, 0, wx.ALL, 3)
        sizer_2.Add(sizer_3, 0, wx.EXPAND, 0)
        self.make_forms.SetSizer(sizer_2)
        sizer_4.Add(self.scanned_data_list, 1, wx.EXPAND, 0)
        label_4 = wx.StaticText(self.notebook_1_pane_3, wx.ID_ANY, "Scanned People:")
        sizer_5.Add(label_4, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 3)
        sizer_5.Add(self.scanned_count_label, 2, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 3)
        sizer_5.Add(self.button_4, 0, wx.ALL, 3)
        sizer_5.Add(self.button_5, 0, wx.ALL, 3)
        sizer_5.Add(self.button_6, 0, wx.ALL, 3)
        sizer_4.Add(sizer_5, 0, wx.EXPAND, 0)
        self.notebook_1_pane_3.SetSizer(sizer_4)
        sizer_10.Add(self.completed_data_list, 2, wx.ALL | wx.EXPAND, 3)
        label_5 = wx.StaticText(self.notebook_1_pane_4, wx.ID_ANY, "People:")
        sizer_11.Add(label_5, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 3)
        sizer_11.Add(self.completed_count_label, 2, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 3)
        sizer_11.Add(self.button_10, 0, wx.ALL, 3)
        sizer_10.Add(sizer_11, 0, wx.EXPAND, 0)
        self.notebook_1_pane_4.SetSizer(sizer_10)
        sizer_7.Add(self.error_data_list, 1, wx.EXPAND, 0)
        label_3 = wx.StaticText(self.notebook_1_pane_1, wx.ID_ANY, "Error count: ")
        sizer_8.Add(label_3, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 3)
        sizer_8.Add(self.error_count_label, 2, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 3)
        sizer_8.Add(self.button_7, 0, wx.ALL, 3)
        sizer_7.Add(sizer_8, 0, wx.EXPAND, 0)
        self.notebook_1_pane_1.SetSizer(sizer_7)
        sizer_19.Add(self.log_info, 1, wx.ALL | wx.EXPAND, 6)
        self.notebook_1_Logs.SetSizer(sizer_19)
        label_9 = wx.StaticText(self.notebook_1_About, wx.ID_ANY, "Climber: covid vaccine batch uploader")
        label_9.SetFont(wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, ""))
        sizer_17.Add(label_9, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 3)
        label_10 = wx.StaticText(self.notebook_1_About, wx.ID_ANY, "Copyright 2020 Phil Underwood\n")
        sizer_17.Add(label_10, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 3)
        sizer_17.Add(self.hyperlink_1, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 3)
        sizer_16.Add(sizer_17, 1, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL | wx.SHAPED, 6)
        sizer_18.Add(self.button_9, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 3)
        sizer_18.Add(self.button_11, 0, wx.ALL, 3)
        sizer_16.Add(sizer_18, 0, wx.ALIGN_RIGHT | wx.ALL, 6)
        self.notebook_1_About.SetSizer(sizer_16)
        self.notebook_1.AddPage(self.vaccinators, "Vaccinators")
        self.notebook_1.AddPage(self.make_forms, "Make forms")
        self.notebook_1.AddPage(self.notebook_1_pane_3, "Read forms")
        self.notebook_1.AddPage(self.notebook_1_pane_4, "Completed")
        self.notebook_1.AddPage(self.notebook_1_pane_1, "Errors")
        self.notebook_1.AddPage(self.notebook_1_Logs, "Logs")
        self.notebook_1.AddPage(self.notebook_1_About, "About")
        sizer_1.Add(self.notebook_1, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_1)
        self.Layout()
        # end wxGlade

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

    def importSession(self, event):  # wxGlade: MyFrame.<event_handler>
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

    def clearData(self, event):  # wxGlade: MyFrame.<event_handler>
        if wx.MessageBox("Clear All Data?", style=wx.OK | wx.CANCEL) == wx.OK:
            self.people = person.Everyone()
            self.update_all_lists()

    def createForms(self, event):  # wxGlade: MyFrame.<event_handler>
        name = TFile.get(".pdf")
        row_count = self.vaccinator_data.GetNumberRows()
        vaccinator_initials = [self.vaccinator_data.GetCellValue(i, 0) for i in range(row_count)]
        pdf = form.DataEntryPDF(vaccinator_initials, self.people.filter(status="imported"))
        pdf.save(name)
        webbrowser.open(name)

    def loadForms(self, event):  # wxGlade: MyFrame.<event_handler>
        with wx.FileDialog(self,
                           "Open Scanned Forms",
                           wildcard="Image files (*.tif; *.png; *.jpeg; *.jpg)|*.tif;*.png;*.jpeg;*.jpg",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST | wx.FD_MULTIPLE) as fd:
            if fd.ShowModal() != wx.ID_OK:
                return
            paths = fd.GetPaths()
            progress = wx.ProgressDialog("Scanning forms", "Starting up OCR" + " " * 30, maximum=len(paths))
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
                for p in scanned_people:
                    self.people.update(p)
            progress.Destroy()
            self.update_all_lists()

    def get_vaccinators(self):
        vaccinators = [self.vaccinator_data.GetCellValue(i, 1) for i in range(7)]
        vaccinators = [x for x in vaccinators if x]
        return vaccinators

    def uploadData(self, event):  # wxGlade: MyFrame.<event_handler>
        # check system is logged in
        if self.scanned_data_list.GetSelectedItemCount()==0:
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
        batch_info = BatchInfo.fromDialog(dlg)
        progress = wx.ProgressDialog("Uploading records", "Connecting" + " " * 30, maximum=len(people_to_upload))

        def callback(message, number):
            progress.Update(number, message)
            wx.Yield()

        Uploader.upload_people(people_to_upload, batch_info, save=True, callback=callback)
        # update views
        self.update_all_lists()

    def vaccinator_list_valid(self, vaccinators):
        success = True
        while True:
            try:
                failed_vaccinators = Uploader.check_vaccinators(vaccinators)
                break
            except NotLoggedIn:
                dlg = wx.MessageDialog(self,
                                       "Please log in to Outcomes4health and go to the Covid 20/21 service",
                                       style=wx.OK | wx.CANCEL)
                if dlg.ShowModal() != wx.ID_OK:
                    return False
        if len(failed_vaccinators) > 0:
            success = False
            wx.MessageBox("Unknown vaccinators: " + ', '.join(failed_vaccinators))
        return success

    def print_errors(self, event):  # wxGlade: MyFrame.<event_handler>
        errors = self.people.filter(status="error")
        report = ErrorReportPDF(errors)
        fname = TFile.get(suffix=".pdf")
        report.save(fname)
        webbrowser.open(fname)

    def createSummary(self, event):  # wxGlade: MyFrame.<event_handler>
        print("Event handler 'createSummary' not implemented!")
        event.Skip()

    def check_vaccinators(self, event):  # wxGlade: MyFrame.<event_handler>
        if self.vaccinator_list_valid(self.get_vaccinators()):
            wx.MessageBox("All vaccinators recognised")

    # noinspection PyMethodMayBeStatic
    def self_test(self, event):  # wxGlade: MyFrame.<event_handler>
        wx.LogVerbose("Running tests")
        # noinspection PyTypeChecker
        all_tests = unittest.TestLoader().loadTestsFromModule(tests.test_all)
        results = unittest.TestResult()
        results = all_tests.run(results)
        fails = results.errors + results.failures
        if fails:
            fails = '\n'.join(x[1] for x in fails)
            wx.MessageBox(fails, "Errors in self-test")
        else:
            wx.MessageBox(f"No errors found in {results.testsRun} tests", "Success")


# end of class MyFrame

class MyApp(wx.App):
    # noinspection PyAttributeOutsideInit,PyPep8Naming
    def OnInit(self):
        self.locale = wx.Locale(wx.LANGUAGE_ENGLISH_UK)
        # locale.setlocale(locale.LC_ALL, "en_GB")
        self.Climber = MyFrame(None, wx.ID_ANY, "")
        self.SetTopWindow(self.Climber)
        self.Climber.Show()
        return True


# end of class MyApp

if __name__ == "__main__":
    if platform.system() == "Windows":
        PROCESS_PER_MONITOR_DPI_AWARE = 2
        ctypes.windll.shcore.SetProcessDpiAwareness(PROCESS_PER_MONITOR_DPI_AWARE)
    app = MyApp(0)
    app.MainLoop()

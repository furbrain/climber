#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# generated by wxGlade 0.9.4 on Fri Dec 11 23:03:44 2020
#
import webbrowser
from typing import Sequence, List

import wx
# begin wxGlade: extracode
import wx.grid

# end wxGlade
import form
import ocr
import person
import sessions
from form import ErrorReportPDF
from tfile import TFile


# begin wxGlade: dependencies
# end wxGlade


def resize_list_ctrl(ctrl):
    width = ctrl.ColumnCount
    length = ctrl.ItemCount
    if length == 0:
        resize_by = wx.LIST_AUTOSIZE_USEHEADER
    else:
        resize_by = wx.LIST_AUTOSIZE
    for i in range(width):
        ctrl.SetColumnWidth(i, resize_by)


def populate_list(ctrl: wx.ListCtrl, people: List[person.Person], headings: Sequence[str]):
    for index, p in enumerate(people):
        texts = p.get_texts(headings)
        for col, text in enumerate(texts):
            if col == 0:
                ctrl.InsertItem(index, text)
            else:
                ctrl.SetItem(index, col, text)


# noinspection PyPep8Naming,PyUnusedLocal
class MyFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: MyFrame.__init__
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.SetSize((929, 875))
        self.notebook_1 = wx.Notebook(self, wx.ID_ANY)
        self.vaccinators = wx.Panel(self.notebook_1, wx.ID_ANY)
        self.vaccinator_data = wx.grid.Grid(self.vaccinators, wx.ID_ANY, size=(1, 1))
        self.make_forms = wx.Panel(self.notebook_1, wx.ID_ANY)
        self.imported_data_list = wx.ListCtrl(self.make_forms, wx.ID_ANY,
                                              style=wx.LC_HRULES | wx.LC_REPORT | wx.LC_VRULES)
        self.imported_count_label = wx.StaticText(self.make_forms, wx.ID_ANY, "0", style=wx.ALIGN_CENTER)
        self.button_1 = wx.Button(self.make_forms, wx.ID_ANY, "Import Session")
        self.button_2 = wx.Button(self.make_forms, wx.ID_ANY, "Clear Data")
        self.button_3 = wx.Button(self.make_forms, wx.ID_ANY, "Create Forms")
        self.notebook_1_pane_3 = wx.Panel(self.notebook_1, wx.ID_ANY)
        self.scanned_data_list = wx.ListCtrl(self.notebook_1_pane_3, wx.ID_ANY,
                                             style=wx.LC_HRULES | wx.LC_REPORT | wx.LC_VRULES)
        self.scanned_count_label = wx.StaticText(self.notebook_1_pane_3, wx.ID_ANY, "0", style=wx.ALIGN_CENTER)
        self.button_4 = wx.Button(self.notebook_1_pane_3, wx.ID_ANY, "Load Forms")
        self.button_5 = wx.Button(self.notebook_1_pane_3, wx.ID_ANY, "Clear Data")
        self.button_6 = wx.Button(self.notebook_1_pane_3, wx.ID_ANY, "Upload Data")
        self.notebook_1_pane_1 = wx.Panel(self.notebook_1, wx.ID_ANY)
        self.error_data_list = wx.ListCtrl(self.notebook_1_pane_1, wx.ID_ANY,
                                           style=wx.LC_HRULES | wx.LC_REPORT | wx.LC_VRULES)
        self.error_count_label = wx.StaticText(self.notebook_1_pane_1, wx.ID_ANY, "0")
        self.button_7 = wx.Button(self.notebook_1_pane_1, wx.ID_ANY, "Print Errors")
        self.notebook_1_pane_2 = wx.Panel(self.notebook_1, wx.ID_ANY)
        self.log_text = wx.TextCtrl(self.notebook_1_pane_2, wx.ID_ANY, "",
                                    style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_RICH)

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_BUTTON, self.importSession, self.button_1)
        self.Bind(wx.EVT_BUTTON, self.clearData, self.button_2)
        self.Bind(wx.EVT_BUTTON, self.createForms, self.button_3)
        self.Bind(wx.EVT_BUTTON, self.loadForms, self.button_4)
        self.Bind(wx.EVT_BUTTON, self.clearScannedData, self.button_5)
        self.Bind(wx.EVT_BUTTON, self.uploadData, self.button_6)
        self.Bind(wx.EVT_BUTTON, self.print_errors, self.button_7)
        # end wxGlade
        self.people = person.Everyone()

    def __set_properties(self):
        # begin wxGlade: MyFrame.__set_properties
        self.SetTitle("Covid Climber")
        self.vaccinator_data.CreateGrid(7, 2)
        self.vaccinator_data.SetColLabelValue(0, "Initials")
        self.vaccinator_data.SetColSize(0, 100)
        self.vaccinator_data.SetColLabelValue(1, "Name")
        self.vaccinator_data.SetColSize(1, 600)
        self.vaccinator_data.SetRowLabelValue(0, "1")
        self.vaccinator_data.SetRowLabelValue(1, "2")
        self.vaccinator_data.SetRowLabelValue(2, "3")
        self.vaccinator_data.SetRowLabelValue(3, "4")
        self.vaccinator_data.SetRowLabelValue(4, "5")
        self.vaccinator_data.SetRowLabelValue(5, "6")
        self.vaccinator_data.SetRowLabelValue(6, "7")
        self.imported_data_list.AppendColumn("Time", format=wx.LIST_FORMAT_LEFT, width=-1)
        self.imported_data_list.AppendColumn("Name", format=wx.LIST_FORMAT_LEFT, width=-1)
        self.imported_data_list.AppendColumn("Dob", format=wx.LIST_FORMAT_LEFT, width=-1)
        self.imported_data_list.AppendColumn("NHS Number", format=wx.LIST_FORMAT_LEFT, width=-1)
        self.scanned_data_list.AppendColumn("Time", format=wx.LIST_FORMAT_LEFT, width=-1)
        self.scanned_data_list.AppendColumn("Name", format=wx.LIST_FORMAT_LEFT, width=-1)
        self.scanned_data_list.AppendColumn("DoB", format=wx.LIST_FORMAT_LEFT, width=-1)
        self.scanned_data_list.AppendColumn("NHS number", format=wx.LIST_FORMAT_LEFT, width=-1)
        self.scanned_data_list.AppendColumn("Vaccinator", format=wx.LIST_FORMAT_LEFT, width=-1)
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
        sizer_9 = wx.BoxSizer(wx.VERTICAL)
        sizer_7 = wx.BoxSizer(wx.VERTICAL)
        sizer_8 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_4 = wx.BoxSizer(wx.VERTICAL)
        sizer_5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_2 = wx.BoxSizer(wx.VERTICAL)
        sizer_3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_6 = wx.BoxSizer(wx.VERTICAL)
        label_2 = wx.StaticText(self.vaccinators, wx.ID_ANY,
                                "Please enter initials and names for all people who may be vaccinating this group",
                                style=wx.ALIGN_LEFT)
        sizer_6.Add(label_2, 0, wx.ALL, 3)
        sizer_6.Add(self.vaccinator_data, 1, wx.ALL | wx.EXPAND, 3)
        self.vaccinators.SetSizer(sizer_6)
        sizer_2.Add(self.imported_data_list, 2, wx.ALL | wx.EXPAND, 3)
        label_1 = wx.StaticText(self.make_forms, wx.ID_ANY, "People:", style=wx.ALIGN_CENTER)
        sizer_3.Add(label_1, 0, wx.ALIGN_CENTER | wx.ALL, 3)
        sizer_3.Add(self.imported_count_label, 2, wx.ALIGN_CENTER | wx.ALL, 3)
        sizer_3.Add(self.button_1, 0, wx.ALL, 3)
        sizer_3.Add(self.button_2, 0, wx.ALL, 3)
        sizer_3.Add(self.button_3, 0, wx.ALL, 3)
        sizer_2.Add(sizer_3, 0, wx.EXPAND, 0)
        self.make_forms.SetSizer(sizer_2)
        sizer_4.Add(self.scanned_data_list, 1, wx.EXPAND, 0)
        label_4 = wx.StaticText(self.notebook_1_pane_3, wx.ID_ANY, "Scanned People:", style=wx.ALIGN_CENTER)
        sizer_5.Add(label_4, 0, wx.ALIGN_CENTER | wx.ALL, 3)
        sizer_5.Add(self.scanned_count_label, 2, wx.ALIGN_CENTER | wx.ALL, 3)
        sizer_5.Add(self.button_4, 0, wx.ALL, 3)
        sizer_5.Add(self.button_5, 0, wx.ALL, 3)
        sizer_5.Add(self.button_6, 0, wx.ALL, 3)
        sizer_4.Add(sizer_5, 0, wx.EXPAND, 0)
        self.notebook_1_pane_3.SetSizer(sizer_4)
        sizer_7.Add(self.error_data_list, 1, wx.EXPAND, 0)
        label_3 = wx.StaticText(self.notebook_1_pane_1, wx.ID_ANY, "Error count: ")
        sizer_8.Add(label_3, 0, wx.ALIGN_CENTER | wx.ALL, 3)
        sizer_8.Add(self.error_count_label, 2, wx.ALIGN_CENTER | wx.ALL, 3)
        sizer_8.Add(self.button_7, 0, wx.ALL, 3)
        sizer_7.Add(sizer_8, 0, wx.EXPAND, 0)
        self.notebook_1_pane_1.SetSizer(sizer_7)
        sizer_9.Add(self.log_text, 1, wx.ALL | wx.EXPAND, 3)
        self.notebook_1_pane_2.SetSizer(sizer_9)
        self.notebook_1.AddPage(self.vaccinators, "Vaccinators")
        self.notebook_1.AddPage(self.make_forms, "Make forms")
        self.notebook_1.AddPage(self.notebook_1_pane_3, "Read forms")
        self.notebook_1.AddPage(self.notebook_1_pane_1, "Errors")
        self.notebook_1.AddPage(self.notebook_1_pane_2, "Logs")
        sizer_1.Add(self.notebook_1, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_1)
        self.Layout()
        # end wxGlade

    def update_session_list(self):
        self.imported_data_list.DeleteAllItems()
        imported = sorted(self.people.filter(status="imported"), key=lambda x: x.time)
        populate_list(self.imported_data_list, imported, person.DEFAULT_HEADINGS)
        resize_list_ctrl(self.imported_data_list)
        self.imported_count_label.SetLabel(str(len(imported)))

    def update_scanned_list(self):
        self.scanned_data_list.DeleteAllItems()
        people = self.people.filter(status="scanned")
        populate_list(self.scanned_data_list, people, person.DEFAULT_HEADINGS + ('vaccinator',))
        resize_list_ctrl(self.scanned_data_list)
        self.scanned_count_label.SetLabel(str(len(people)))

    def update_error_list(self):
        self.error_data_list.DeleteAllItems()
        errors = self.people.filter(status="error")
        populate_list(self.error_data_list, errors, person.DEFAULT_HEADINGS + ('error_type', 'image'))
        resize_list_ctrl(self.error_data_list)
        self.error_count_label.SetLabel(str(len(errors)))

    def update_all_lists(self):
        self.update_session_list()
        self.update_scanned_list()
        self.update_error_list()

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
            self.people = []
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
            print(paths)
            vaccinators = [self.vaccinator_data.GetCellValue(i, 1) for i in range(7)]
            vaccinators = [x for x in vaccinators if x]
            for path in paths:
                # FIXME check vaccinators...
                print(f"Scanning {path}")
                wx.BeginBusyCursor()
                scanned_people = ocr.ocrreader.get_all_details(path, vaccinators)
                wx.EndBusyCursor()

                for p in scanned_people:
                    self.people.update(p)
            self.update_all_lists()

    def clearScannedData(self, event):  # wxGlade: MyFrame.<event_handler>
        print("Event handler 'clearScannedData' not implemented!")
        event.Skip()

    def uploadData(self, event):  # wxGlade: MyFrame.<event_handler>
        print("Event handler 'uploadData' not implemented!")
        event.Skip()

    def print_errors(self, event):  # wxGlade: MyFrame.<event_handler>
        errors = self.people.filter(status="error")
        report = ErrorReportPDF(errors)
        fname = TFile.get(suffix=".pdf")
        report.save(fname)
        webbrowser.open(fname)


# end of class MyFrame

class MyApp(wx.App):
    # noinspection PyAttributeOutsideInit
    def OnInit(self):
        self.Climber = MyFrame(None, wx.ID_ANY, "")
        self.SetTopWindow(self.Climber)
        self.Climber.Show()
        return True


# end of class MyApp

if __name__ == "__main__":
    app = MyApp(0)
    app.MainLoop()

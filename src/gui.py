#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# generated by wxGlade 0.9.4 on Fri Dec 11 23:03:44 2020
#
import platform

import wx
import wx.adv
# begin wxGlade: extracode
import wx.grid
import wx.adv
# end wxGlade
from .batch import BatchValidator
# begin wxGlade: dependencies
import wx.adv
import wx.grid
# end wxGlade
import ctypes


# noinspection PyPep8Naming,PyUnusedLocal
class GetUploadData(wx.Dialog):
    def __init__(self, *args, **kwds):
        # begin wxGlade: GetUploadData.__init__
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER
        wx.Dialog.__init__(self, *args, **kwds)
        self.SetTitle("Start upload")

        sizer_10 = wx.BoxSizer(wx.VERTICAL)

        sizer_15 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_10.Add(sizer_15, 0, wx.ALL | wx.EXPAND, 6)

        label_8 = wx.StaticText(self, wx.ID_ANY, "Clinic Date: ", style=wx.ALIGN_RIGHT)
        sizer_15.Add(label_8, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 3)

        self.clinic_date = wx.adv.DatePickerCtrl(self, wx.ID_ANY)
        sizer_15.Add(self.clinic_date, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 3)

        sizer_13 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, "Drawer"), wx.VERTICAL)
        sizer_10.Add(sizer_13, 0, wx.ALL | wx.EXPAND, 6)

        self.drawer_is_vaccinator = wx.RadioButton(self, wx.ID_ANY, "Vaccinator draws up")
        self.drawer_is_vaccinator.SetValue(1)
        sizer_13.Add(self.drawer_is_vaccinator, 0, wx.ALL, 3)

        sizer_14 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_13.Add(sizer_14, 1, wx.EXPAND, 0)

        self.drawer_is_specified = wx.RadioButton(self, wx.ID_ANY, "Specific drawer: ")
        sizer_14.Add(self.drawer_is_specified, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 3)

        self.drawer_name = wx.TextCtrl(self, wx.ID_ANY, "")
        self.drawer_name.SetMinSize((300, -1))
        self.drawer_name.Enable(False)
        sizer_14.Add(self.drawer_name, 1, wx.ALL | wx.EXPAND, 3)

        sizer_12 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, "Vaccine details"), wx.VERTICAL)
        sizer_10.Add(sizer_12, 0, wx.ALL | wx.EXPAND, 6)

        grid_sizer_1 = wx.FlexGridSizer(4, 2, 6, 6)
        sizer_12.Add(grid_sizer_1, 1, wx.ALL | wx.EXPAND, 3)

        label_5 = wx.StaticText(self, wx.ID_ANY, "Manufacturer: ", style=wx.ALIGN_RIGHT)
        grid_sizer_1.Add(label_5, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT, 0)

        self.manufacturer = wx.Choice(self, wx.ID_ANY, choices=["Pfizer", "AstraZeneca 10 dose", "AstraZeneca 8 dose"])
        self.manufacturer.SetSelection(0)
        grid_sizer_1.Add(self.manufacturer, 0, 0, 0)

        label_6 = wx.StaticText(self, wx.ID_ANY, "Batch: ", style=wx.ALIGN_RIGHT)
        grid_sizer_1.Add(label_6, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT, 0)

        self.batch = wx.TextCtrl(self, wx.ID_ANY, "")
        grid_sizer_1.Add(self.batch, 0, wx.EXPAND, 0)

        label_7 = wx.StaticText(self, wx.ID_ANY, "Use by: ", style=wx.ALIGN_RIGHT)
        grid_sizer_1.Add(label_7, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT, 0)

        self.use_by_date = wx.adv.DatePickerCtrl(self, wx.ID_ANY)
        grid_sizer_1.Add(self.use_by_date, 0, 0, 0)

        Expires = wx.StaticText(self, wx.ID_ANY, "Expires: ", style=wx.ALIGN_RIGHT)
        grid_sizer_1.Add(Expires, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT, 0)

        self.expiry_date = wx.adv.DatePickerCtrl(self, wx.ID_ANY)
        grid_sizer_1.Add(self.expiry_date, 0, 0, 0)

        sizer_11 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_10.Add(sizer_11, 0, wx.ALIGN_RIGHT | wx.ALL, 6)

        self.ok_button = wx.Button(self, wx.ID_OK, "")
        sizer_11.Add(self.ok_button, 0, wx.ALL, 3)

        self.cancel_button = wx.Button(self, wx.ID_CANCEL, "")
        sizer_11.Add(self.cancel_button, 0, wx.ALL, 3)

        grid_sizer_1.AddGrowableCol(1)

        self.SetSizer(sizer_10)
        sizer_10.Fit(self)

        self.Layout()

        self.Bind(wx.EVT_RADIOBUTTON, lambda x: self.drawer_name.Disable(), self.drawer_is_vaccinator)
        self.Bind(wx.EVT_RADIOBUTTON, lambda x: self.drawer_name.Enable(), self.drawer_is_specified)
        # end wxGlade

    def __set_properties(self):
        # Content of this block not found. Did you rename this class?
        pass
        self.clinic_date.SetValidator(BatchValidator())

    def __do_layout(self):
        # Content of this block not found. Did you rename this class?
        pass
# end of class GetUploadData


# noinspection PyPep8Naming, PyUnusedLocal
class MyFrame(wx.Frame):
    # noinspection PyPep8
    def __init__(self, *args, **kwds):
        # begin wxGlade: MyFrame.__init__
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.SetSize((800, 600))
        self.SetTitle("Covid Climber")

        sizer_1 = wx.BoxSizer(wx.VERTICAL)

        self.notebook_1 = wx.Notebook(self, wx.ID_ANY)
        sizer_1.Add(self.notebook_1, 1, wx.EXPAND, 0)

        self.vaccinators = wx.Panel(self.notebook_1, wx.ID_ANY)
        self.notebook_1.AddPage(self.vaccinators, "Vaccinators")

        sizer_6 = wx.BoxSizer(wx.VERTICAL)

        label_2 = wx.StaticText(self.vaccinators, wx.ID_ANY, "Please enter initials and names for all people who may be vaccinating this group", style=wx.ALIGN_LEFT)
        sizer_6.Add(label_2, 0, wx.ALL, 3)

        self.vaccinator_data = wx.grid.Grid(self.vaccinators, wx.ID_ANY, size=(1, 1))
        self.vaccinator_data.CreateGrid(7, 2)
        self.vaccinator_data.SetColLabelValue(0, "Initials")
        self.vaccinator_data.SetColSize(0, 100)
        self.vaccinator_data.SetColLabelValue(1, "Name")
        self.vaccinator_data.SetColSize(1, 550)
        sizer_6.Add(self.vaccinator_data, 1, wx.ALL | wx.EXPAND, 3)

        sizer_9 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_6.Add(sizer_9, 0, wx.ALIGN_RIGHT | wx.ALL, 6)

        self.button_8 = wx.Button(self.vaccinators, wx.ID_ANY, "Confirm vaccinators")
        sizer_9.Add(self.button_8, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 3)

        self.make_forms = wx.Panel(self.notebook_1, wx.ID_ANY)
        self.notebook_1.AddPage(self.make_forms, "Create forms")

        sizer_2 = wx.BoxSizer(wx.VERTICAL)

        self.imported_data_list = wx.ListCtrl(self.make_forms, wx.ID_ANY, style=wx.LC_HRULES | wx.LC_REPORT | wx.LC_VRULES)
        self.imported_data_list.AppendColumn("Time", format=wx.LIST_FORMAT_LEFT, width=-1)
        self.imported_data_list.AppendColumn("Name", format=wx.LIST_FORMAT_LEFT, width=-1)
        self.imported_data_list.AppendColumn("Dob", format=wx.LIST_FORMAT_LEFT, width=-1)
        self.imported_data_list.AppendColumn("NHS Number", format=wx.LIST_FORMAT_LEFT, width=-1)
        sizer_2.Add(self.imported_data_list, 2, wx.ALL | wx.EXPAND, 3)

        sizer_3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_2.Add(sizer_3, 0, wx.EXPAND, 0)

        label_1 = wx.StaticText(self.make_forms, wx.ID_ANY, "People:")
        sizer_3.Add(label_1, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 3)

        self.imported_count_label = wx.StaticText(self.make_forms, wx.ID_ANY, "0")
        sizer_3.Add(self.imported_count_label, 2, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 3)

        self.button_1 = wx.Button(self.make_forms, wx.ID_ANY, "Import Appointments")
        sizer_3.Add(self.button_1, 0, wx.ALL, 3)

        self.button_2 = wx.Button(self.make_forms, wx.ID_ANY, "Clear Data")
        sizer_3.Add(self.button_2, 0, wx.ALL, 3)

        self.button_3 = wx.Button(self.make_forms, wx.ID_ANY, "Create Forms")
        sizer_3.Add(self.button_3, 0, wx.ALL, 3)

        self.notebook_1_pane_3 = wx.Panel(self.notebook_1, wx.ID_ANY)
        self.notebook_1.AddPage(self.notebook_1_pane_3, "Submit Scans")

        sizer_4 = wx.BoxSizer(wx.VERTICAL)

        self.scanned_data_list = wx.ListCtrl(self.notebook_1_pane_3, wx.ID_ANY, style=wx.LC_HRULES | wx.LC_REPORT | wx.LC_VRULES)
        self.scanned_data_list.AppendColumn("Time", format=wx.LIST_FORMAT_LEFT, width=-1)
        self.scanned_data_list.AppendColumn("Name", format=wx.LIST_FORMAT_LEFT, width=-1)
        self.scanned_data_list.AppendColumn("DoB", format=wx.LIST_FORMAT_LEFT, width=-1)
        self.scanned_data_list.AppendColumn("NHS number", format=wx.LIST_FORMAT_LEFT, width=-1)
        self.scanned_data_list.AppendColumn("Vaccinator", format=wx.LIST_FORMAT_LEFT, width=-1)
        sizer_4.Add(self.scanned_data_list, 1, wx.EXPAND, 0)

        sizer_5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_4.Add(sizer_5, 0, wx.EXPAND, 0)

        label_4 = wx.StaticText(self.notebook_1_pane_3, wx.ID_ANY, "Scanned People:")
        sizer_5.Add(label_4, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 3)

        self.scanned_count_label = wx.StaticText(self.notebook_1_pane_3, wx.ID_ANY, "0")
        sizer_5.Add(self.scanned_count_label, 2, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 3)

        self.button_4 = wx.Button(self.notebook_1_pane_3, wx.ID_ANY, "Read Scanned Forms")
        sizer_5.Add(self.button_4, 0, wx.ALL, 3)

        self.button_5 = wx.Button(self.notebook_1_pane_3, wx.ID_ANY, "Clear Data")
        sizer_5.Add(self.button_5, 0, wx.ALL, 3)

        self.button_6 = wx.Button(self.notebook_1_pane_3, wx.ID_ANY, "Upload to Pinnacle")
        sizer_5.Add(self.button_6, 0, wx.ALL, 3)

        self.notebook_1_pane_4 = wx.Panel(self.notebook_1, wx.ID_ANY)
        self.notebook_1.AddPage(self.notebook_1_pane_4, "Completed")

        sizer_10 = wx.BoxSizer(wx.VERTICAL)

        self.completed_data_list = wx.ListCtrl(self.notebook_1_pane_4, wx.ID_ANY, style=wx.LC_HRULES | wx.LC_REPORT | wx.LC_VRULES)
        self.completed_data_list.AppendColumn("Time", format=wx.LIST_FORMAT_LEFT, width=-1)
        self.completed_data_list.AppendColumn("Name", format=wx.LIST_FORMAT_LEFT, width=-1)
        self.completed_data_list.AppendColumn("Dob", format=wx.LIST_FORMAT_LEFT, width=-1)
        self.completed_data_list.AppendColumn("NHS Number", format=wx.LIST_FORMAT_LEFT, width=-1)
        sizer_10.Add(self.completed_data_list, 2, wx.ALL | wx.EXPAND, 3)

        sizer_11 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_10.Add(sizer_11, 0, wx.EXPAND, 0)

        label_5 = wx.StaticText(self.notebook_1_pane_4, wx.ID_ANY, "People:")
        sizer_11.Add(label_5, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 3)

        self.completed_count_label = wx.StaticText(self.notebook_1_pane_4, wx.ID_ANY, "0")
        sizer_11.Add(self.completed_count_label, 2, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 3)

        self.button_10 = wx.Button(self.notebook_1_pane_4, wx.ID_ANY, "Print Summary")
        sizer_11.Add(self.button_10, 0, wx.ALL, 3)

        self.notebook_1_pane_1 = wx.Panel(self.notebook_1, wx.ID_ANY)
        self.notebook_1.AddPage(self.notebook_1_pane_1, "Errors")

        sizer_7 = wx.BoxSizer(wx.VERTICAL)

        self.error_data_list = wx.ListCtrl(self.notebook_1_pane_1, wx.ID_ANY, style=wx.LC_HRULES | wx.LC_REPORT | wx.LC_VRULES)
        self.error_data_list.AppendColumn("Time", format=wx.LIST_FORMAT_LEFT, width=-1)
        self.error_data_list.AppendColumn("Name", format=wx.LIST_FORMAT_LEFT, width=-1)
        self.error_data_list.AppendColumn("DoB", format=wx.LIST_FORMAT_LEFT, width=-1)
        self.error_data_list.AppendColumn("NHS number", format=wx.LIST_FORMAT_LEFT, width=-1)
        self.error_data_list.AppendColumn("Error", format=wx.LIST_FORMAT_LEFT, width=-1)
        self.error_data_list.AppendColumn("Has Image", format=wx.LIST_FORMAT_LEFT, width=-1)
        sizer_7.Add(self.error_data_list, 1, wx.EXPAND, 0)

        sizer_8 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_7.Add(sizer_8, 0, wx.EXPAND, 0)

        label_3 = wx.StaticText(self.notebook_1_pane_1, wx.ID_ANY, "Error count: ")
        sizer_8.Add(label_3, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 3)

        self.error_count_label = wx.StaticText(self.notebook_1_pane_1, wx.ID_ANY, "0")
        sizer_8.Add(self.error_count_label, 2, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 3)

        self.button_7 = wx.Button(self.notebook_1_pane_1, wx.ID_ANY, "Print Errors")
        sizer_8.Add(self.button_7, 0, wx.ALL, 3)

        self.notebook_1_Logs = wx.Panel(self.notebook_1, wx.ID_ANY)
        self.notebook_1.AddPage(self.notebook_1_Logs, "Logs")

        sizer_19 = wx.BoxSizer(wx.HORIZONTAL)

        self.log_info = wx.TextCtrl(self.notebook_1_Logs, wx.ID_ANY, "", style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_RICH)
        sizer_19.Add(self.log_info, 1, wx.ALL | wx.EXPAND, 6)

        self.notebook_1_About = wx.Panel(self.notebook_1, wx.ID_ANY)
        self.notebook_1.AddPage(self.notebook_1_About, "About")

        sizer_16 = wx.BoxSizer(wx.VERTICAL)

        sizer_17 = wx.BoxSizer(wx.VERTICAL)
        sizer_16.Add(sizer_17, 1, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL | wx.SHAPED, 6)

        label_9 = wx.StaticText(self.notebook_1_About, wx.ID_ANY, "Climber: covid vaccine batch uploader")
        label_9.SetFont(wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, ""))
        sizer_17.Add(label_9, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 3)

        label_10 = wx.StaticText(self.notebook_1_About, wx.ID_ANY, "Copyright 2020 Phil Underwood\n")
        sizer_17.Add(label_10, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 3)

        self.hyperlink_1 = wx.adv.HyperlinkCtrl(self.notebook_1_About, wx.ID_ANY, "Website: http://github.com/furbrain/climber", "http://github.com/furbrain/climber", style=wx.adv.HL_ALIGN_CENTRE)
        sizer_17.Add(self.hyperlink_1, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 3)

        sizer_18 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_16.Add(sizer_18, 0, wx.ALIGN_RIGHT | wx.ALL, 6)

        self.button_9 = wx.Button(self.notebook_1_About, wx.ID_HELP, "")
        sizer_18.Add(self.button_9, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 3)

        self.button_11 = wx.Button(self.notebook_1_About, wx.ID_ANY, "Self test")
        sizer_18.Add(self.button_11, 0, wx.ALL, 3)

        self.notebook_1_About.SetSizer(sizer_16)

        self.notebook_1_Logs.SetSizer(sizer_19)

        self.notebook_1_pane_1.SetSizer(sizer_7)

        self.notebook_1_pane_4.SetSizer(sizer_10)

        self.notebook_1_pane_3.SetSizer(sizer_4)

        self.make_forms.SetSizer(sizer_2)

        self.vaccinators.SetSizer(sizer_6)

        self.SetSizer(sizer_1)

        self.Layout()

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

    # noinspection PyMethodMayBeStatic


# end of class MyFrame


# end of class MyApp

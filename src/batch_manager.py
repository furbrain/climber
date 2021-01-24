import typing

import wx

from src.batch import BatchInfo
from src.gui import BatchDialog, GetUploadData


class BatchManager(BatchDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.batches: typing.List[BatchInfo] = []

    def update_list(self):
        self.batch_list_ctrl.DeleteAllItems()
        for index, b in enumerate(self.batches):
            texts = [b.batch, b.manufacturer, str(b.use_by_date), str(b.expiry_date)]
            for col, text in enumerate(texts):
                if col == 0:
                    self.batch_list_ctrl.InsertItem(index, text)
                else:
                    self.batch_list_ctrl.SetItem(index, col, text)

    def add_batch(self, event):
        dlg = GetUploadData(self)
        dlg.main_sizer.Hide(dlg.clinic_date_section)
        dlg.main_sizer.Hide(dlg.drawer_section)
        if dlg.ShowModal() == wx.ID_OK:
            self.batches.append(BatchInfo.from_dialog(dlg))
            self.update_list()

    def edit_batch(self, event):
        dlg = GetUploadData(self)
        dlg.main_sizer.Hide(dlg.clinic_date_section)
        dlg.main_sizer.Hide(dlg.drawer_section)
        index = self.batch_list_ctrl.GetFirstSelected()
        if index >= 0:
            current = self.batches[index]
            current.fill_dialog(dlg)
            if dlg.ShowModal() == wx.ID_OK:
                self.batches[index] = BatchInfo.from_dialog(dlg)
                self.update_list()

    def delete_batch(self, event):
        index = self.batch_list_ctrl.GetFirstSelected()
        if index >= 0:
            del self.batches[index]
            self.update_list()
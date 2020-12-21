import datetime
import typing

import wx
import wx.adv

if typing.TYPE_CHECKING:
    import gui


def wx2pydt(ctrl: wx.adv.DatePickerCtrl):
    dt: wx.DateTime = ctrl.GetValue()
    return datetime.date.fromtimestamp(dt.GetTicks())


class BatchValidator(wx.Validator):
    def Validate(self, parent: "gui.GetUploadData"):
        print("Validator called")
        clinic_date = wx2pydt(self.GetWindow())
        use_by_date = wx2pydt(parent.use_by_date)
        expiry_date = wx2pydt(parent.expiry_date)
        if clinic_date > use_by_date:
            wx.MessageBox("Clinic date must be on or before use by date")
            return False
        if clinic_date > expiry_date:
            wx.MessageBox("Clinic date must be on or before use by date")
            return False
        if clinic_date > datetime.date.today():
            wx.MessageBox("Clinic date must not be in the future")
            return False
        return True

    def Clone(self):
        return BatchValidator()

    def TransferFromWindow(self):
        return True

    def TransferToWindow(self):
        return True


class BatchInfo:
    def __init__(self, dlg: "gui.GetUploadData"):
        self.clinic_date = wx2pydt(dlg.clinic_date)
        if dlg.drawer_is_vaccinator.GetValue():
            self.drawer = ""
        else:
            self.drawer = dlg.drawer_name.GetValue()
        self.manufacturer = dlg.manufacturer.GetString(dlg.manufacturer.GetCurrentSelection())
        self.batch = dlg.batch.GetValue()
        self.use_by_date = wx2pydt(dlg.use_by_date)
        self.expiry_date = wx2pydt(dlg.expiry_date)

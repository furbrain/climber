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
            wx.MessageBox("Clinic date must be on or before expiry date")
            return False
        if clinic_date > datetime.date.today():
            wx.MessageBox("Clinic date must not be in the future")
            return False
        if parent.batch.GetValue() == "":
            wx.MessageBox("Batch number cannot be empty")
            return False
        return True

    # noinspection PyMethodMayBeStatic
    def Clone(self):
        return BatchValidator()

    # noinspection PyMethodMayBeStatic
    def TransferFromWindow(self):
        return True

    # noinspection PyMethodMayBeStatic
    def TransferToWindow(self):
        return True


class BatchInfo:
    def __init__(self, clinic_date, drawer, manufacturer, batch, use_by_date, expiry_date):
        self.clinic_date = clinic_date
        self.drawer = drawer
        self.manufacturer = manufacturer
        self.batch = batch
        self.use_by_date = use_by_date
        self.expiry_date = expiry_date

    @classmethod
    def fromDialog(cls, dlg: "gui.GetUploadData"):
        clinic_date = wx2pydt(dlg.clinic_date)
        if dlg.drawer_is_vaccinator.GetValue():
            drawer = ""
        else:
            drawer = dlg.drawer_name.GetValue()
        manufacturer = dlg.manufacturer.GetString(dlg.manufacturer.GetCurrentSelection())
        batch = dlg.batch.GetValue()
        use_by_date = wx2pydt(dlg.use_by_date)
        expiry_date = wx2pydt(dlg.expiry_date)
        return cls(clinic_date, drawer, manufacturer, batch, use_by_date, expiry_date)

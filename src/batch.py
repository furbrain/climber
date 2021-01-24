import datetime
import typing

import wx
import wx.adv

if typing.TYPE_CHECKING:
    import gui


def wx2pydt(ctrl: wx.adv.DatePickerCtrl) -> datetime.datetime:
    dt: wx.DateTime = ctrl.GetValue()
    return datetime.datetime.fromtimestamp(dt.GetTicks())


def pydt2wx(dt: datetime.datetime) -> wx.DateTime:
    return wx.DateTime.FromTimeT(dt.timestamp())


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
        if clinic_date.date() > datetime.date.today():
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
    def from_dialog(cls, dlg: "gui.GetUploadData"):
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

    def fill_dialog(self, dlg: "src.gui.GetUploadData"):
        dlg.clinic_date.SetValue(pydt2wx(self.clinic_date))
        dlg.expiry_date.SetValue(pydt2wx(self.expiry_date))
        dlg.use_by_date.SetValue(pydt2wx(self.use_by_date))
        dlg.batch.SetValue(self.batch)
        man_index = dlg.manufacturer.FindString(self.manufacturer)
        dlg.manufacturer.SetSelection(man_index)


# noinspection PyUnusedLocal,PyUnusedLocal,PyUnusedLocal

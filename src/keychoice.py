import wx


class KeyChoice(wx.Choice):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Bind(wx.EVT_CHAR, self.handle_char)

    def handle_char(self, event: wx.KeyEvent):
        keycode = event.GetUnicodeKey()
        if keycode == wx.WXK_NONE:
            event.Skip()
        else:
            key = chr(keycode).lower()
            if key.isalpha():
                num = self.GetCurrentSelection()
                texts = self.GetStrings()
                matches = [e for e, t in enumerate(texts) if t.lower().startswith(key)]
                if matches:
                    matches_after_current = [x for x in matches if x > num]
                    if matches_after_current:
                        next_selection = matches_after_current[0]
                    else:
                        next_selection = matches[0]
                    self.SetSelection(next_selection)
                else:
                    wx.Bell()
            else:
                event.Skip()

    def get_current_string(self):
        index = self.GetSelection()
        return self.GetString(index)

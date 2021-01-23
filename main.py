#!/usr/bin/env python3
import wx
import src.ui
import platform
import ctypes

if platform.system() == "Windows":
    PROCESS_PER_MONITOR_DPI_AWARE = 2
    ctypes.windll.shcore.SetProcessDpiAwareness(PROCESS_PER_MONITOR_DPI_AWARE)
app = src.ui.MyApp(0)
app.MainLoop()

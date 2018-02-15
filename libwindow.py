# -*- coding: utf-8 -*-

from time import sleep

import win32gui
import ctypes
import pywintypes

INVALID_HWND = -1

def get_foreground_window():
    return ctypes.windll.user32.GetForegroundWindow()

def get_caption(hwnd):
    return win32gui.GetWindowText(hwnd)

def get_classname(hwnd):
    """ @return A empty string if failed. """
    try:
        return win32gui.GetClassName(hwnd)
    except Exception:
        pass
    return ''

def is_invalid_hwnd(hwnd):
    return not(win32gui.IsWindow(hwnd))

def is_minimized(hwnd):
    return win32gui.IsIconic(hwnd)!=0

def is_visible(hwnd):
    return win32gui.IsWindowVisible(hwnd)==1

class WindowRect:
    def __init__(self, left, top, right, bottom):
        self.xpos = left
        self.ypos = top
        self._right = right
        self._bottom = bottom
        self.xsize = self._right - self.xpos
        self.ysize = self._bottom - self.ypos

    def __str__(self):
        return 'pos(%d,%d) size(%d,%d)' % (self.xpos, self.ypos, self.xsize, self.ysize)

def get_window_rect(hwnd):
    l, t, r, b = win32gui.GetWindowRect(hwnd)
    return WindowRect(l, t, r, b)

def listup_windows():
    """ @return A list which contains of visible window handles. """
    hparent = 0
    hchild = 0
    queryclassname = None
    querycaption = None
    ret = []
    while True:
        hchild = win32gui.FindWindowEx(hparent, hchild, queryclassname, querycaption)

        # all parsed.
        if hchild==0:
            break

        if not(is_visible(hchild)):
            continue

        ret.append(hchild)

    return ret

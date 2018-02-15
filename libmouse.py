# -*- coding: utf-8 -*-

import win32api
import win32con

def get_cursorpos():
    """ @exception pywintypes.error: (5, 'GetCursorPos', 'アクセスが拒否されました') """
    mx, my = win32api.GetCursorPos()
    return mx, my

def get_cursorpos_safe():
    c = 0
    while True:
        try:
            mx, my = get_cursorpos()
            break
        except pywintypes.error as e:
            c += 1
            if c>10:
                raise e
    return mx, my

def set_cursorpos(x, y):
    prm = (x, y)
    win32api.SetCursorPos(prm)

def _mouse_event_for_clicking(dwFlags):
    # 左右クリック限定なら使わないので固定.
    x = 0
    y = 0
    dwData = 0
    dwExtraInfo = 0

    win32api.mouse_event(dwFlags, x, y, dwData, dwExtraInfo)

def left_click():
    _mouse_event_for_clicking(
        win32con.MOUSEEVENTF_LEFTDOWN | win32con.MOUSEEVENTF_LEFTUP
    )

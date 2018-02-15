# -*- coding: utf-8 -*-

import sys
from time import sleep
import pywintypes

import libwindow
import libmouse

class K:
    LEFT = 37
    UP = 38
    RIGHT = 39
    DOWN = 40

# funcs
# -----

def listup_windows():
    def is_desktop(caption):
        return caption=="Program Manager"
    def is_empty_caption(caption):
        return len(caption)==0
    def is_smaller_than_area_lower_limit(target_rect, given_lower_limit):
        target_area = target_rect.xsize * target_rect.ysize
        return target_area<given_lower_limit
    def has_filtered_classname(target_classname, filterlist):
        for q in filterlist:
            if target_classname.lower().find(q.lower())!=-1:
                return True
        return False
    def has_filtered_caption(target_caption, filterlist):
        for q in filterlist:
            if target_caption.lower().find(q.lower())!=-1:
                return True
        return False

    hwnds = libwindow.listup_windows()

    i = 0
    lmt = len(hwnds)

    while True:
        if i>=lmt:
            break

        hwnd = hwnds[i]

        rect = libwindow.get_window_rect(hwnd)
        classname = libwindow.get_classname(hwnd)
        caption = libwindow.get_caption(hwnd)

        if is_desktop(caption) and not(disable_desktop_filter) or \
           is_empty_caption(caption) and not(disable_empty_caption_filter) or \
           is_smaller_than_area_lower_limit(rect, args.area) or \
           has_filtered_classname(classname, excludee_classnames) or \
           has_filtered_caption(caption, excludee_captions):
            hwnds.pop(i)
            lmt -= 1
            continue

        i += 1

    return hwnds

def activate_by_click(target_hwnd):
    rect = libwindow.get_window_rect(target_hwnd)
    curmx, curmy = libmouse.get_cursorpos()
    libmouse.set_cursorpos(rect.xpos, rect.ypos)
    libmouse.left_click()
    # restore cursor pos.
    libmouse.set_cursorpos(curmx, curmy)

def activate_by_attach(hwnd):
    import win32process
    import win32api
    import win32gui
    import ctypes

    forehwnd = libwindow.get_foreground_window()
    fore_threadid, processid = win32process.GetWindowThreadProcessId(forehwnd)
    current_threadid = win32api.GetCurrentThreadId()

    # foreground なスレッドにアタッチする
    if fore_threadid != current_threadid:
        try:
            # たまに error:87 が起きるので吸収.
            win32process.AttachThreadInput(current_threadid, fore_threadid, True)
        except:
            pass

    try:
        ctypes.windll.user32.BringWindowToTop(hwnd)
    except:
        pass

    if fore_threadid != current_threadid:
        try:
            win32process.AttachThreadInput(current_threadid, fore_threadid, False)
        except:
            pass

def activete(target_hwnd):
    activate_by_attach(target_hwnd)
    activate_by_click(target_hwnd)

def pickup_next_window(foreground_hwnd, direction):
    """ @param A direction value either of K.{UP|DOWN|LEFT|RIGHT}
    @return (INVALID, _) If no next window exists. """
    hwnds = listup_windows()
    if foreground_hwnd in hwnds:
        hwnds.remove(foreground_hwnd)

    def is_new_smallest(p1, p2, cur_smallest):
        diff = p1-p2
        if diff < 0:
            return False
        if diff < cur_smallest:
            return True
        return False

    def is_new_largest(p1, p2, cur_largest):
        diff = p1-p2
        if diff < 0:
            return False
        if diff > cur_largest:
            return True
        return False

    def reverse_direction(direction):
        if direction==K.UP:
            return K.DOWN
        if direction==K.RIGHT:
            return K.LEFT
        if direction==K.DOWN:
            return K.UP
        if direction==K.LEFT:
            return K.RIGHT
        raise RuntimeError('Invalid direction in reverse_direction().')

    def determin_diff_params(direction, fore_rect, rect):
        #next window 方針: とりあえず左端基点で指定方向に関して一番近いもの.
        #
        #up
        #  fore.ypos - hwnd.ypos > 0 かつ、最も小さいもの
        #right
        #  hwnd.xpos - fore.ypos > 0 かつ、最も小さいもの
        #down
        #  hwnd.ypos - fore.ypos > 0 かつ、最も小さいもの
        #left
        #  fore.xpos - hwnd.xpos > 0 かつ、最も小さいもの
        if direction==K.UP:
            p1 = fore_rect.ypos
            p2 = rect.ypos
        elif direction==K.RIGHT:
            p1 = rect.xpos
            p2 = fore_rect.xpos
        elif direction==K.DOWN:
            p1 = rect.ypos
            p2 = fore_rect.ypos
        elif direction==K.LEFT:
            p1 = fore_rect.xpos
            p2 = rect.xpos
        else:
            raise RuntimeError('Invalid direction in pickup_next_windows().')
        return p1, p2

    smallest_diff = 1000000
    next_hwnd = libwindow.INVALID_HWND
    # warp 機能用.
    largest_diff = 0
    largest_hwnd = libwindow.INVALID_HWND

    try:
        fore_rect = libwindow.get_window_rect(foreground_hwnd)
    except pywintypes.error as e:
        return next_hwnd, largest_hwnd

    for hwnd in hwnds:
        rect = libwindow.get_window_rect(hwnd)

        p1, p2 = None, None
        p1, p2 = determin_diff_params(direction, fore_rect, rect)
        if is_new_smallest(p1, p2, smallest_diff):
            smallest_diff = p1 - p2
            next_hwnd = hwnd

        p1_warp, p2_warp = None, None
        direction_warp = reverse_direction(direction)
        p1_warp, p2_warp = determin_diff_params(direction_warp, fore_rect, rect)
        if is_new_largest(p1_warp, p2_warp, largest_diff):
            largest_diff = p1_warp - p2_warp
            largest_hwnd = hwnd

    return next_hwnd, largest_hwnd

# transient mode
# --------------

def transient_switching():
    hwnd = libwindow.INVALID_HWND
    direction = None
    direction_str = ''
    fore_hwnd = libwindow.get_foreground_window()
    if args.up:
        direction = K.UP
        direction_str = 'UP'
    elif args.down:
        direction = K.DOWN
        direction_str = 'DOWN'
    elif args.left:
        direction = K.LEFT
        direction_str = 'LEFT'
    elif args.right:
        direction = K.RIGHT
        direction_str = 'RIGHT'
    else:
        raise RuntimeError('')

    next_hwnd, most_far_hwnd  = pickup_next_window(fore_hwnd, direction)

    if next_hwnd==libwindow.INVALID_HWND:
        if not args.warp or most_far_hwnd==libwindow.INVALID_HWND:
            return
        next_hwnd = most_far_hwnd

    activete(next_hwnd)

# args
# ----

def parse_arguments():
    import argparse

    parser = argparse.ArgumentParser(
        description='End of Altab -- Cursor based window switcher.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument('-w', '--warp', default=False, action='store_true',
        help='Use edge warp.')

    parser.add_argument('-a', '--area', default=10000, type=int,
        help='Use window target exclusion with the lower area(height*width) limit.')
    parser.add_argument('-t', '--title', default=[], nargs='*',
        help='Use window target exclusion with partial match of Caption.')
    parser.add_argument('-c', '--classname', default=[], nargs='*',
        help='Use window target exclusion with partial match of Classname.')
    parser.add_argument('--no-empty-caption', default=False, action='store_true',
        help='Disable window target exclusion with empty caption name.')
    parser.add_argument('--no-desktop', default=False, action='store_true',
        help='Disable exclusion of desktop as a window target.')

    parser.add_argument('--left', default=False, action='store_true',
        help='Switch to the left window and exit.')
    parser.add_argument('--right', default=False, action='store_true',
        help='Switch to the right window and exit.')
    parser.add_argument('--up', default=False, action='store_true',
        help='Switch to the up window and exit.')
    parser.add_argument('--down', default=False, action='store_true',
        help='Switch to the down window and exit.')

    parser.add_argument('--debug-print', default=False, action='store_true',
        help='[DEBUG] Print window information. Only works from .PY, **not .EXE**')

    parsed_args = parser.parse_args()
    return parsed_args

# main
# ----

args = parse_arguments()
excludee_captions = args.title
excludee_classnames = args.classname
disable_empty_caption_filter = args.no_empty_caption
disable_desktop_filter = args.no_desktop
use_debug_print = args.debug_print

if use_debug_print:
    print('captions  : {:}'.format(excludee_captions))
    print('classnames: {:}'.format(excludee_classnames))

    hwnds = listup_windows()
    for hwnd in hwnds:
        rect = libwindow.get_window_rect(hwnd)
        classname = libwindow.get_classname(hwnd)
        caption = libwindow.get_caption(hwnd)
        print('{:>10} "{:}" "{:}" pos({:},{:}) size({:}x{:})'.format(
            hwnd, caption, classname,
            rect.xpos, rect.ypos, rect.xsize, rect.ysize
        ))

if args.left or args.right or args.down or args.up:
    transient_switching()

sys.exit(0)

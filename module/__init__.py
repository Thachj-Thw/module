from __future__ import annotations
from win32gui import (SetParent, SetWindowPos, GetWindowRect, EnableWindow, EnumWindows, GetWindowText,
                      IsWindowVisible, IsWindowEnabled, GetSystemMenu, DeleteMenu)
from win32process import GetWindowThreadProcessId
import win32con
import pywintypes
import ctypes
import traceback
from typing import Union
import threading
import sys
import os


class Path:

    class StringPath(str):
        def __init__(self, path: str):
            self._path = os.path.normpath(path)
            super().__init__()

        def join(self, *args: str):
            path = [os.path.normpath(p) for p in args]
            return os.path.join(self._path, *path)

        def __str__(self):
            return self._path

    def __init__(self, _file_: str):
        self._file = os.path.normpath(_file_)
        self._source = os.path.dirname(self._file)
        if getattr(sys, "frozen", False):
            self._app = os.path.normpath(os.path.dirname(sys.executable))
        else:
            self._app = self._source

    @property
    def source(self):
        return Path.StringPath(self._source)

    @property
    def app(self):
        return Path.StringPath(self._app)


win_pos = Union[list[int, int], tuple[int, int]]
win_size = Union[list[int, int], tuple[int, int]]


class Window:
    def __init__(self, hwnd: int):
        try:
            rect = GetWindowRect(hwnd)
        except pywintypes.error:
            raise ValueError("Invalid window handle. HWND: %s" % hwnd)
        self._hwnd = hwnd
        self._x = rect[0]
        self._y = rect[1]
        self._width = rect[2] - self._x
        self._height = rect[3] - self._y
        self._enabled = IsWindowEnabled(self._hwnd)
        self._pid = GetWindowThreadProcessId(self._hwnd)

    def __str__(self):
        return str(self._hwnd) + " " + GetWindowText(self._hwnd)

    def _refresh(self):
        rect = GetWindowRect(self._hwnd)
        self._x = rect[0]
        self._y = rect[1]
        self._width = rect[2] - self._x
        self._height = rect[3] - self._y

    @classmethod
    def from_pyqt(cls, obj):
        try:
            return cls(int(obj.winId()))
        except AttributeError:
            return None

    @classmethod
    def from_tkinter(cls, obj):
        try:
            return cls(int(obj.root()))
        except AttributeError:
            return None

    @classmethod
    def from_pid(cls, pid: int):
        result = []

        def handle(hwnd, _):
            if IsWindowVisible(hwnd):
                _, cpid = GetWindowThreadProcessId(hwnd)
                if cpid == pid:
                    result.append(hwnd)

        EnumWindows(handle, None)
        return [cls(hwnd) for hwnd in result]

    def list_window_handles(self) -> list:
        result = []

        def handle(hwnd, _):
            if IsWindowVisible(hwnd):
                result.append(hwnd)

        EnumWindows(handle, None)
        return result

    def _update(self):
        SetWindowPos(self.hwnd, 0, self._x, self._y, self._width, self._height, 0)

    @property
    def hwnd(self):
        return self._hwnd

    @property
    def pid(self):
        return self._pid

    @property
    def enabled(self):
        return self._enabled

    @enabled.setter
    def enabled(self, value: bool):
        if not isinstance(value, bool):
            raise TypeError("Enabled must be a boolean")
        self.set_enabled(value)

    def set_enabled(self, __b: bool):
        self._enabled = __b
        EnableWindow(self.hwnd, __b)

    @property
    def x(self):
        self._refresh()
        return self._x

    @x.setter
    def x(self, value: int):
        if not isinstance(value, int):
            raise TypeError("X must be an integer")
        self._x = value
        self._update()

    @property
    def y(self):
        self._refresh()
        return self._y

    @y.setter
    def y(self, value: int):
        if not isinstance(value, int):
            raise TypeError("Y must be an integer")
        self._y = value
        self._update()

    @property
    def width(self):
        self._refresh()
        return self._width

    @width.setter
    def width(self, value: int):
        if not isinstance(value, int):
            raise TypeError("Width must be an integer")
        self._width = value
        self._update()

    @property
    def height(self):
        self._refresh()
        return self._height

    @height.setter
    def height(self, value: int):
        if not isinstance(value, int):
            raise ValueError("Height must be an integer")
        self._height = value
        self._update()

    @property
    def size(self):
        self._refresh()
        return self._width, self._height

    @size.setter
    def size(self, new_size: win_size):
        self.set_window_size(*new_size)

    def set_window_size(self, width: int, height: int):
        self._width, self.height = width, height
        self._update()

    @property
    def position(self):
        self._refresh()
        return self._x, self._y

    @position.setter
    def position(self, new_pos: win_pos):
        if not isinstance(new_pos, (list, tuple)):
            raise ValueError("Position must be a tuple[int, int] or list[int, int]")
        self.set_window_position(*new_pos)

    def attack_child(self, child: Window):
        SetParent(child.hwnd, self.hwnd)

    def set_window_position(self, x: int, y: int):
        self._x, self._y = x, y
        self._update()

    def hide(self):
        ctypes.windll.user32.ShowWindow(self.hwnd, 0)

    def show(self):
        ctypes.windll.user32.ShowWindow(self.hwnd, 1)

    def remove_title_bar(self):
        print("warning remove_title_bar untested")
        title = GetSystemMenu(self.hwnd, 0)
        if title:
            DeleteMenu(title, win32con.SC_CLOSE, win32con.MF_BYCOMMAND)
            DeleteMenu(title, win32con.SC_MINIMIZE, win32con.MF_BYCOMMAND)
            DeleteMenu(title, win32con.SC_MAXIMIZE, win32con.MF_BYCOMMAND)


class ThreadList(list):
    lock = threading.Lock()
    _i = -1

    def next(self):
        with self.lock:
            self._i += 1
            __i = self._i
        if __i < self.__len__():
            return super().__getitem__(__i)


def hide_console():
    hwnd = ctypes.windll.kernel32.GetConsoleWindow()
    if hwnd:
        ctypes.windll.user32.ShowWindow(hwnd, 0)
        ctypes.windll.kernel32.CloseHandle(hwnd)


def alert_excepthook():

    def excepthook(exc_type, exc_value, exc_tb):
        tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
        print(str(tb))
        ctypes.windll.user32.MessageBoxW(None, str(tb), "ERROR", 0)
        sys.exit(0)

    sys.excepthook = excepthook

from __future__ import annotations
from win32gui import (SetParent, SetWindowPos, GetWindowRect, EnableWindow, EnumWindows,
                      GetWindowText, IsWindowVisible, IsWindowEnabled)
from win32process import GetWindowThreadProcessId
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
        self._hwnd = hwnd
        rect = GetWindowRect(hwnd)
        self._x = rect[0]
        self._y = rect[1]
        self._width = rect[2] - self._x
        self._height = rect[3] - self._y
        self._pos = [self._x, self._y]
        self._size = [self._width, self._height]
        self._enabled = IsWindowEnabled(self._hwnd)

    def __str__(self):
        return str(self._hwnd) + " " + GetWindowText(self._hwnd)

    @classmethod
    def from_pyqt(cls, obj):
        return cls(int(obj.winId()))

    @classmethod
    def from_tkinter(cls, obj):
        return cls(int(obj.root()))

    @classmethod
    def from_pid(cls, pid: int):
        result = []

        def handle(hwnd, _):
            if IsWindowVisible(hwnd):
                _, cpid = GetWindowThreadProcessId(hwnd)
                if cpid == pid:
                    result.append(hwnd)

        EnumWindows(handle, None)
        if result:
            return cls(result[0])

    def _update(self):
        SetWindowPos(self.hwnd, 0, self._pos[0], self._pos[1], self._size[0], self._size[1], 0)

    @property
    def hwnd(self):
        return self._hwnd

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
        return self._x

    @x.setter
    def x(self, value: int):
        if not isinstance(value, int):
            raise TypeError("X must be an integer")
        self._x = value
        self._pos[0] = value
        self._update()

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value: int):
        if not isinstance(value, int):
            raise TypeError("Y must be an integer")
        self._y = value
        self._pos[1] = value
        self._update()

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value: int):
        if not isinstance(value, int):
            raise TypeError("Width must be an integer")
        self._width = value
        self._size[0] = value
        self._update()

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value: int):
        if not isinstance(value, int):
            raise ValueError("Height must be an integer")
        self._height = value
        self._size[1] = value
        self._update()

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, new_size: win_size):
        self.set_window_size(new_size)

    def set_window_size(self, width: int, height: int):
        self._width, self.height = width, height
        self._size[0] = width
        self._size[1] = height
        self._update()

    @property
    def position(self):
        return self._pos

    @position.setter
    def position(self, new_pos: win_pos):
        if not isinstance(new_pos, (list, tuple)):
            raise ValueError("Position must be a tuple[int, int] or list[int, int]")
        self.set_window_position(*new_pos)

    def attach_child(self, child: Window):
        SetParent(child.hwnd, self.hwnd)

    def set_window_position(self, x: int, y: int):
        self._x, self._y = x, y
        self._pos[0] = x
        self._pos[1] = y
        self._update()

    def hide(self):
        ctypes.windll.user32.ShowWindow(self.hwnd, 0)

    def show(self):
        ctypes.windll.user32.ShowWindow(self.hwnd, 1)


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
        ctypes.windll.user32.MessageBoxW(None, str(tb), "ERROR", 0)
        sys.exit(0)

    sys.excepthook = excepthook

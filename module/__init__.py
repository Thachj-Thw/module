from __future__ import annotations
from win32gui import SetParent, SetWindowPos, GetWindowRect
import ctypes
import traceback
from typing import Union
import threading
import sys
import os


class Path:
    def __init__(self, _file_: str):
        self._file = os.path.normpath(_file_)
        self._source = os.path.dirname(self._file)
        self._app = os.path.normpath(os.path.dirname(sys.executable)) if getattr(sys, "frozen", False) else self._source

    @property
    def source(self):
        return self._dir

    @property
    def app(self):
        return self._app


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

    def _update(self):
        SetWindowPos(self.hwnd, 0, self._pos[0], self._pos[1], self._size[0], self._size[1], 0)

    @property
    def hwnd(self):
        return self._hwnd

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

    @property
    def position(self):
        return self._pos

    @position.setter
    def position(self, new_pos: win_pos):
        self.set_window_position(new_pos)

    def attach_child(self, child):
        SetParent(child.hwnd, self.hwnd)

    def set_window_position(self, pos: win_pos):
        if not isinstance(pos, win_pos):
            raise ValueError("Position must be a tuple[int, int] or list[int, int]")
        self._pos[0] = pos[0]
        self._pos[1] = pos[1]
        self._update()

    def set_window_size(self, size: win_size):
        if not isinstance(size, win_size):
            raise ValueError("Size must be a tuple[int, int] or list[int int]")
        self._size = size
        self._update()

    def hide(self):
        ctypes.windll.user32.ShowWindow(self.hwnd, 0)

    def show(self):
        ctypes.windll.user32.ShowWindow(self.hwnd, 1)


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


class ThreadList(list):
    lock = threading.Lock()
    _i = -1

    def next(self):
        with self.lock:
            self._i += 1
            __i = self._i
        if __i < self.__len__():
            return super().__getitem__(__i)

# import degree
from enum import Enum


class Color(Enum):
    GRAY = 0
    RED = 1
    BLUE = 2
    WATER = 3


class Soldier(object):
    def __init__(self, degree, position_x, position_y, color):
        self._degree = degree
        self._position_x = position_x
        self._position_y = position_y
        self._color = color
        self._is_alive = True
        # self._num_steps = 1
        # if degree == degree.BOMB or degree == degree.FLAG:
        #     self._num_steps = 0
        # elif degree == degree.TWO:
        #     self._num_steps

    @property
    def degree(self):
        return self._degree

    @property
    def position(self):
        return self._position_x, self._position_y

    @property
    def x(self):
        return self._position_x

    @property
    def y(self):
        return self._position_y

    @property
    def color(self):
        return self._color

    @property
    def is_alive(self):
        return self._is_alive

    def set_position(self, position_x, position_y):
        self._position_x = position_x
        self._position_y = position_y

    def set_x(self, position_x):
        self._position_x = position_x

    def set_y(self, position_y):
        self._position_y = position_y

    def kill_me(self):
        self._is_alive = False

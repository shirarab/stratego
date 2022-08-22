
class Soldier(object):
    def __init__(self, degree, position_x, position_y, color):
        self._degree = degree
        self._position_x = position_x
        self._position_y = position_y
        self._color = color
        self._is_alive = True
        self._show_me = False
        self._has_moved = False

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

    @property
    def show_me(self):
        return self._show_me

    @property
    def has_moved(self):
        return self._has_moved

    def set_position(self, position_x, position_y):
        self._position_x = position_x
        self._position_y = position_y

    def set_x(self, position_x):
        self._position_x = position_x

    def set_y(self, position_y):
        self._position_y = position_y

    def kill_me(self):
        self._is_alive = False

    def set_show_me(self):
        self._show_me = True

    def set_has_moved(self):
        self._has_moved = True

    def store(self):
        return self._position_x, self._position_y, self._is_alive, self._show_me

    def restore(self, stored_info):
        self._position_x = stored_info[0]
        self._position_y = stored_info[1]
        self._is_alive = stored_info[2]
        self._show_me = stored_info[3]

from enum import IntEnum, Enum


class Degree(IntEnum):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    FLAG = 0
    BOMB = -1
    WATER = -2
    EMPTY = -3


BOARD_SIZE = 10

DEAD_SOLDIERS = {
    Degree.BOMB: 0,
    Degree.ONE: 0,
    Degree.TWO: 0,
    Degree.THREE: 0,
    Degree.FOUR: 0,
    Degree.FIVE: 0,
    Degree.SIX: 0,
    Degree.SEVEN: 0,
    Degree.EIGHT: 0,
    Degree.NINE: 0,
    Degree.TEN: 0,
    Degree.FLAG: 0
}


class Color(Enum):
    GRAY = 0
    RED = 1
    BLUE = 2
    WATER = 3


NUM_OF_PLAYER_DEGREE_SOLDIERS = {
    Degree.BOMB: 6,
    Degree.ONE: 1,
    Degree.TWO: 8,
    Degree.THREE: 5,
    Degree.FOUR: 4,
    Degree.FIVE: 4,
    Degree.SIX: 4,
    Degree.SEVEN: 3,
    Degree.EIGHT: 2,
    Degree.NINE: 1,
    Degree.TEN: 1,
    Degree.FLAG: 1
}


class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4

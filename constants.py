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


OP_COLOR = {
    Color.BLUE: Color.RED,
    Color.RED: Color.BLUE
}

UNMOVABLE = {
    Degree.BOMB,
    Degree.FLAG
}

SOLDIER_COUNT_FOR_EACH_DEGREE = {
    Degree.FLAG: 1,
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
    Degree.TEN: 1
}


class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4


DEGREE_OPTIONS_LIST = [j.value for j in Degree]

PLAYER_SOLDIER_DEGREES_LIST = [d for d in SOLDIER_COUNT_FOR_EACH_DEGREE]

NUM_OF_PLAYER_SOLDIERS = 40

OP_DISTANCE_FROM_FLAG = 5

JEROEN_METS_VALUES_TABLE = {
    # degree: (moved, discovered, captured)
    Degree.BOMB: (0, 100, 750),
    Degree.ONE: (100, 0, 100),  # Spy
    Degree.TWO: (100, 0, 2),  # Scout
    Degree.THREE: (100, 20, 50),  # Miner
    Degree.FOUR: (100, 5, 5),  # Sergeant
    Degree.FIVE: (100, 10, 10),  # Lieutenant
    Degree.SIX: (100, 15, 20),  # Captain
    Degree.SEVEN: (100, 20, 50),  # Major
    Degree.EIGHT: (100, 25, 100),  # Colonel
    Degree.NINE: (100, 50, 250),  # General
    Degree.TEN: (100, 100, 500),  # Marshal
    Degree.FLAG: (0, 0, 1000)
}

NUVC_VALUES_TABLE = {
    # degree: (moved, discovered, captured)
    Degree.BOMB: 10,
    Degree.ONE: (10, 1),  # Spy
    Degree.TWO: 1,  # Scout
    Degree.THREE: (6, 3),  # Miner
    Degree.FOUR: 4,  # Sergeant
    Degree.FIVE: 5,  # Lieutenant
    Degree.SIX: 12,  # Captain
    Degree.SEVEN: 14,  # Major
    Degree.EIGHT: 16,  # Colonel
    Degree.NINE: 18,  # General
    Degree.TEN: (20, 40),  # Marshal
    Degree.FLAG: 0
}

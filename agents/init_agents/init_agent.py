import abc
import random
from typing import Set

from agents.init_agents.init_heuristics import init_null_heuristic
from constants import Color
from soldier import Soldier
from graphics.graphic import Graphic


class InitAgent(object):
    def __init__(self, heuristic=init_null_heuristic):
        self._heuristic = heuristic

    @property
    def heuristic(self):
        return self._heuristic

    @abc.abstractmethod
    def get_initial_positions(self, soldiers: Set[Soldier],
                              graphic: Graphic, color: Color = None):
        return

    def get_initial_random_board(self, soldiers: Set[Soldier]):
        # return 4*10 board
        cp_soldiers = soldiers.copy()
        num_rows, num_cols = 4, 10
        board = [[None for i in range(num_cols)] for j in range(num_rows)]
        for i in range(num_rows):
            for j in range(num_cols):
                soldier = random.sample(cp_soldiers, 1)[0]
                cp_soldiers.remove(soldier)
                board[i][j] = soldier
                soldier.set_position(i, j)
        return board

import random
from typing import Set

from agents.init_agents.init_agent import InitAgent
from graphics.stratego_graphic import StrategoGraphic
from soldier import Soldier, Color


class InitRandomAgent(InitAgent):
    def get_initial_positions(self, soldiers: Set[Soldier], graphic: StrategoGraphic, color: Color = None):
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

from typing import Set

from agents.init_agents.init_agent import InitAgent
from graphics.stratego_graphic import StrategoGraphic
from soldier import Soldier


class InitHumanAgent(InitAgent):
    def get_initial_positions(self, soldiers: Set[Soldier], graphic: StrategoGraphic):
        cp_soldiers = soldiers.copy()
        optional_positions = set()
        num_rows, num_cols = 4, 10
        board = [[None for i in range(num_cols)] for j in range(num_rows)]
        for i in range(num_rows):
            for j in range(num_cols):
                optional_positions.add((i, j))
        while len(optional_positions) > 0:
            soldier, x, y = graphic.ask_for_initial_position(list(cp_soldiers), optional_positions)
            board[x][y] = soldier
            cp_soldiers.remove(soldier)
            optional_positions.remove((x, y))
            soldier.set_position(x, y)
        return board

import random
from typing import Set

from agents.init_agents.init_agent import InitAgent
from graphics.stratego_graphic import StrategoGraphic
from soldier import Soldier, Color


class InitRandomAgent(InitAgent):
    def get_initial_positions(self, soldiers: Set[Soldier],
                              graphic: StrategoGraphic, color: Color = None):
        # return 4*10 board
        return self.get_initial_random_board(soldiers)

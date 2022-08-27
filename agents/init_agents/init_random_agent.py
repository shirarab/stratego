import random
from typing import Set

from agents.init_agents.init_agent import InitAgent
from graphics.graphic import Graphic
from constants import Color
from soldier import Soldier#, Color


class InitRandomAgent(InitAgent):
    def get_initial_positions(self, soldiers: Set[Soldier],
                              graphic: Graphic, color: Color = None):
        # return 4*10 board
        return self.get_initial_random_board(soldiers)

from typing import Set

from agent import Agent
from action import Action
import random

from agents.init_agent import InitAgent
from game_state import GameState
from soldier import Soldier
from stratego_graphic import StrategoGraphic


class InitRandomAgent(InitAgent):
    def get_initial_positions(self, soldiers: Set[Soldier], graphic: StrategoGraphic):
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


class RandomAgent(Agent):
    def __init__(self, color, graphic: StrategoGraphic = None, init_agent: InitAgent = None):
        super().__init__(color, graphic, init_agent)
        if init_agent is None:
            self._init_agent = InitRandomAgent()

    def get_action(self, game_state: GameState) -> Action:
        legal_actions = game_state.get_legal_actions(self.color)
        if legal_actions == set():
            return None
        return random.sample(legal_actions, 1)[0]

    def get_initial_positions(self):
        return self.init_agent.get_initial_positions(self.soldiers, self.graphic)

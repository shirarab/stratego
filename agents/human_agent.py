from typing import Set

from agent import Agent
from action import Action
from agents.init_agent import InitAgent

from game_state import GameState
from soldier import Soldier
from stratego_graphic import StrategoGraphic


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


class HumanAgent(Agent):
    def __init__(self, color, graphic: StrategoGraphic = None, init_agent: InitAgent = None):
        super().__init__(color, graphic, init_agent)
        if init_agent is None:
            self._init_agent = InitHumanAgent()

    def get_action(self, game_state: GameState) -> Action:
        legal_actions = game_state.get_legal_actions(self.color)
        if legal_actions == set():
            return None
        action = None
        while action not in legal_actions:
            x, y, direction, num_steps = self.graphic.ask_for_action(game_state)
            soldier = game_state.get_soldier_at_x_y(x, y)
            action = Action(soldier, direction, num_steps)
        return action

    def get_initial_positions(self):
        return self.init_agent.get_initial_positions(self.soldiers, self.graphic)

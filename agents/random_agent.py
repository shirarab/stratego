from agents.agent import Agent
from action import Action
import random

from agents.init_agents.init_agent import InitAgent
from agents.init_agents.init_random_agent import InitRandomAgent
from game_state import GameState
from graphics.stratego_graphic import StrategoGraphic


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
        return self.init_agent.get_initial_positions(self.soldiers, self.graphic, self.color)

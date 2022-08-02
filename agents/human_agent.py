from agents.agent import Agent
from action import Action
from agents.init_agents.init_agent import InitAgent
from agents.init_agents.init_human_agent import InitHumanAgent

from game_state import GameState
from graphics.stratego_graphic import StrategoGraphic


class HumanAgent(Agent):
    def __init__(self, color, graphic: StrategoGraphic = None, init_agent: InitAgent = None):
        super().__init__(color, graphic, init_agent)
        if init_agent is None:
            self._init_agent = InitHumanAgent()

    def get_action(self, game_state: GameState) -> Action:
        legal_actions = game_state.get_legal_actions(self.color)
        for a in legal_actions:
            print(a.soldier.degree,"x:", a.soldier.x, "y:", a.soldier.y, "dir:", a.direction, "steps:", a.num_steps)
        if legal_actions == set():
            return None
        action = None
        while action not in legal_actions:
            x, y, direction, num_steps = self.graphic.ask_for_action(game_state)
            soldier = game_state.get_soldier_at_x_y(x, y)
            action = Action(soldier, direction, num_steps)
        return action

    def get_initial_positions(self):
        return self.init_agent.get_initial_positions(self.soldiers, self.graphic, self.color)

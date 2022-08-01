import abc

from agents.init_agent import InitAgent
from stratego_graphic import StrategoGraphic


class Agent(object):
    def __init__(self, color, graphic: StrategoGraphic, init_agent: InitAgent):
        self._color = color
        self._my_soldiers = set()  # 40 soldiers
        self._init_agent = init_agent
        self._graphic = graphic

    @property
    def color(self):
        return self._color

    @property
    def soldiers(self):
        return self._my_soldiers

    @property
    def init_agent(self):
        return self._init_agent

    @property
    def graphic(self):
        return self._graphic

    @abc.abstractmethod
    def get_action(self, game_state):
        return

    @abc.abstractmethod
    def get_initial_positions(self):
        # return 4*10 board
        return

    def set_start_soldiers(self, soldiers):
        self._my_soldiers = soldiers
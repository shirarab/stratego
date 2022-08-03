import abc

from agents.init_agents.init_agent import InitAgent
from agents.init_agents.init_random_agent import InitRandomAgent
from graphics.stratego_graphic import StrategoGraphic
from agents.heuristics import null_heuristic


class Agent(object):
    def __init__(self, color, graphic: StrategoGraphic, init_agent: InitAgent,
                 heuristic=null_heuristic, depth: int = 0):
        self._heuristic = heuristic
        self._color = color
        self._my_soldiers = set()  # 40 soldiers
        self._init_agent = init_agent
        self._graphic = graphic
        self._depth = depth
        if init_agent is None:
            self._init_agent = InitRandomAgent()

    @property
    def depth(self):
        return self._depth

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

    @property
    def heuristic(self):
        return self._heuristic

    @abc.abstractmethod
    def get_action(self, game_state):
        return

    @abc.abstractmethod
    def get_initial_positions(self):
        # return 4*10 board
        return

    def set_start_soldiers(self, soldiers):
        self._my_soldiers = soldiers
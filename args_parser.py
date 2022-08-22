import argparse

from agents.alpha_beta_agent import AlphaBetaAgent
from agents.guessing_alpha_beta_agent import GuessingAlphaBetaAgent
from agents.human_agent import HumanAgent
from agents.init_agents.init_hill_climbing_agent import InitHillClimbingAgent
from agents.init_agents.init_human_agent import InitHumanAgent
from agents.init_agents.init_random_agent import InitRandomAgent
from agents.random_agent import RandomAgent
from constants import BOARD_SIZE, Color
from graphics.console_graphic import ConsoleGraphic
from graphics.gui_graphic import GuiGraphic
from graphics.stratego_graphic import StrategoGraphic

DISPLAYS = {'console': ConsoleGraphic,
            'gui': GuiGraphic}

INIT_AGENTS = {'InitRandomAgent': InitRandomAgent,
               'InitHumanAgent': InitHumanAgent,
               'InitHillClimbingAgent': InitHillClimbingAgent}

AGENTS = {'RandomAgent': RandomAgent,
          'HumanAgent': HumanAgent,
          'AlphaBetaAgent': AlphaBetaAgent,
          'GuessingAlphaBetaAgent': GuessingAlphaBetaAgent}

PLAYER_COLORS = {Color.RED: 'red', Color.BLUE: 'blue'}

DEFAULT_DISPLAY = 'GuiGraphic'
DEFAULT_AGENT = 'RandomAgent'
DEFAULT_EVALUATION_FUNCTION = 'num_soldiers_evaluator'


class ArgsParser(object):
    def __init__(self):
        self._parser = argparse.ArgumentParser(description='Stratego Game.')
        self._args = None
        self._is_parsed = False

    def parse(self):
        # some params
        self._parser.add_argument('-g', '--display', dest='display',
                                  choices=DISPLAYS.keys(), help='The game ui.',
                                  default=DEFAULT_DISPLAY, type=str)
        self._parser.add_argument('-p', '--num_players_to_show', dest='num_players_to_show',
                                  choices=[0, 1, 2], help='The number of players to show on board.',
                                  default=1, type=int)
        self._parser.add_argument('-d', '--depth', dest='depth',
                                  help='The maximum depth for to search in the game tree.',
                                  default=2, type=int)
        self._parser.add_argument('-n', '--num_of_games', dest='num_of_games',
                                  help='The number of games to run.',
                                  default=1, type=int)

        # init agents and agents
        self._parser.add_argument('-ria', '--red_init_agent', dest='red_init_agent',
                                  choices=INIT_AGENTS.keys(), help='The red init agent.',
                                  default=None, type=str)
        self._parser.add_argument('-bia', '--blue_init_agent', dest='blue_init_agent',
                                  choices=INIT_AGENTS.keys(), help='The blue init agent.',
                                  default=None, type=str)
        self._parser.add_argument('-ra', '--red_agent', dest='red_agent',
                                  choices=AGENTS.keys(), help='The red agent.',
                                  default=DEFAULT_AGENT, type=str)
        self._parser.add_argument('-ba', '--blue_agent', dest='blue_agent',
                                  choices=AGENTS, help='The blue agent.',
                                  default=DEFAULT_AGENT, type=str)

        # score evaluation function
        self._parser.add_argument('-e', '--evaluation_function', dest='evaluation_function',
                                  help='The evaluation function for ai agent.',
                                  default=DEFAULT_EVALUATION_FUNCTION, type=str)

        # init agents heuristics
        self._parser.add_argument('-rih', '--red_init_heuristic', dest='red_init_heuristic',
                                  help='The red agent init heuristic.',
                                  default=None, type=str)
        self._parser.add_argument('-bih', '--blue_init_heuristic', dest='blue_init_heuristic',
                                  help='The blue agent init heuristic.',
                                  default=None, type=str)

        # agents heuristics and functions
        self._parser.add_argument('-rh', '--red_heuristic', dest='red_heuristic',
                                  help='The red agent heuristic.',
                                  default=None, type=str)
        self._parser.add_argument('-bh', '--blue_heuristic', dest='blue_heuristic',
                                  help='The blue agent heuristic.',
                                  default=None, type=str)
        self._parser.add_argument('-roh', '--red_opponent_heuristic', dest='red_opponent_heuristic',
                                  help='The red agent opponent heuristic.',
                                  default=None, type=str)
        self._parser.add_argument('-boh', '--blue_opponent_heuristic', dest='blue_opponent_heuristic',
                                  help='The blue agent opponent heuristic.',
                                  default=None, type=str)
        self._parser.add_argument('-rola', '--red_get_legal_actions_opponent', dest='red_get_legal_actions_opponent',
                                  help='The get legal actions of red opponent.',
                                  default=None, type=str)
        self._parser.add_argument('-bola', '--blue_get_legal_actions_opponent', dest='blue_get_legal_actions_opponent',
                                  help='The get legal actions of blue opponent.',
                                  default=None, type=str)
        self._parser.add_argument('-ros', '--red_get_successor_opponents', dest='red_get_successor_opponents',
                                  help='The get successor of red opponent.',
                                  default=None, type=str)
        self._parser.add_argument('-bos', '--blue_get_successor_opponents', dest='blue_get_successor_opponents',
                                  help='The get successor of blue opponent.',
                                  default=None, type=str)

        self._args = self._parser.parse_args()
        self._is_parsed = True

        # self._parser.print_help()

    def check_is_parse(self):
        if not self._is_parsed:
            raise Exception('Need to parse arguments first')

    def get_num_of_games(self):
        self.check_is_parse()
        return self._args.num_of_games

    def get_graphic(self):
        self.check_is_parse()
        display_name = self._args.display
        num_players_to_show = self._args.num_players_to_show
        if display_name not in DISPLAYS.keys():
            raise Exception('Invalid graphic chosen.')

        return DISPLAYS[display_name](BOARD_SIZE, num_players_to_show)

    def get_init_agent(self, color: Color):
        self.check_is_parse()
        if color not in PLAYER_COLORS.keys():
            raise Exception('Invalid color given.')
        init_agent_name = getattr(self._args, PLAYER_COLORS[color] + '_init_agent')
        if init_agent_name is None:
            return None
        if init_agent_name not in INIT_AGENTS.keys():
            raise Exception('Invalid init agent chosen.')
        init_heuristic = self.get_init_heuristic(color)
        if init_heuristic is None:
            return INIT_AGENTS[init_agent_name]()
        return INIT_AGENTS[init_agent_name](heuristic=init_heuristic)

    def get_agent(self, color: Color, graphic: StrategoGraphic):
        self.check_is_parse()
        init_agent = self.get_init_agent(color)
        agent_name = getattr(self._args, PLAYER_COLORS[color] + '_agent')

        if agent_name not in AGENTS.keys():
            raise Exception('Invalid agent chosen.')

        obj = {}
        heuristic = self.get_heuristic(color)
        opponent_heuristic = self.get_opponent_heuristic(color)
        get_legal_actions_opponent = self.get_legal_actions_opponent(color)
        get_successor_opponents = self.get_successor_opponents(color)
        if heuristic is not None:
            obj['heuristic'] = heuristic
        if opponent_heuristic is not None:
            obj['opponent_heuristic'] = opponent_heuristic
        if get_legal_actions_opponent is not None:
            obj['get_legal_actions_opponent'] = get_legal_actions_opponent
        if get_successor_opponents is not None:
            obj['get_successor_opponents'] = get_successor_opponents

        return AGENTS[agent_name](color, graphic, init_agent, depth=self._args.depth, **obj)

    def get_evaluation_function(self):
        self.check_is_parse()
        return lookup("evaluate_score." + self._args.evaluation_function, globals())

    def get_init_heuristic(self, color: Color):
        self.check_is_parse()
        init_heuristic_name = getattr(self._args, PLAYER_COLORS[color] + '_init_heuristic')
        if init_heuristic_name is None:
            return None
        init_agents_module = lookup("agents.init_agents", globals())
        init_heuristics_module = getattr(init_agents_module, 'init_heuristics')
        return getattr(init_heuristics_module, init_heuristic_name)

    def get_heuristic(self, color: Color, atr_name='_heuristic'):
        self.check_is_parse()
        heuristic_name = getattr(self._args, PLAYER_COLORS[color] + atr_name)
        if heuristic_name is None:
            return None
        agents_heuristics_module = lookup("agents.heuristics", globals())
        return getattr(agents_heuristics_module, heuristic_name)

    def get_opponent_heuristic(self, color: Color):
        return self.get_heuristic(color, '_opponent_heuristic')

    def get_legal_actions_opponent(self, color: Color):
        self.check_is_parse()
        name = getattr(self._args, PLAYER_COLORS[color] + '_get_legal_actions_opponent')
        if name is None:
            return None
        module = lookup("agents.opponent_actions", globals())
        return getattr(module, name)

    def get_successor_opponents(self, color: Color):
        self.check_is_parse()
        name = getattr(self._args, PLAYER_COLORS[color] + '_get_successor_opponents')
        if name is None:
            return None
        module = lookup("agents.opponent_actions", globals())
        return getattr(module, name)


def lookup(name, namespace):
    """
    Get a method or class from any imported module from its name.
    Usage: lookup(functionName, globals())
    """
    dots = name.count('.')
    if dots > 0:
        module_name, obj_name = '.'.join(name.split('.')[:-1]), name.split('.')[-1]
        module = __import__(module_name)
        return getattr(module, obj_name)
    else:
        modules = [obj for obj in namespace.values() if str(type(obj)) == "<type 'module'>"]
        options = [getattr(module, name) for module in modules if name in dir(module)]
        options += [obj[1] for obj in namespace.items() if obj[0] == name]
        if len(options) == 1: return options[0]
        if len(options) > 1: raise Exception('Name conflict for %s')
        raise Exception('%s not found as a method or class' % name)

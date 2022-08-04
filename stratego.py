from agents.alpha_beta_agent import AlphaBetaAgent
from agents.new_alpha_beta_agent import NewAlphaBetaAgent
from agents.human_agent import HumanAgent
from agents.init_agents.init_hill_climbing_agent import InitHillClimbingAgent
from agents.init_agents.init_human_agent import InitHumanAgent
from agents.init_agents.init_random_agent import InitRandomAgent
from agents.random_agent import RandomAgent
from game import StrategoGame
from graphics.console_graphic import ConsoleGraphic
from graphics.gui_graphic import GuiGraphic
from constants import Color
# from soldier import Color
from agents.init_agents.init_heuristics import *
from agents.opponent_actions import *
from agents.heuristics import *

if __name__ == '__main__':
    # graphic = ConsoleGraphic(10, 2)
    graphic = GuiGraphic(10, 2)
    red_agent = NewAlphaBetaAgent(Color.RED, graphic, InitRandomAgent(), depth=2,
                                  heuristic=min_soldiers_opp_heuristic, opponent_heuristic=min_soldiers_opp_heuristic,
                                  get_legal_actions_opponent=do_not_use_me_ever)
    # red_agent = RandomAgent(Color.RED, graphic)
    blue_agent = RandomAgent(Color.BLUE, graphic)
    game = StrategoGame(red_agent, blue_agent, graphic, True)
    score = game.run()

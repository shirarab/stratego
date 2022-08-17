import time
from datetime import datetime

from agents.alpha_beta_agent import AlphaBetaAgent
from agents.guessing_alpha_beta_agent import GuessingAlphaBetaAgent

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
    graphic = ConsoleGraphic(10, 0)
    # graphic = GuiGraphic(10, 2)
    # red_agent = AlphaBetaAgent(Color.RED, graphic, InitRandomAgent(), depth=2,
    #                            heuristic=sum_of_heuristics_heuristic,
    #                            opponent_heuristic=sum_of_heuristics_heuristic,
    #                            get_legal_actions_opponent=legal_actions_from_subset_guess,
    #                            get_successor_opponents=naive_opp_get_successor)
    red_agent = GuessingAlphaBetaAgent(Color.RED, graphic, InitRandomAgent(), depth=2,
                                       heuristic=sum_of_heuristics_heuristic,
                                       opponent_heuristic=min_opp_soldiers_num_heuristic,
                                       get_legal_actions_opponent=do_not_use_me_ever)
    # red_agent = RandomAgent(Color.RED, graphic)
    # blue_agent = RandomAgent(Color.BLUE, graphic)
    blue_agent = GuessingAlphaBetaAgent(Color.BLUE, graphic, InitRandomAgent(), depth=2,
                                        heuristic=min_opp_soldiers_num_heuristic,
                                        opponent_heuristic=sum_of_heuristics_heuristic,
                                        get_legal_actions_opponent=do_not_use_me_ever)

    num_games = 10
    for i in range(num_games):
        game = StrategoGame(red_agent, blue_agent, graphic, True)
        s_time = time.time()
        score, turn_count = game.run()
        e_time = time.time()
        print(f"Time: {e_time - s_time} sec, Turns: {turn_count}")

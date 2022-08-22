import time

from game import StrategoGame
from agents.heuristics import *
from agents.opponent_actions import *
from graphics.stratego_graphic import StrategoGraphic

from evaluate_score import num_soldiers_evaluator
from graphics.console_graphic import ConsoleGraphic
from graphics.gui_graphic import GuiGraphic

from agents.init_agents.init_random_agent import InitRandomAgent
from agents.init_agents.init_human_agent import InitHumanAgent
from agents.init_agents.init_hill_climbing_agent import InitHillClimbingAgent
from agents.init_agents.init_heuristics import *

from agents.random_agent import RandomAgent
from agents.human_agent import HumanAgent
from agents.alpha_beta_agent import AlphaBetaAgent
from agents.guessing_alpha_beta_agent import GuessingAlphaBetaAgent


def main():
    graphic = StrategoGraphic(BOARD_SIZE)
    red_agent = GuessingAlphaBetaAgent(Color.RED, graphic, InitHillClimbingAgent(init_flag_in_second_row_heuristic),
                                       heuristic=protect_flag_and_attack_heuristic,
                                       opponent_heuristic=null_heuristic, depth=2)
    blue_agent = HumanAgent(Color.BLUE, graphic, InitHillClimbingAgent(init_take_1_heuristic))
    # blue_agent = GuessingAlphaBetaAgent(Color.BLUE, graphic, InitHillClimbingAgent(init_take_1_heuristic),
    #                                     heuristic=min_opp_soldiers_num_heuristic,
    #                                     opponent_heuristic=min_opp_soldiers_num_heuristic, depth=2,
    #                                     get_legal_actions_opponent=legal_actions_from_subset_guess)
    # red_agent = RandomAgent(Color.RED, graphic)
    # blue_agent = RandomAgent(Color.BLUE, graphic)
    num_of_games = 10
    for i in range(num_of_games):
        # graphic = ConsoleGraphic(10, 1)
        graphic = GuiGraphic(10, 2)
        red_agent.graphic = graphic
        blue_agent.graphic = graphic
        game = StrategoGame(red_agent, blue_agent, graphic, weighted_num_soldiers_evaluator)
        s_time = time.time()
        score, turn_count = game.run()
        e_time = time.time()
        print(f"Time: {e_time - s_time} sec, Turns: {turn_count}")


if __name__ == '__main__':
    main()

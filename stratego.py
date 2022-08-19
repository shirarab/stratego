import time

from args_parser import ArgsParser
from game import StrategoGame
from agents.heuristics import *
from agents.opponent_actions import *
from graphics.stratego_graphic import StrategoGraphic


# from evaluate_score import evaluate_num_soldiers
# from graphics.console_graphic import ConsoleGraphic
# from graphics.gui_graphic import GuiGraphic
#
# from agents.init_agents.init_random_agent import InitRandomAgent
# from agents.init_agents.init_human_agent import InitHumanAgent
# from agents.init_agents.init_hill_climbing_agent import InitHillClimbingAgent
#
# from agents.random_agent import RandomAgent
# from agents.human_agent import HumanAgent
# from agents.alpha_beta_agent import AlphaBetaAgent
# from agents.guessing_alpha_beta_agent import GuessingAlphaBetaAgent


def main():
    my_parser = ArgsParser()
    my_parser.parse()
    graphic = StrategoGraphic(BOARD_SIZE)
    red_agent = my_parser.get_agent(Color.RED, graphic)
    blue_agent = my_parser.get_agent(Color.BLUE, graphic)
    evaluation_function = my_parser.get_evaluation_function()
    num_of_games = my_parser.get_num_of_games()
    for i in range(num_of_games):
        graphic = my_parser.get_graphic()
        red_agent.graphic = graphic
        blue_agent.graphic = graphic
        game = StrategoGame(red_agent, blue_agent, graphic, evaluation_function)
        s_time = time.time()
        score, turn_count = game.run()
        e_time = time.time()
        print(f"Time: {e_time - s_time} sec, Turns: {turn_count}")


if __name__ == '__main__':
    main()

"""
Possible Command Line Arguments:

empty console:
1. --display console --num_players_to_show 0
2. -g console -p 0

6 games:
1. --num_of_games 6
2. -n 6

evaluation function=evaluate_num_soldiers:
1. --evaluation_function evaluate_num_soldiers
2. -e evaluate_num_soldiers

red init hill climbing agent, init_take_1_heuristic:
1. --red_init_agent InitHillClimbingAgent --red_init_heuristic init_take_1_heuristic
2. -ria InitHillClimbingAgent -rih init_take_1_heuristic

blue alpha beta agent, random_heuristic, ...:
1. --blue_agent AlphaBetaAgent --blue_heuristic random_heuristic
2. -ba AlphaBetaAgent --bh random_heuristic
"""

"""
    # do not uncomment this!!!!!
    
    
    graphic = ConsoleGraphic(10, 1)
    graphic = GuiGraphic(10, 2)
    red_agent = AlphaBetaAgent(Color.RED, graphic, InitHillClimbingAgent(init_take_1_heuristic), depth=2,
                               heuristic=random_heuristic, opponent_heuristic=random_heuristic,
                               get_legal_actions_opponent=do_not_use_me_ever)
    red_agent = RandomAgent(Color.RED, graphic, InitHillClimbingAgent(init_take_1_heuristic))
    blue_agent = RandomAgent(Color.BLUE, graphic)
    game = StrategoGame(red_agent, blue_agent, graphic, evaluate_num_soldiers)
    score = game.run()
    # == == == =
    red_agent = AlphaBetaAgent(Color.RED, graphic, InitRandomAgent(), depth=2,
                               heuristic=sum_of_heuristics_heuristic,
                               opponent_heuristic=sum_of_heuristics_heuristic,
                               get_legal_actions_opponent=legal_actions_from_subset_guess,
                               get_successor_opponents=naive_opp_get_successor)
    red_agent = GuessingAlphaBetaAgent(Color.RED, graphic, InitRandomAgent(), depth=2,
                                       heuristic=sum_of_heuristics_heuristic,
                                       opponent_heuristic=min_opp_soldiers_num_heuristic,
                                       get_legal_actions_opponent=do_not_use_me_ever)
    red_agent = RandomAgent(Color.RED, graphic)
    blue_agent = RandomAgent(Color.BLUE, graphic)
    blue_agent = GuessingAlphaBetaAgent(Color.BLUE, graphic, InitRandomAgent(), depth=2,
                                        heuristic=min_opp_soldiers_num_heuristic,
                                        opponent_heuristic=sum_of_heuristics_heuristic,
                                        get_legal_actions_opponent=do_not_use_me_ever)
"""

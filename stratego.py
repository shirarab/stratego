import time

from args_parser import ArgsParser
from game import StrategoGame
from agents.heuristics import *
from agents.opponent_actions import *
from graphics.graphic import Graphic


def main():
    my_parser = ArgsParser()
    my_parser.parse()
    graphic = Graphic(BOARD_SIZE)
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
        print(f"Time: {e_time - s_time:.5f} sec, Turns: {turn_count}")


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
2. -ba AlphaBetaAgent -bh random_heuristic


interesting games:
1. -g gui -p 1 -ba RandomAgent -ra GuessingAlphaBetaAgent -rih init_take_1_heuristic -rh interesting_heuristic -d 1 -n 5
2. 
"""

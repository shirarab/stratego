import itertools
import time

from game import StrategoGame
from agents.heuristics import *
from agents.opponent_actions import *
from graphics.stratego_graphic import StrategoGraphic

from evaluate_score import *
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

SCORE_EVALUATORS = {
    "num soldiers evaluator": num_soldiers_evaluator,
    "weighted num soldiers evaluator": weighted_num_soldiers_evaluator,
    "naive unit count evaluator": naive_unit_count_evaluator,
    "flat naive unit count evaluator": flat_naive_unit_count_evaluator,
    "naive unit value count evaluator": naive_unit_value_count_evaluator,
    "jeroen mets evaluator": jeroen_mets_evaluator
}

EVALUATE_SCORE_AVG = {
    x: 0 for x in SCORE_EVALUATORS
}

TURNS = "turns"
TIME = "game duration"
GAME_MARATHON_SUMMARY = {
    Color.RED: 0,
    Color.BLUE: 0,
    TURNS: 0,
    TIME: 0
}

FOR_PRINT = {
    GuessingAlphaBetaAgent: "GuessingAlphaBetaAgent",
    RandomAgent: "RandomAgent",
    InitHillClimbingAgent: "InitHillClimbingAgent",
    InitRandomAgent: "InitRandomAgent",
    init_take_1_heuristic: "init_heuristic",
    min_opp_soldiers_num_heuristic: "min_opp_soldiers_num_heuristic",
    attack_opponent_heuristic: "attack_opponent_heuristic",
    max_me_min_opponent_heuristic: "max_me_min_opponent_heuristic",
    protect_flag_and_attack_heuristic: "protect_flag_and_attack_heuristic",
    random_heuristic: "random_heuristic"
}
AGENTS = [GuessingAlphaBetaAgent]
INIT_AGENTS = [InitHillClimbingAgent, InitRandomAgent]
INIT_HEURISTICS = [init_take_1_heuristic]
HEURISTICS = AGENT_HEURISTICS


# OP_HEURISTICS = AGENT_HEURISTICS.copy()
# OP_HEURISTICS.append(random_heuristic)


def main():
    f = open("evaluate_project.txt", "w")

    agent_combinations = list(
        itertools.product(AGENTS, INIT_AGENTS, INIT_HEURISTICS, AGENT_HEURISTICS))
    random_agent_combinations = list(itertools.product([RandomAgent], INIT_AGENTS, INIT_HEURISTICS, [random_heuristic]))
    all_combinations_for_one_agent = random_agent_combinations + agent_combinations
    all_combinations = list(itertools.combinations(all_combinations_for_one_agent, 2))
    graphic = StrategoGraphic(BOARD_SIZE)
    number_of_marathons = len(all_combinations) * 2 - (
            len(random_agent_combinations) * (len(random_agent_combinations) - 1)) / 2
    completed_marathons = 0
    print(f"---------------- {completed_marathons} / {number_of_marathons} ----------------")
    for i in range(len(all_combinations)):
        first_agent, second_agent = all_combinations[i]
        r_agent, r_init_agent, r_init_heuristic, r_heuristic = first_agent
        b_agent, b_init_agent, b_init_heuristic, b_heuristic = second_agent

        r_op_heuristic = [b_heuristic, random_heuristic]
        b_op_heuristic = [r_heuristic, random_heuristic]
        if b_heuristic == random_heuristic and r_heuristic == random_heuristic:
            r_op_heuristic = [random_heuristic]
            b_op_heuristic = [random_heuristic]
        for op_heuristic_index in range(len(r_op_heuristic)):
            red_agent = r_agent(color=Color.RED, graphic=graphic, init_agent=r_init_agent(r_init_heuristic),
                                heuristic=r_heuristic,
                                opponent_heuristic=r_op_heuristic[op_heuristic_index], depth=2)
            blue_agent = b_agent(color=Color.BLUE, graphic=graphic, init_agent=b_init_agent(b_init_heuristic),
                                 heuristic=b_heuristic,
                                 opponent_heuristic=b_op_heuristic[op_heuristic_index], depth=2)
            num_of_games = 10
            evaluate_score_avg = EVALUATE_SCORE_AVG.copy()
            game_marathon_summary = GAME_MARATHON_SUMMARY.copy()
            for j in range(num_of_games):
                graphic = ConsoleGraphic(10, 0)
                red_agent.graphic = graphic
                blue_agent.graphic = graphic
                game = StrategoGame(red_agent, blue_agent, graphic, weighted_num_soldiers_evaluator)
                s_time = time.time()
                score, turn_count = game.run()
                e_time = time.time()
                duration = e_time - s_time
                game_marathon_summary[game.state.winner] += 1
                game_marathon_summary[TURNS] += float(turn_count) / num_of_games
                game_marathon_summary[TIME] += float(duration) / num_of_games

                for evaluator in SCORE_EVALUATORS:
                    evaluate_score_avg[evaluator] += float(SCORE_EVALUATORS[evaluator](game.state, Color.RED,
                                                                                       red_agent=red_agent,
                                                                                       blue_agent=blue_agent)) / num_of_games

            f.write(
                f"{FOR_PRINT[r_agent]} with : init agent - {FOR_PRINT[r_init_agent]} with {FOR_PRINT[r_init_heuristic]},\nplay heuristic - {FOR_PRINT[r_heuristic]}, guessed opponent heuristic - {FOR_PRINT[r_op_heuristic[op_heuristic_index]]}\n")
            f.write(" against \n")
            f.write(
                f"{FOR_PRINT[b_agent]} with : init agent - {FOR_PRINT[b_init_agent]} with {FOR_PRINT[b_init_heuristic]},\nplay heuristic - {FOR_PRINT[b_heuristic]}, guessed opponent heuristic - {FOR_PRINT[b_op_heuristic[op_heuristic_index]]}\n")
            f.write(f"In {num_of_games} games:\n - player {Color.RED} won {game_marathon_summary[Color.RED]} games\n")
            f.write(f" - player {Color.BLUE} won {game_marathon_summary[Color.BLUE]} games\n")
            f.write(f" - the average number of {TURNS} in a game was {game_marathon_summary[TURNS]}\n")
            f.write(f" - the average {TIME} in a game was {game_marathon_summary[TIME]}\n")
            for evaluator in evaluate_score_avg:
                f.write(f" - the average {evaluator} : {evaluate_score_avg[evaluator]}\n")
            f.write("\n")
            completed_marathons += 1
            print(f"---------------- {completed_marathons} / {number_of_marathons} ----------------")
            if completed_marathons > 1:
                break
        if completed_marathons > 1:
            break
    f.close()


if __name__ == '__main__':
    main()

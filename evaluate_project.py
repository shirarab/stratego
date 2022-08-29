import itertools
import time

from game import StrategoGame
from agents.heuristics import *
from agents.opponent_actions import *
from graphics.graphic import Graphic

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
import xlwt
from xlwt import Workbook

SCORE_EVALUATORS = {
    "NUM SOLDIERS EVALUATOR": num_soldiers_evaluator,
    "WEIGHTED NUM SOLDIERS EVALUATOR": weighted_num_soldiers_evaluator,
    "NAIVE UNIT COUNT EVALUATOR": naive_unit_count_evaluator,
    "FLAT NAIVE UNIT COUNT EVALUATOR": flat_naive_unit_count_evaluator,
    "NAIVE UNIT VALUE EVALUATOR": naive_unit_value_count_evaluator,
    "JEROEN METS EVALUATOR": jeroen_mets_evaluator
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
    AlphaBetaAgent: "AlphaBetaAgent",
    RandomAgent: "RandomAgent",
    InitHillClimbingAgent: "InitHillClimbingAgent",
    InitRandomAgent: "InitRandomAgent",
    init_take_2_heuristic: "init_heuristic",
    min_opp_soldiers_num_heuristic: "min_opp_soldiers_num_heuristic",
    attack_opponent_heuristic: "attack_opponent_heuristic",
    max_me_min_opponent_heuristic: "max_me_min_opponent_heuristic",
    protect_flag_and_attack_heuristic: "protect_flag_and_attack_heuristic",
    better_num_soldiers_difference_heuristic: "better_num_soldiers_difference_heuristic",
    random_heuristic: "random_heuristic"
}
INIT_AGENTS = [InitHillClimbingAgent, InitRandomAgent]
INIT_HEURISTICS = [init_take_2_heuristic]
GUESSING_AGENT_HEURISTICS = [attack_opponent_heuristic, max_me_min_opponent_heuristic,
                             protect_flag_and_attack_heuristic]
ALPHA_BETA_AGENT_HEURISTICS = [attack_opponent_heuristic, better_num_soldiers_difference_heuristic]
DEPTH = [2]


# OP_HEURISTICS = AGENT_HEURISTICS.copy()
# OP_HEURISTICS.append(random_heuristic)

def create_excel():
    wb = Workbook()
    sheet = wb.add_sheet('evaluate project')
    style_red = xlwt.easyxf('font: name Arial, bold 1, color dark_red;')
    style_blue = xlwt.easyxf('font: name Arial, bold 1, color dark_blue;')
    style_black = xlwt.easyxf('font: name Arial, bold 1, color black;')
    sheet.write(1, 0, 'RED AGENT', style_red)
    sheet.write(2, 0, 'RED INIT AGENT', style_red)
    sheet.write(3, 0, 'RED INIT HEURISTIC', style_red)
    sheet.write(4, 0, 'RED PLAY HEURISTIC', style_red)
    sheet.write(5, 0, 'RED GUESSED OP HEURISTIC', style_red)
    sheet.write(6, 0, 'BLUE AGENT', style_blue)
    sheet.write(7, 0, 'BLUE INIT AGENT', style_blue)
    sheet.write(8, 0, 'BLUE INIT HEURISTIC', style_blue)
    sheet.write(9, 0, 'BLUE PLAY HEURISTIC', style_blue)
    sheet.write(10, 0, 'BLUE GUESSED OP HEURISTIC', style_blue)
    sheet.write(11, 0, 'RED WON', style_red)
    sheet.write(12, 0, 'BLUE WON', style_blue)
    sheet.write(13, 0, 'AVG TURN NUMBER', style_black)
    sheet.write(14, 0, 'AVG GAME DURATION (SECONDS)', style_black)
    i = 15
    for ev in SCORE_EVALUATORS:
        sheet.write(i, 0, 'AVG ' + ev + '- RED', style_red)
        i += 1
    for ev in SCORE_EVALUATORS:
        sheet.write(i, 0, 'AVG ' + ev + '- BLUE', style_blue)
        i += 1
    wb.save('evaluate project.xls')
    return sheet, wb, style_red, style_blue, style_black


def main():
    sheet, wb, style_red, style_blue, style_black = create_excel()
    # f = open("evaluate_project.txt", "w")
    guessing_agent_combinations = list(
        itertools.product([GuessingAlphaBetaAgent], INIT_AGENTS, INIT_HEURISTICS, GUESSING_AGENT_HEURISTICS, DEPTH))
    alpha_beta_agent_combinations = list(
        itertools.product([AlphaBetaAgent], INIT_AGENTS, INIT_HEURISTICS, ALPHA_BETA_AGENT_HEURISTICS, DEPTH))
    random_agent_combinations = list(
        itertools.product([RandomAgent], INIT_AGENTS, INIT_HEURISTICS, [random_heuristic], [1]))
    all_combinations_for_one_agent = random_agent_combinations + guessing_agent_combinations
    all_combinations_for_one_agent += alpha_beta_agent_combinations
    all_combinations = list(itertools.combinations(all_combinations_for_one_agent, 2))
    graphic = Graphic(BOARD_SIZE)
    number_of_marathons = len(all_combinations) * 2 - (
            len(random_agent_combinations) * (len(random_agent_combinations) - 1)) / 2 - len(
        random_agent_combinations) * (len(guessing_agent_combinations) + len(alpha_beta_agent_combinations))
    completed_marathons = 0
    col = 1
    print(f"---------------- {completed_marathons} / {number_of_marathons} ----------------")
    start_index = max(3, 0)
    last_index = min(6, len(all_combinations) - 1)
    for k in range(start_index, last_index + 1):
        first_agent, second_agent = all_combinations[k]
        r_agent, r_init_agent, r_init_heuristic, r_heuristic, r_depth = first_agent
        b_agent, b_init_agent, b_init_heuristic, b_heuristic, b_depth = second_agent

        r_op_heuristic = [b_heuristic, random_heuristic]
        b_op_heuristic = [r_heuristic, random_heuristic]
        if r_agent == RandomAgent or b_agent == RandomAgent:
            r_op_heuristic = [b_heuristic]
            b_op_heuristic = [r_heuristic]
        for op_heuristic_index in range(len(r_op_heuristic)):
            red_agent = r_agent(color=Color.RED, graphic=graphic, init_agent=r_init_agent(r_init_heuristic),
                                heuristic=r_heuristic,
                                opponent_heuristic=r_op_heuristic[op_heuristic_index], depth=r_depth)
            blue_agent = b_agent(color=Color.BLUE, graphic=graphic, init_agent=b_init_agent(b_init_heuristic),
                                 heuristic=b_heuristic,
                                 opponent_heuristic=b_op_heuristic[op_heuristic_index], depth=b_depth)
            num_of_games = 10 if r_agent != RandomAgent or b_agent != RandomAgent else 30
            evaluate_score_avg_red = EVALUATE_SCORE_AVG.copy()
            evaluate_score_avg_blue = EVALUATE_SCORE_AVG.copy()
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
                    evaluate_score_avg_red[evaluator] += float(SCORE_EVALUATORS[evaluator](game.state, Color.RED,
                                                                                           red_agent=red_agent,
                                                                                           blue_agent=blue_agent)) / num_of_games
                    evaluate_score_avg_blue[evaluator] += float(SCORE_EVALUATORS[evaluator](game.state, Color.BLUE,
                                                                                            red_agent=red_agent,
                                                                                            blue_agent=blue_agent)) / num_of_games
            col_ = start_index + op_heuristic_index
            sheet.write(0, col, col_, style_black)
            sheet.write(1, col, FOR_PRINT[r_agent], style_red)
            sheet.write(2, col, FOR_PRINT[r_init_agent], style_red)
            sheet.write(3, col, FOR_PRINT[r_init_heuristic], style_red)
            sheet.write(4, col, FOR_PRINT[r_heuristic], style_red)
            sheet.write(5, col, FOR_PRINT[r_op_heuristic[op_heuristic_index]], style_red)
            sheet.write(6, col, FOR_PRINT[b_agent], style_blue)
            sheet.write(7, col, FOR_PRINT[b_init_agent], style_blue)
            sheet.write(8, col, FOR_PRINT[b_init_heuristic], style_blue)
            sheet.write(9, col, FOR_PRINT[b_heuristic], style_blue)
            sheet.write(10, col, FOR_PRINT[b_op_heuristic[op_heuristic_index]], style_blue)
            sheet.write(11, col, game_marathon_summary[Color.RED], style_red)
            sheet.write(12, col, game_marathon_summary[Color.BLUE], style_blue)
            sheet.write(13, col, game_marathon_summary[TURNS], style_black)
            sheet.write(14, col, game_marathon_summary[TIME], style_black)
            i = 15
            for ev in SCORE_EVALUATORS:
                sheet.write(i, col, evaluate_score_avg_red[ev], style_red)
                i += 1
            for ev in SCORE_EVALUATORS:
                sheet.write(i, col, evaluate_score_avg_blue[ev], style_blue)
                i += 1
            col += 1
            wb.save('evaluate project.xls')
            # f.write(
            #     f"{FOR_PRINT[r_agent]} with : init agent - {FOR_PRINT[r_init_agent]} with {FOR_PRINT[r_init_heuristic]},\nplay heuristic - {FOR_PRINT[r_heuristic]}, guessed opponent heuristic - {FOR_PRINT[r_op_heuristic[op_heuristic_index]]}\n")
            # f.write(" against \n")
            # f.write(
            #     f"{FOR_PRINT[b_agent]} with : init agent - {FOR_PRINT[b_init_agent]} with {FOR_PRINT[b_init_heuristic]},\nplay heuristic - {FOR_PRINT[b_heuristic]}, guessed opponent heuristic - {FOR_PRINT[b_op_heuristic[op_heuristic_index]]}\n")
            # f.write(f"In {num_of_games} games:\n - player {Color.RED} won {game_marathon_summary[Color.RED]} games\n")
            # f.write(f" - player {Color.BLUE} won {game_marathon_summary[Color.BLUE]} games\n")
            # f.write(f" - the average number of {TURNS} in a game was {game_marathon_summary[TURNS]}\n")
            # f.write(f" - the average {TIME} in a game was {game_marathon_summary[TIME]}\n")
            # for evaluator in evaluate_score_avg:
            #     f.write(f" - the average {evaluator} : {evaluate_score_avg[evaluator]}\n")
            # f.write("\n")
            completed_marathons += 1
            print(f"---------------- {completed_marathons} / {number_of_marathons} ----------------")
        #     if completed_marathons > 0:
        #         break
        # if completed_marathons > 0:
        #     break
    wb.save('evaluate project.xls')
    # f.close()


if __name__ == '__main__':
    main()

# import itertools
# from copy import deepcopy
from constants import SOLDIER_COUNT_FOR_EACH_DEGREE, Degree, BOARD_SIZE, OP_COLOR
from soldier import Soldier
from agents.agent import Agent
from action import Action
from collections import Counter
# import numpy as np
import random

from agents.init_agents.init_agent import InitAgent
# from agents.init_agents.init_random_agent import InitRandomAgent
from game_state import GameState
from graphics.stratego_graphic import StrategoGraphic
from constants import Color
# from soldier import Color
from agents.heuristics import null_heuristic
from agents.opponent_actions import null_get_legal_actions_opponent, null_get_successor_opponent


class GuessingAlphaBetaAgent(Agent):
    def __init__(self, color, graphic: StrategoGraphic, init_agent: InitAgent,
                 heuristic=null_heuristic, opponent_heuristic=null_heuristic, depth: int = 1,
                 get_legal_actions_opponent=null_get_legal_actions_opponent,
                 get_successor_opponents=null_get_successor_opponent):
        super().__init__(color, graphic, init_agent, heuristic, opponent_heuristic, depth)
        self._get_legal_actions_opponent = get_legal_actions_opponent
        self._get_successor_opponent = get_successor_opponents
        self._stored_by_depth = {}
        self.op_color = Color.RED if self.color == Color.BLUE else Color.BLUE

    def get_action(self, game_state: GameState) -> Action:
        if random.randint(1, 100) >= 95:
            legal_actions = game_state.get_legal_actions(self.color)
            return random.sample(legal_actions, 1)[0]
        self.store_alpha_beta(game_state, self.depth + 1, self.color)
        guessed_game_state = self.guessing_opponent_soldiers(game_state)
        val, action = self.alpha_beta(-float("inf"), float("inf"), guessed_game_state, self.depth, True)
        action = Action(game_state.get_soldier_at_x_y(action.soldier.x, action.soldier.y), action.direction,
                        action.num_steps)
        self.restore_alpha_beta(game_state, self.depth + 1, self.color)
        return action

    def get_initial_positions(self):
        return self.init_agent.get_initial_positions(self.soldiers, self.graphic)

    def store_alpha_beta(self, game_state: GameState, depth, color):
        self._stored_by_depth[(depth, color)] = game_state.store()

    def restore_alpha_beta(self, game_state: GameState, depth, color):
        game_state.restore(self._stored_by_depth[(depth, color)])

    def guessing_opponent_soldiers(self, game_state: GameState):
        op_color = OP_COLOR[self.color]
        game_state.get_knowledge_base(op_color).update(game_state)
        num_soldiers_opponent = Counter(SOLDIER_COUNT_FOR_EACH_DEGREE.copy())
        num_dead_soldiers_opponent = Counter(game_state.dead[op_color].copy())
        num_soldiers_opponent_on_board = num_soldiers_opponent - num_dead_soldiers_opponent

        board = [[Soldier(Degree.EMPTY, i, j, Color.GRAY) for j in range(BOARD_SIZE)]
                 for i in range(BOARD_SIZE)]
        for i in range(2):
            for j in range(BOARD_SIZE):
                if j in {2, 3, 6, 7}:
                    board[4 + i][j] = Soldier(Degree.WATER, 4 + i, j, Color.WATER)
        can_op_soldier_be_flag = {}
        my_knowledge_base = game_state.get_knowledge_base(self.color)
        opp_soldiers = []
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                soldier_info = game_state.board[i][j]
                if soldier_info.color == op_color:
                    opp_soldiers.append([soldier_info,
                                         game_state.get_knowledge_base(op_color).option_count_for_soldier(
                                             soldier_info)])
                if soldier_info.color == self.color:
                    board[i][j] = Soldier(soldier_info.degree, i, j, self.color)
                    my_options = my_knowledge_base.get_options_for_soldier(soldier_info)
                    can_op_soldier_be_flag[board[i][j]] = True if Degree.FLAG in my_options else False

        # random.shuffle(opp_soldiers)
        opp_soldiers.sort(key=lambda x: x[1])
        opp_knowledge_base = game_state.get_knowledge_base(op_color)
        options = [opp_knowledge_base.get_options_for_soldier(opp_soldiers[index][0]) for index in range(len(opp_soldiers))]
        for i in range(len(options)):
            random.shuffle(options[i])
        degree_opp = self.find_degree_for_opp_soldiers(game_state, opp_soldiers, [], num_soldiers_opponent_on_board, 0,
                                                       op_color, options)

        for i in range(len(opp_soldiers)):
            soldier = opp_soldiers[i][0]
            board[soldier.x][soldier.y] = Soldier(degree_opp[i], soldier.x, soldier.y, op_color)
            can_op_soldier_be_flag[board[soldier.x][soldier.y]] = True if Degree.FLAG in options[i] else False

        dead = {Color.RED: game_state.dead[Color.RED].copy(), Color.BLUE: game_state.dead[Color.BLUE].copy()}
        # kb_info = {color: game_state.get_knowledge_base(color).store_kb() for color in OP_COLOR}
        return GameState(board, game_state.score, game_state.done, dead, None, can_op_soldier_be_flag)

    def find_degree_for_opp_soldiers(self, game_state, opp_soldiers, degree, num_soldiers_opponent_on_board, index,
                                     op_color, options):
        if index == len(opp_soldiers):
            return degree
        # options = game_state._soldier_knowledge_base[op_color][opp_soldiers[index][0]].copy()
        # options = opp_knowledge_base.get_options_for_soldier(opp_soldiers[index][0])

        # random.shuffle(options)
        for i in options[index]:
            if num_soldiers_opponent_on_board[i] > 0:
                degree.append(i)
                num_soldiers_opponent_on_board[i] -= 1
                return_val = self.find_degree_for_opp_soldiers(game_state, opp_soldiers, degree,
                                                               num_soldiers_opponent_on_board, index + 1, op_color, options)
                if return_val is not None:
                    degree = return_val
                    return degree
                degree.pop(index)
                num_soldiers_opponent_on_board[i] += 1

        return None

    def alpha_beta(self, alpha, beta, game_state: GameState, depth, is_max_node):
        if is_max_node:
            if depth == 0:
                return self.heuristic(game_state, self.color), None
            legal_actions = game_state.get_legal_actions(self.color)
            if not legal_actions:
                return self.heuristic(game_state, self.color), None
            max_action = None
            self.store_alpha_beta(game_state, depth, self.color)
            for action in legal_actions:
                # self.store_alpha_beta(game_state, depth, self.color)
                board = game_state.get_successor(action)
                new_alpha = self.alpha_beta(alpha, beta, game_state, depth, False)[0]
                self.restore_alpha_beta(board, depth, self.color)
                if new_alpha > alpha:
                    max_action = action
                    alpha = new_alpha
                if alpha >= beta:
                    break
            return alpha, max_action
        else:
            if depth == 0:
                return self.opponent_heuristic(game_state, self.op_color), None
            legal_actions = game_state.get_legal_actions(self.op_color)
            if not legal_actions:
                return self.opponent_heuristic(game_state, self.op_color), None
            min_action = None
            self.store_alpha_beta(game_state, depth, self.op_color)
            for action in legal_actions:
                # self.store_alpha_beta(game_state, depth, op_color)
                board = self._get_successor_opponent(game_state, action, self.op_color)
                new_beta = self.alpha_beta(alpha, beta, game_state, depth - 1, True)[0]
                self.restore_alpha_beta(board, depth, self.op_color)
                if new_beta < beta:
                    min_action = action
                    beta = new_beta
                if alpha >= beta:
                    break
            return beta, min_action

import itertools
from copy import deepcopy
from constants import NUM_OF_PLAYER_DEGREE_SOLDIERS, Degree, BOARD_SIZE, OP_COLOR
from soldier import Soldier
from agents.agent import Agent
from action import Action
from collections import Counter
import numpy as np
import random

from agents.init_agents.init_agent import InitAgent
from agents.init_agents.init_random_agent import InitRandomAgent
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

    def get_action(self, game_state: GameState) -> Action:
        self.store_alpha_beta(game_state, self.depth + 1, self.color)
        guessed_game_state = self.guessing_opponent_soldiers(game_state)
        val, action = self.alpha_beta(-float("inf"), float("inf"), guessed_game_state, self.depth, True)
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
        game_state.update_knowledge_base(op_color)
        num_soldiers_opponent = Counter(NUM_OF_PLAYER_DEGREE_SOLDIERS.copy())
        num_dead_soldiers_opponent = Counter(game_state.dead[op_color].copy())
        num_soldiers_opponent_on_board = num_soldiers_opponent - num_dead_soldiers_opponent

        board = [[Soldier(Degree.EMPTY, i, j, Color.GRAY) for j in range(BOARD_SIZE)]
                 for i in range(BOARD_SIZE)]
        for i in range(2):
            for j in range(BOARD_SIZE):
                if j in {2, 3, 6, 7}:
                    board[4 + i][j] = Soldier(Degree.WATER, 4 + i, j, Color.WATER)
        list_indexes = list(range(BOARD_SIZE))
        pairs_i_j = list(itertools.product(list_indexes, list_indexes))
        random.shuffle(pairs_i_j)
        opp_soldiers = []
        for i, j in pairs_i_j:
            soldier_info = game_state.board[i][j]
            if soldier_info.color == op_color:
                opp_soldiers.append(soldier_info)
            if soldier_info.color == self.color:
                board[i][j] = Soldier(soldier_info.degree, i, j, self.color)
        degree_opp = self.find_degree_for_opp_soldiers(game_state, opp_soldiers, [], num_soldiers_opponent_on_board, 0,
                                                       op_color)
        for i in range(len(opp_soldiers)):
            soldier = opp_soldiers[i]
            board[soldier.x][soldier.y] = Soldier(degree_opp[i], soldier.x, soldier.y, op_color)

        dead = {Color.RED: game_state.dead[Color.RED].copy(), Color.BLUE: game_state.dead[Color.BLUE].copy()}
        return GameState(board, game_state.score, game_state.done, dead)

    def find_degree_for_opp_soldiers(self, game_state, opp_soldiers, degree, num_soldiers_opponent_on_board, index,
                                     op_color):
        if index == len(opp_soldiers):
            return degree
        options = game_state.soldier_knowledge_base[op_color][opp_soldiers[index]].copy()
        random.shuffle(options)
        for i in options:
            if num_soldiers_opponent_on_board[i] > 0:
                degree.append(i)
                num_soldiers_opponent_on_board[i] -= 1
                return_val = self.find_degree_for_opp_soldiers(game_state, opp_soldiers, degree,
                                                               num_soldiers_opponent_on_board, index + 1,op_color)
                if return_val is not None:
                    degree = return_val
                    return degree
                degree.pop(index)
                num_soldiers_opponent_on_board[i] += 1

        return None

    def alpha_beta(self, alpha, beta, game_state: GameState, depth, is_max_node):
        if is_max_node:
            legal_actions = game_state.get_legal_actions(self.color)
            if depth == 0 or not legal_actions:
                return self.heuristic(game_state, self.color), None
            max_action = None
            for action in legal_actions:
                self.store_alpha_beta(game_state, depth, self.color)
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
            op_color = Color.RED if self.color == Color.BLUE else Color.BLUE
            legal_actions = game_state.get_legal_actions(op_color)
            if depth == 0 or not legal_actions:
                return self.opponent_heuristic(game_state, op_color), None
            min_action = None
            for action in legal_actions:
                self.store_alpha_beta(game_state, depth, op_color)
                board = self._get_successor_opponent(game_state, action, op_color)
                new_beta = self.alpha_beta(alpha, beta, game_state, depth - 1, True)[0]
                self.restore_alpha_beta(board, depth, op_color)
                if new_beta < beta:
                    min_action = action
                    beta = new_beta
                if alpha >= beta:
                    break
            return beta, min_action

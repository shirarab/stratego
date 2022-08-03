from copy import deepcopy

from agents.agent import Agent
from action import Action
import random

from agents.init_agents.init_agent import InitAgent
from agents.init_agents.init_random_agent import InitRandomAgent
from game_state import GameState
from graphics.stratego_graphic import StrategoGraphic
from constants import Color
# from soldier import Color
from agents.heuristics import null_heuristic
from agents.opponent_actions import null_get_legal_actions_opponent, null_get_successor_opponent


class AlphaBetaAgent(Agent):
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
        val, action = self.alpha_beta(-float("inf"), float("inf"), game_state, self.depth, True)
        self.restore_alpha_beta(game_state, self.depth + 1, self.color)
        return action

    def get_initial_positions(self):
        return self.init_agent.get_initial_positions(self.soldiers, self.graphic)

    def store_alpha_beta(self, game_state: GameState, depth, color):
        self._stored_by_depth[(depth, color)] = game_state.store()

    def restore_alpha_beta(self, game_state: GameState, depth, color):
        game_state.restore(self._stored_by_depth[(depth, color)])

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
            legal_actions = self._get_legal_actions_opponent(game_state, op_color)
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

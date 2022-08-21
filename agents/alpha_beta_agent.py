from copy import deepcopy

from agents.agent import Agent
from action import Action
import random

from agents.init_agents.init_agent import InitAgent
from agents.init_agents.init_random_agent import InitRandomAgent
from game_state import GameState
from graphics.stratego_graphic import StrategoGraphic
from constants import Color, Degree, Direction, OP_COLOR
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
        self.op_color = OP_COLOR[color]

    def get_action(self, game_state: GameState) -> Action:
        if random.randint(1, 100) >= 90:
            legal_actions = game_state.get_legal_actions(self.color)
            if len(legal_actions) == 0:
                return None
            rand_action = random.sample(legal_actions, 1)[0]
            new_legal_action = set()
            for action in legal_actions:
                soldier = self.find_opp_soldier_we_revealed(action, game_state)
                if soldier is not None and \
                        (soldier.degree == Degree.BOMB or soldier.degree > action.soldier.degree):
                    continue
                new_legal_action.add(action)
            if len(new_legal_action) == 0:
                return rand_action
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
            op_color = Color.RED if self.color == Color.BLUE else Color.BLUE
            legal_actions = self._get_legal_actions_opponent(game_state, op_color)
            if depth == 0 or not legal_actions:
                return self.opponent_heuristic(game_state, op_color), None
            min_action = None
            self.store_alpha_beta(game_state, depth, op_color)
            for action in legal_actions:
                # self.store_alpha_beta(game_state, depth, op_color)
                board = self._get_successor_opponent(game_state, action, op_color)
                new_beta = self.alpha_beta(alpha, beta, game_state, depth - 1, True)[0]
                self.restore_alpha_beta(board, depth, op_color)
                if new_beta < beta:
                    min_action = action
                    beta = new_beta
                if alpha >= beta:
                    break
            return beta, min_action

    def find_opp_soldier_we_revealed(self, action: Action, game_state: GameState):
        sol_x = action.soldier.x
        sol_y = action.soldier.y
        op_x = sol_x
        op_y = sol_y
        if action.direction == Direction.UP:
            op_x += action.num_steps
        if action.direction == Direction.DOWN:
            op_x -= action.num_steps
        if action.direction == Direction.RIGHT:
            op_y += action.num_steps
        if action.direction == Direction.LEFT:
            op_y -= action.num_steps
        opponent = game_state.get_soldier_at_x_y(op_x, op_y)
        if (opponent.color == self.op_color and action.soldier.color == self.color) or (
                opponent.color == self.color and action.soldier.color == self.op_color):
            return opponent

        return None

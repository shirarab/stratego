# from agents.agent import Agent
# from action import Action
# import random
#
# from agents.init_agents.init_agent import InitAgent
# from agents.init_agents.init_random_agent import InitRandomAgent
# from game_state import GameState
# from graphics.stratego_graphic import StrategoGraphic
#
#
# class AlphaBetaAgent(Agent):
#     def get_action(self, game_state: GameState) -> Action:
#         return self.alpha_beta(-float("inf"), float("inf"), game_state, self.depth, True)[1]
# 
#     def get_initial_positions(self):
#         return self.init_agent.get_initial_positions(self.soldiers, self.graphic)
#
#     def alpha_beta(self, alpha, beta, game_state: GameState, depth, is_max_node):
#         if is_max_node:
#             legal_actions = game_state.get_legal_actions(self.color)
#             if depth == 0 or not legal_actions:
#                 return self.heuristic(game_state), None
#             max_action = None
#             for action in legal_actions:
#                 board = game_state.apply_action(action) ####!!!!!!!!!!!!!!!!!!!!
#                 new_alpha = self.alpha_beta(alpha, beta, board, depth, False)[0]
#                 if new_alpha > alpha:
#                     max_action = action
#                     alpha = new_alpha
#                 if alpha >= beta:
#                     break
#             return alpha, max_action
#         else:
#
#             legal_actions = game_state.get_legal_actions()
#             if depth == 0 or not legal_actions:
#                 return self.heuristic(game_state), None #######!!!!!!!!!!!!!!!!!!!!
#             min_action = None
#             for action in legal_actions:
#                 board = game_state.apply_action(action) #######!!!!!!!!!!!!!!!!!
#                 new_beta = self.alpha_beta(alpha, beta, board, depth - 1, True)[0]
#                 if new_beta < beta:
#                     min_action = action
#                     beta = new_beta
#                 if alpha >= beta:
#                     break
#             return beta, min_action

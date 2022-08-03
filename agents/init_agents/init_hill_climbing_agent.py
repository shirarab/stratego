from typing import Set

from agents.init_agents.init_agent import InitAgent
from graphics.stratego_graphic import StrategoGraphic
from search.init_search_problem import InitSearchProblem
from search.search_problem import SearchProblem
from constants import Color
from soldier import Soldier#, Color


class InitHillClimbingAgent(InitAgent):
    def get_initial_positions(self, soldiers: Set[Soldier],
                              graphic: StrategoGraphic, color: Color = None):
        board = self.get_initial_random_board(soldiers)
        init_search_p = InitSearchProblem(board)
        current_b = init_search_p.get_start_state()
        current_v = self.heuristic(current_b)
        while True:
            successors = init_search_p.get_successors(current_b)
            max_neighbor = current_b
            max_value = current_v
            for s in successors:
                if self.heuristic(s) > max_value:
                    max_value = self.heuristic(s)
                    max_neighbor = s
            if max_value == current_v:
                break
            current_b = max_neighbor
            current_v = max_value
        return current_b

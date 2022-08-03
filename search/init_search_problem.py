from typing import List
from itertools import combinations

from search.search_problem import SearchProblem
from soldier import Soldier


class InitSearchProblem(SearchProblem):
    def __init__(self, board: List[List[Soldier]]):
        self._board = board
        self._reset_successors()

    def get_start_state(self):
        return self._board

    def is_goal_state(self, state):
        return True

    def _reset_successors(self):
        self._successors = ((x, y) for y in range(10) for x in range(4))
        self._successors = combinations(self._successors, 2)

    def get_successors(self, board: List[List[Soldier]]):
        for first, second in self._successors:
            f_soldier = board[first[0]][first[1]]
            s_soldier = board[second[0]][second[1]]
            new_b = [[board[i][j] for j in range(10)] for i in range(4)]
            new_b[first[0]][first[1]] = s_soldier
            new_b[second[0]][second[1]] = f_soldier
            yield new_b
        self._reset_successors()
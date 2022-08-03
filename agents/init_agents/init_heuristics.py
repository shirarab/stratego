from typing import List

from constants import Degree
# from degree import Degree
from soldier import Soldier


def init_null_heuristic(board: List[List[Soldier]]):
    return 0


def init_try_heuristic(board: List[List[Soldier]]):
    val = 0
    for j in range(10):
        if board[0][j].degree == Degree.TWO:
            val += 10
    return val
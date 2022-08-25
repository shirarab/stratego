from typing import List

from constants import Degree
# from degree import Degree
from soldier import Soldier


REGULARIZATION = 10

def init_null_heuristic(board: List[List[Soldier]]) -> int:
    return 0


def init_try_heuristic(board: List[List[Soldier]]):
    val = 0
    for j in range(10):
        if board[0][j].degree == Degree.TWO:
            val += 10
    return val


def next_to(i, j, degree: Degree, board: List[List[Soldier]]):
    if (j+1 < len(board[i])) and board[i][j+1].degree == degree:
        return True
    if (j-1 >= 0) and board[i][j-1].degree == degree:
        return True
    if (i+1 < len(board)) and board[i+1][j].degree == degree:
        return True
    if (i-1 >= 0) and board[i-1][j].degree == degree:
        return True
    return False


def average_degree_val(i_first, j_first, i_second, j_second, board: List[List[Soldier]]):
    if i_first < 0 or j_first < 0 or i_second < 0 or j_second < 0:
        return -1
    if i_first >= len(board) or j_first >= len(board[i_first]) or\
            i_second >= len(board) or j_second >= len(board[i_second]):
        return -1
    if i_first > i_second:
        temp = i_first
        i_first = i_second
        i_second = temp
    if j_first > j_second:
        temp = j_first
        j_first = j_second
        j_second = temp
    num_of_sol = 0
    val = 0
    for i in range(i_first, i_second+1):
        for j in range(j_first, j_second+1):
            num_of_sol += 1
            val += board[i][j].degree
    return val / num_of_sol


def init_flag_in_second_row_heuristic(board: List[List[Soldier]]):
    for j in range(10):
        if board[2][j].degree == Degree.FLAG:
            return 10
    return 0


def init_take_1_heuristic(board: List[List[Soldier]]):
    val = 0
    for i in range(len(board)):
        for j in range(len(board[i])):
            soldier = board[i][j]
            if soldier.degree == Degree.FLAG and i == 0:
                val += 100
            if soldier.degree == Degree.BOMB and next_to(i, j, Degree.FLAG, board):
                val += 1000
            if soldier.degree == Degree.ONE and i == len(board)-1:
                val -= 5
    avg_left = average_degree_val(0, 0, 3, 2, board)
    avg_middle = average_degree_val(0, 3, 3, 6, board)
    avg_right = average_degree_val(0, 7, 3, 9, board)
    if avg_left == avg_middle == avg_right:
        val += 1500
    elif avg_left == avg_middle:
        val += 500 \
               + (1/(abs(avg_middle - avg_right)))*REGULARIZATION\
               + (1 / (abs(avg_right - avg_left)))*REGULARIZATION
    elif avg_middle == avg_right:
        val += 500\
               + (1 / (abs(avg_middle - avg_left)))*REGULARIZATION\
               + (1 / (abs(avg_right - avg_left)))*REGULARIZATION
    elif avg_left == avg_right:
        val += 500\
               + (1 / (abs(avg_middle - avg_left)))*REGULARIZATION\
               + (1 / (abs(avg_right - avg_middle)))*REGULARIZATION
    else:
        val += (1 / (abs(avg_middle - avg_left)))*REGULARIZATION\
               + (1 / (abs(avg_right - avg_middle))*REGULARIZATION)\
               + (1 / (abs(avg_right - avg_left)))*REGULARIZATION
    return val


def init_take_2_heuristic(board: List[List[Soldier]]):
    val = 0
    for i in range(len(board)):
        for j in range(len(board[i])):
            soldier = board[i][j]
            if soldier.degree == Degree.FLAG and i == 0:
                val += 1000
            if soldier.degree == Degree.BOMB and next_to(i, j, Degree.FLAG, board):
                val += 100
            if soldier.degree == Degree.BOMB and i == len(board)-1:
                val -= 5
            if soldier.degree == Degree.ONE and i == len(board)-1:
                val -= 5
    avg_left = average_degree_val(0, 0, 3, 2, board)
    avg_middle = average_degree_val(1, 3, 3, 6, board)
    avg_right = average_degree_val(0, 7, 3, 9, board)
    val -= abs(avg_right - avg_left)
    val -= abs(avg_left - avg_middle)
    val -= abs(avg_middle - avg_right)
    return val


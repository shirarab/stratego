from game_state import GameState
from constants import Color, Degree, NUM_OF_PLAYER_SOLDIERS, BOARD_SIZE, SOLDIER_COUNT_FOR_EACH_DEGREE
from scipy import spatial
# import numpy as np

# from soldier import Color

SUM_DEGREES_OF_PLAYER_FOR_HEURISTIC = sum(
    [SOLDIER_COUNT_FOR_EACH_DEGREE[deg] * deg for deg in Degree if
     deg not in [Degree.BOMB, Degree.THREE, Degree.WATER, Degree.EMPTY]] + [
        SOLDIER_COUNT_FOR_EACH_DEGREE[Degree.BOMB] * 5, SOLDIER_COUNT_FOR_EACH_DEGREE[Degree.THREE] * 5])

MAX_DISTANCE_TO_FLAG = BOARD_SIZE


def null_heuristic(game_state: GameState, color: Color):
    return 0


def max_my_soldier_num_heuristic(game_state: GameState, color: Color):
    # return len(game_state.soldier_knowledge_base[color]) / NUM_OF_PLAYER_SOLDIERS
    return len(game_state.get_knowledge_base(color).get_living_soldiers()) / NUM_OF_PLAYER_SOLDIERS


def min_opp_soldiers_num_heuristic(game_state: GameState, color: Color):
    op_color = Color.RED if color == Color.BLUE else Color.BLUE
    val = 0
    dead_opp = game_state.dead[op_color]
    for i in dead_opp:
        val += dead_opp[i]
    return val / NUM_OF_PLAYER_SOLDIERS


def max_my_soldier_degree_heuristic(game_state: GameState, color: Color):
    val = 0
    for s in game_state.get_knowledge_base(color).get_living_soldiers():
        val += s.degree if s.degree != Degree.BOMB and s.degree != Degree.THREE else 5

    return val / SUM_DEGREES_OF_PLAYER_FOR_HEURISTIC


def min_opp_soldier_degree_heuristic(game_state: GameState, color: Color):
    op_color = Color.RED if color == Color.BLUE else Color.BLUE
    return 1 - (max_my_soldier_degree_heuristic(game_state, op_color) / SUM_DEGREES_OF_PLAYER_FOR_HEURISTIC)


def opp_distance_to_flag_heuristic(game_state: GameState, color: Color):
    op_color = Color.RED if color == Color.BLUE else Color.BLUE
    loc = []
    for s in game_state.get_knowledge_base(op_color).get_living_soldiers():
        loc.append([s.x, s.y])
    my_flag = [s for s in game_state.get_knowledge_base(color).get_living_soldiers() if s.degree == Degree.FLAG]
    if len(my_flag) == 0:
        return -10
    my_flag = my_flag[0]
    distance, index = spatial.KDTree(loc).query([my_flag.x, my_flag.y])
    return 1 - distance / MAX_DISTANCE_TO_FLAG


def distance_to_opp_flag_heuristic(game_state: GameState, color: Color):
    op_color = Color.RED if color == Color.BLUE else Color.BLUE
    return 1 - opp_distance_to_flag_heuristic(game_state, op_color)


def sum_of_heuristics_heuristic(game_state: GameState, color: Color):
    is_done = 20 if game_state.done else 0
    val = 0
    # val += is_done + min_opp_soldier_degree_heuristic(game_state, color)
    val += is_done + 2 * max_my_soldier_degree_heuristic(game_state, color)
    val += 2 * opp_distance_to_flag_heuristic(game_state, color)
    val += 4 * distance_to_opp_flag_heuristic(game_state, color)
    return val

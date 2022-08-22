import math
import random

from evaluate_score import weighted_num_soldiers_evaluator, naive_unit_count_evaluator
from game_state import GameState
from constants import Color, Degree, NUM_OF_PLAYER_SOLDIERS, BOARD_SIZE, SOLDIER_COUNT_FOR_EACH_DEGREE, OP_COLOR, \
    OP_DISTANCE_FROM_FLAG
from scipy import spatial

from soldier import Soldier

SUM_DEGREES_OF_PLAYER_FOR_HEURISTIC = sum(
    [SOLDIER_COUNT_FOR_EACH_DEGREE[deg] * deg for deg in Degree if
     deg not in [Degree.TWO, Degree.BOMB, Degree.THREE, Degree.WATER, Degree.EMPTY]] + [
        SOLDIER_COUNT_FOR_EACH_DEGREE[Degree.BOMB] * 5, SOLDIER_COUNT_FOR_EACH_DEGREE[Degree.THREE] * 5])

MAX_DISTANCE_TO_FLAG = BOARD_SIZE


def null_heuristic(game_state: GameState, color: Color):
    return 0


def random_heuristic(game_state: GameState, color: Color):
    return random.randint(0, 10)


def max_my_soldier_num_heuristic(game_state: GameState, color: Color):
    is_done = math.inf if game_state.done else 0
    if is_done != 0:
        return is_done
    # return len(game_state.soldier_knowledge_base[color]) / NUM_OF_PLAYER_SOLDIERS
    return len(game_state.get_knowledge_base(color).get_living_soldiers()) / NUM_OF_PLAYER_SOLDIERS


# good heuristic
def min_opp_soldiers_num_heuristic(game_state: GameState, color: Color):
    is_done = math.inf if game_state.done else 0
    if is_done != 0:
        return is_done
    op_color = Color.RED if color == Color.BLUE else Color.BLUE
    val = 0
    dead_opp = game_state.dead[op_color]
    for i in dead_opp:
        val += dead_opp[i]
    return val / NUM_OF_PLAYER_SOLDIERS


def max_my_soldier_degree_heuristic(game_state: GameState, color: Color):
    is_done = math.inf if game_state.done else 0
    if is_done != 0:
        return is_done
    val = 0
    for s in game_state.get_knowledge_base(color).get_living_soldiers():
        if s.degree == Degree.TWO:
            continue
        val += s.degree if (s.degree != Degree.BOMB and s.degree != Degree.THREE) else 5

    return val / SUM_DEGREES_OF_PLAYER_FOR_HEURISTIC


def min_opp_soldier_degree_heuristic(game_state: GameState, color: Color):
    is_done = math.inf if game_state.done else 0
    if is_done != 0:
        return is_done
    op_color = Color.RED if color == Color.BLUE else Color.BLUE
    return 1 - (max_my_soldier_degree_heuristic(game_state, op_color) / SUM_DEGREES_OF_PLAYER_FOR_HEURISTIC)


def opp_distance_to_flag_heuristic(game_state: GameState, color: Color):
    is_done = math.inf if game_state.done else 0
    if is_done != 0:
        return is_done
    op_color = Color.RED if color == Color.BLUE else Color.BLUE
    loc = []
    for s in game_state.get_knowledge_base(op_color).get_living_soldiers():
        loc.append([s.x, s.y])
    my_flag = [s for s in game_state.get_knowledge_base(color).get_living_soldiers() if s.degree == Degree.FLAG]
    if len(my_flag) == 0:
        return -10
    my_flag = my_flag[0]
    distance, index = spatial.KDTree(loc).query([my_flag.x, my_flag.y])
    return distance


def distance_to_opp_flag_heuristic(game_state: GameState, color: Color):
    is_done = math.inf if game_state.done else 0
    if is_done != 0:
        return is_done
    op_color = Color.RED if color == Color.BLUE else Color.BLUE
    return opp_distance_to_flag_heuristic(game_state, op_color)


def small_dist_opp_to_flag_heuristic(game_state: GameState, color: Color):
    is_done = math.inf if game_state.done else 0
    if is_done != 0:
        return is_done
    flag_x, flag_y = (0, 0)
    living_soldiers = game_state.get_knowledge_base(color).get_living_soldiers()
    for soldier in living_soldiers:
        if soldier.degree == Degree.FLAG:
            flag_x, flag_y = soldier.position
            break
    count_soldiers = 0
    for soldier in living_soldiers:
        if soldier.degree == Degree.FLAG or soldier.degree < Degree.SEVEN:
            continue
        x, y = soldier.position
        diff_x = abs(x - flag_x)
        diff_y = abs(y - flag_y)
        if diff_x + diff_y < 3:
            count_soldiers += 1
            if count_soldiers == 2:
                return 6
    return count_soldiers * 2


def min_of_opp_soldiers_that_are_flag_options_heuristic(game_state: GameState, color: Color):
    is_done = math.inf if game_state.done else 0
    if is_done != 0:
        return is_done
    op_color = Color.RED if color == Color.BLUE else Color.BLUE
    if game_state.can_op_soldier_be_flag is None:
        op_soldiers_knowledge_base = game_state.get_knowledge_base(op_color)
        val = 0
        for s in op_soldiers_knowledge_base.get_living_soldiers():
            val += 0 if Degree.FLAG in op_soldiers_knowledge_base.get_options_for_soldier(s) else 1
        return val

    else:
        val = 0
        living_sol = game_state.get_knowledge_base(op_color).get_living_soldiers()
        for s in living_sol:
            val += 0 if game_state.can_op_soldier_be_flag[s] else 1
        return val


def sum_of_heuristics_heuristic(game_state: GameState, color: Color):
    is_done = math.inf if game_state.done else 0
    if is_done != 0:
        return is_done
    val = 0
    val += 2 * min_opp_soldiers_num_heuristic(game_state, color)
    # val += 6 * min_of_opp_soldiers_that_are_flag_options_heuristic(game_state, color)
    # val += 2 * max_my_soldier_degree_heuristic(game_state, color)
    # val += small_dist_opp_to_flag_heuristic(game_state, color)
    val += min_of_opp_soldiers_that_are_flag_options_heuristic(game_state, color)
    # val += 3 * distance_to_opp_flag_heuristic(game_state, color)
    return val


# good heuristic
def attack_opponent_heuristic(game_state: GameState, color: Color):
    is_done = math.inf if game_state.done else 0
    if is_done != 0:
        return is_done
    val = 0
    val += 2 * min_opp_soldiers_num_heuristic(game_state, color)
    val += min_of_opp_soldiers_that_are_flag_options_heuristic(game_state, color)
    return val


def get_random_weights():
    pieceW = random.uniform(1, 1.8)
    rankW = random.uniform(0.015, 0.075)
    moveW = random.uniform(0.01, 0.06)
    distW = random.uniform(0.005, 0.025)
    return pieceW, rankW, moveW, distW


# heuristic for alpha-beta
def better_num_soldiers_difference_heuristic(game_state: GameState, color: Color):
    return weighted_num_soldiers_evaluator(game_state, color, get_random_weights)


def my_most_far_soldier(game_state: GameState, color: Color):
    my_soldiers = game_state.get_knowledge_base(color).get_living_soldiers()
    x = 0
    for soldier in my_soldiers:
        weight = 0
        if (color == Color.RED and soldier.x > 5) or (color == Color.BLUE and soldier.x < 4):
            weight = random.uniform(0.5, 1.5)
        elif 6 > soldier.x > 3:
            weight = random.uniform(0.2, 0.49)
        x += weight * soldier.x if color == Color.RED else weight * (BOARD_SIZE - soldier.x)
    return x


# good heuristic
def max_me_min_opponent_heuristic(game_state: GameState, color: Color):
    is_done = math.inf if game_state.done else 0
    if is_done != 0:
        return is_done
    max_me = max_my_soldier_degree_heuristic(game_state, color)
    min_op = min_opp_soldiers_num_heuristic(game_state, color)
    op_flag_count = min_of_opp_soldiers_that_are_flag_options_heuristic(game_state, color)
    dis_op_flag = 5 if distance_to_opp_flag_heuristic(game_state, color) < OP_DISTANCE_FROM_FLAG else 0
    protect_my_flag = small_dist_opp_to_flag_heuristic(game_state, color)
    op_close_to_my_flag = -10 if opp_distance_to_flag_heuristic(game_state, color) < OP_DISTANCE_FROM_FLAG else 0
    most_far_soldier = my_most_far_soldier(game_state, color)
    return 3 * max_me + 7 * min_op + op_flag_count + dis_op_flag + protect_my_flag \
           + op_close_to_my_flag + most_far_soldier


# similar to "min_opp_soldiers_num_heuristic" but "min_opp_soldiers_num_heuristic" is better
def naive_unit_count_heuristic(game_state: GameState, color: Color):
    return naive_unit_count_evaluator(game_state, color)


def protect_flag_and_attack_heuristic(game_state: GameState, color: Color):
    is_done = math.inf if game_state.done else 0
    if is_done != 0:
        return is_done
    protect_my_flag = small_dist_opp_to_flag_heuristic(game_state, color)
    op_close_to_my_flag = -10 if opp_distance_to_flag_heuristic(game_state, color) < OP_DISTANCE_FROM_FLAG else 0
    most_far_soldier = my_most_far_soldier(game_state, color)
    res = protect_my_flag + 5 * op_close_to_my_flag + most_far_soldier
    if game_state.dead[color][Degree.FLAG] > 0:
        return -10000
    return res

# try not to reveal 10
# once 10 revealed- it should attack only identified pieces.
# 1 and 9 should be together as long as they can
# if enemy gets close to a piece it can kill- bring a 2 (without him knowing) for it to chase instead
# attack pieces from high to low
# never leave flag unprotected
# start with moving lower pieces and then once enemy's pieces are revealed kill them with higher ranks

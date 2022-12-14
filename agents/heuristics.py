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


# good heuristic
def attack_opponent_heuristic(game_state: GameState, color: Color):
    is_done = math.inf if game_state.done else 0
    if is_done != 0:
        return is_done
    val = 0
    val += 15 * min_opp_soldiers_num_heuristic(game_state, color)
    val += min_of_opp_soldiers_that_are_flag_options_heuristic(game_state, color)

    return val


# good heuristic   -  use for guessing agent only
def max_me_min_opponent_heuristic(game_state: GameState, color: Color):
    is_done = math.inf if game_state.done else 0
    if is_done != 0:
        return is_done
    max_me = max_my_soldier_degree(game_state, color)
    min_op = min_opp_soldiers_num_heuristic(game_state, color)
    op_flag_count = min_of_opp_soldiers_that_are_flag_options_heuristic(game_state, color)
    # dis_op_flag = 5 if distance_to_opp_flag_heuristic(game_state, color) < OP_DISTANCE_FROM_FLAG else 0
    protect_my_flag = large_soldiers_near_flag_heuristic(game_state, color)
    op_close_to_my_flag = -10 if opp_distance_to_flag_heuristic(game_state, color) < OP_DISTANCE_FROM_FLAG else 0
    most_far_soldier = my_most_far_soldier(game_state, color)
    return 3 * max_me + 7 * min_op + op_flag_count + protect_my_flag \
           + op_close_to_my_flag + 10 * most_far_soldier  # + dis_op_flag


# good heuristic - use for opp heuristic for guessing agent only
def protect_flag_and_attack_heuristic(game_state: GameState, color: Color):
    is_done = math.inf if game_state.done else 0
    if is_done != 0:
        return is_done
    protect_my_flag = large_soldiers_near_flag_heuristic(game_state, color)
    op_close_to_my_flag = opp_close_to_my_flag_heuristic(game_state, color)
    most_far_soldier = my_most_far_soldier(game_state, color)
    res = protect_my_flag + op_close_to_my_flag + 10 * most_far_soldier
    return res


# heuristic for alpha-beta
def expose_soldiers_and_advance_heuristic(game_state: GameState, color: Color):
    return weighted_num_soldiers_evaluator(game_state, color, get_weights=get_random_weights)


# similar to "min_opp_soldiers_num_heuristic" but "min_opp_soldiers_num_heuristic" is better
def naive_unit_count_heuristic(game_state: GameState, color: Color):
    return naive_unit_count_evaluator(game_state, color)


def null_heuristic(game_state: GameState, color: Color):
    return 0


def random_heuristic(game_state: GameState, color: Color):
    return random.randint(1, 10)


def max_my_soldier_num(game_state: GameState, color: Color):
    is_done = math.inf if game_state.done else 0
    if is_done != 0:
        return is_done
    return len(game_state.get_knowledge_base(color).get_living_soldiers()) / NUM_OF_PLAYER_SOLDIERS


def max_my_soldier_degree(game_state: GameState, color: Color):
    is_done = math.inf if game_state.done else 0
    if is_done != 0:
        return is_done
    val = 0
    soldiers = game_state.get_knowledge_base(color).get_living_soldiers()
    for s in soldiers:
        if s.degree == Degree.TWO:
            continue
        val += s.degree if (s.degree != Degree.BOMB and s.degree != Degree.THREE) else 5

    return val / SUM_DEGREES_OF_PLAYER_FOR_HEURISTIC


def min_opp_soldier_degree_heuristic(game_state: GameState, color: Color):
    is_done = math.inf if game_state.done else 0
    if is_done != 0:
        return is_done
    op_color = Color.RED if color == Color.BLUE else Color.BLUE
    return 1 - (max_my_soldier_degree(game_state, op_color))


def opp_distance_to_flag_heuristic(game_state: GameState, color: Color):
    # guessing agent only - for opp heuristic
    # return the distance of the closest opp soldier to my flag
    if game_state.done:
        return math.inf
    op_color = OP_COLOR[color]
    my_flag = game_state.red_flag if color == Color.RED else game_state.blue_flag
    if my_flag is None:
        return -10
    distance = BOARD_SIZE
    flag_x = my_flag[0]
    flag_y = my_flag[1]
    soldiers = game_state.get_knowledge_base(op_color).get_living_soldiers()
    for s in soldiers:
        dis = abs(s.x - flag_x) + abs(s.y - flag_y)
        if dis < distance:
            distance = dis
    return distance


def opp_close_to_my_flag_heuristic(game_state: GameState, color: Color):
    # guessing agent only - for opp heuristic
    # returns a lower value as more enemy soldiers approach my flag.
    # The value is higher for a soldier according to his proximity to the flag
    if game_state.done:
        return math.inf
    op_color = OP_COLOR[color]
    my_flag = game_state.red_flag if color == Color.RED else game_state.blue_flag
    if my_flag is None:
        return -10
    val = 0
    flag_x = my_flag[0]
    flag_y = my_flag[1]
    soldiers = game_state.get_knowledge_base(op_color).get_living_soldiers()
    for s in soldiers:
        dis = abs(s.x - flag_x) + abs(s.y - flag_y)
        if dis < OP_DISTANCE_FROM_FLAG:
            val -= 50 * (OP_DISTANCE_FROM_FLAG - dis)
    return val


def distance_to_opp_flag_heuristic(game_state: GameState, color: Color):
    # guessing agent only
    # return the distance of my closest soldier to the op flag
    is_done = math.inf if game_state.done else 0
    if is_done != 0:
        return is_done
    op_color = Color.RED if color == Color.BLUE else Color.BLUE
    return opp_distance_to_flag_heuristic(game_state, op_color)


def large_soldiers_near_flag_heuristic(game_state: GameState, color: Color):
    # guessing agent only - for opp heuristic
    is_done = math.inf if game_state.done else 0
    if is_done != 0:
        return is_done

    living_soldiers = game_state.get_knowledge_base(color).get_living_soldiers()
    my_flag = game_state.red_flag if color == Color.RED else game_state.blue_flag
    flag_x = my_flag[0]
    flag_y = my_flag[1]
    count_soldiers = 0
    for soldier in living_soldiers:
        if soldier.degree < Degree.SEVEN:
            continue
        x, y = soldier.position
        if abs(x - flag_x) + abs(y - flag_y) < 3:
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
    # val += 2 * max_my_soldier_degree_heuristic(game_state, color)
    # val += large_soldiers_near_flag_heuristic(game_state, color)
    val += min_of_opp_soldiers_that_are_flag_options_heuristic(game_state, color)
    # val += 3 * distance_to_opp_flag_heuristic(game_state, color)
    return val


def get_random_weights():
    pieceW = random.uniform(1, 1.8)
    rankW = random.uniform(0.015, 0.075)
    moveW = random.uniform(0.01, 0.06)
    distW = random.uniform(0.005, 0.025)
    return pieceW, rankW, moveW, distW


def my_most_far_soldier(game_state: GameState, color: Color):
    my_soldiers = game_state.get_knowledge_base(color).get_living_soldiers()
    x = 0
    weight1 = random.uniform(0.5, 1.5)
    weight2 = random.uniform(0.2, 0.7)
    if color == Color.RED:
        for soldier in my_soldiers:
            weight = 0
            if 6 > soldier.x > 3:
                weight = weight2
            elif soldier.x > 5:
                weight = weight1
            x += weight * soldier.x
    else:
        for soldier in my_soldiers:
            weight = 0
            if 6 > soldier.x > 3:
                weight = weight2
            elif soldier.x < 4:
                weight = weight1
            x += weight * (BOARD_SIZE - soldier.x)
    return x

# try not to reveal 10
# once 10 revealed- it should attack only identified pieces.
# 1 and 9 should be together as long as they can
# if enemy gets close to a piece it can kill- bring a 2 (without him knowing) for it to chase instead
# attack pieces from high to low
# never leave flag unprotected
# start with moving lower pieces and then once enemy's pieces are revealed kill them with higher ranks

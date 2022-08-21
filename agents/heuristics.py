import math
import random

from evaluate_score import evaluate_weighted_num_soldiers
from game_state import GameState
from constants import Color, Degree, NUM_OF_PLAYER_SOLDIERS, BOARD_SIZE, SOLDIER_COUNT_FOR_EACH_DEGREE, OP_COLOR
from scipy import spatial

from soldier import Soldier

SUM_DEGREES_OF_PLAYER_FOR_HEURISTIC = sum(
    [SOLDIER_COUNT_FOR_EACH_DEGREE[deg] * deg for deg in Degree if
     deg not in [Degree.BOMB, Degree.THREE, Degree.WATER, Degree.EMPTY]] + [
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
        val += s.degree if s.degree != Degree.BOMB and s.degree != Degree.THREE else 5

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
    return 1 - distance / MAX_DISTANCE_TO_FLAG


def distance_to_opp_flag_heuristic(game_state: GameState, color: Color):
    is_done = math.inf if game_state.done else 0
    if is_done != 0:
        return is_done
    op_color = Color.RED if color == Color.BLUE else Color.BLUE
    return 1 - opp_distance_to_flag_heuristic(game_state, op_color)


def small_dist_opp_to_flag_heuristic(game_state: GameState, color: Color):
    is_done = math.inf if game_state.done else 0
    if is_done != 0:
        return is_done
    return -20 if opp_distance_to_flag_heuristic(game_state, color) < 0.15 else 0


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


def get_random_weights():
    pieceW = random.uniform(1, 1.8)
    rankW = random.uniform(0.015, 0.075)
    moveW = random.uniform(0.01, 0.06)
    distW = random.uniform(0.005, 0.025)
    return pieceW, rankW, moveW, distW


def better_num_soldiers_difference_heuristic(game_state: GameState, color: Color):
    return evaluate_weighted_num_soldiers(game_state, color, get_random_weights)


# i-1j-1      i-1j        i-1j+1
# ij-1        ij          ij+1
# i+1j-1      i+1j        i+1j+1
def get_sum_around_soldier(game_state: GameState, soldier: Soldier) -> float:
    degreeW = random.uniform(0.1, 0.5)
    flagW = random.uniform(1.51, 1.9)
    sum: float = 0
    op_color = OP_COLOR[soldier.color]
    kb = game_state.get_knowledge_base(soldier.color)
    i, j = soldier.position
    positions = [(i - 1, j - 1, 1), (i - 1, j, 20), (i - 1, j + 1, 1),
                 (i, j - 1, 20), (i, j + 1, 20),
                 (i + 1, j - 1, 1), (i + 1, j, 20), (i + 1, j + 1, 1)]

    for (x, y, w) in positions:
        if not (0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE):
            continue
        s = game_state.board[x][y]
        is_op = True if s.color == op_color else False
        if is_op:
            if s.show_me:
                sum -= degreeW * w * s.degree
            else:
                sum -= degreeW * w * kb.get_highest_option_for_soldier(s)
        else:
            if s.degree not in [Degree.EMPTY, Degree.WATER]:
                if soldier.degree in [Degree.ONE, Degree.FLAG]:
                    sum += flagW * w * s.degree
                else:
                    sum += degreeW * w * s.degree
            else:
                sum += degreeW * w * 9
    # print(f"shira flag sum: {sum}")
    return sum


def temp_name(game_state: GameState, color: Color):
    show_meW = random.uniform(0.7, 1.1)
    positionsW = random.uniform(0.05, 0.16)

    op_color = OP_COLOR[color]
    show_me_diff = 0
    positions = 0
    sum_around_soldiers = 0

    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            soldier = game_state.board[i][j]
            if soldier.color == color:
                if i < 6:
                    positions += positionsW
                if soldier.show_me:
                    show_me_diff -= show_meW * soldier.degree
                    if i < 6:
                        positions -= positionsW * soldier.degree
                sum_around_soldiers += get_sum_around_soldier(game_state, soldier)
            elif soldier.color == op_color:
                if i > 4:
                    positions -= positionsW
                if soldier.show_me:
                    show_me_diff += show_meW * soldier.degree
                    if i > 4:
                        positions -= positionsW * soldier.degree
                    sum_around_soldiers -= get_sum_around_soldier(game_state, soldier)

    return show_me_diff + positions


def interesting_heuristic(game_state: GameState, color: Color):
    return 1.7 * temp_name(game_state, color) + 0.15*sum_of_heuristics_heuristic(game_state, color)

# try not to reveal 10
# once 10 revealed- it should attack only identified pieces.
# 1 and 9 should be together as long as they can
# if enemy gets close to a piece it can kill- bring a 2 (without him knowing) for it to chase instead
# attack pieces from high to low
# never leave flag unprotected
# start with moving lower pieces and then once enemy's pieces are revealed kill them with higher ranks

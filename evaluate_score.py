from typing import Set

from constants import Color, OP_COLOR, BOARD_SIZE, Degree, JEROEN_METS_VALUES_TABLE, NUVC_VALUES_TABLE
from game_state import GameState
from soldier import Soldier


def null_evaluate_score(game_state: GameState, color: Color, **kwargs):
    return 0


def num_soldiers_evaluator(game_state: GameState, color: Color, **kwargs):
    op_color = OP_COLOR[color]
    red_living_soldiers = game_state.get_knowledge_base(color).get_living_soldiers_count()
    blue_living_soldiers = game_state.get_knowledge_base(op_color).get_living_soldiers_count()
    return red_living_soldiers - blue_living_soldiers


def get_num_weights():
    pieceW, rankW, moveW, distW = 1.4, 0.045, 0.03, 0.018
    return pieceW, rankW, moveW, distW


def weighted_num_soldiers_evaluator(game_state: GameState, color: Color, get_weights=get_num_weights, **kwargs):
    pieceW, rankW, moveW, distW = get_weights()
    sum = 0
    op_color = OP_COLOR[color]
    # kb = game_state.get_knowledge_base(color)
    # op_kb = game_state.get_knowledge_base(op_color)
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            soldier = game_state.board[i][j]
            if soldier.color == color:
                sum += pieceW
                if soldier.show_me:
                    sum -= rankW * soldier.degree
                if i < 5 and color == Color.RED:
                    sum -= distW * (5 - i) ** 2
                elif i > 3 and color == Color.BLUE:
                    sum -= distW * (i - 3) ** 2
                if soldier.has_moved:  # kb.has_soldier_moved(soldier):
                    sum -= moveW
            elif soldier.color == op_color:
                sum -= pieceW
                if soldier.show_me:
                    sum += rankW * soldier.degree
                if i > 3 and color == Color.BLUE:
                    sum += distW * (i - 3) ** 2
                elif i < 5 and color == Color.RED:
                    sum += distW * (5 - i) ** 2
                if soldier.has_moved:  # op_kb.has_soldier_moved(soldier):
                    sum += moveW
    return sum


# better than "flat_naive_unit_count_evaluator" and "jeroen_mets_evaluator"
def naive_unit_count_evaluator(game_state: GameState, color: Color, **kwargs):
    friendlies = game_state.get_knowledge_base(color).get_living_soldiers_count()
    enemies = game_state.get_knowledge_base(OP_COLOR[color]).get_living_soldiers_count()
    return 1 - (1 - (float(friendlies) / (enemies * 40)) ** 8)


def flat_naive_unit_count_evaluator(game_state: GameState, color: Color, **kwargs):
    friendlies = game_state.get_knowledge_base(color).get_living_soldiers_count()
    enemies = game_state.get_knowledge_base(OP_COLOR[color]).get_living_soldiers_count()
    return (friendlies - enemies) / 80 + 0.5


def nuvc_agent_has_10_bombs_spy(soldiers: Set[Soldier]):
    op_has = {Degree.ONE: False, Degree.THREE: 0, Degree.TEN: False}
    for s in soldiers:
        if not s.is_alive:
            continue
        if s.degree == Degree.TEN:
            op_has[Degree.TEN] = True
        elif s.degree == Degree.BOMB:
            op_has[Degree.THREE] += 1
        elif s.degree == Degree.ONE:
            op_has[Degree.ONE] = True
        if op_has[Degree.TEN] and op_has[Degree.THREE] >= 2 and op_has[Degree.ONE]:
            break
    op_has[Degree.THREE] = True if op_has[Degree.THREE] >= 2 else False
    return op_has


def nuvc_get_soldier_points(soldier, op_has):
    if soldier.degree in op_has.keys():
        return NUVC_VALUES_TABLE[soldier.degree][0] if op_has[soldier.degree] else NUVC_VALUES_TABLE[soldier.degree][1]
    return NUVC_VALUES_TABLE[soldier.degree]


def naive_unit_value_count_evaluator(game_state: GameState, color: Color, red_agent, blue_agent):
    points = {Color.RED: 0, Color.BLUE: 0}
    red_soldiers = red_agent.soldiers
    blue_soldiers = blue_agent.soldiers
    red_has = nuvc_agent_has_10_bombs_spy(red_soldiers)
    blue_has = nuvc_agent_has_10_bombs_spy(blue_soldiers)
    for soldier in red_soldiers:
        points[Color.RED] += nuvc_get_soldier_points(soldier, blue_has)
    for soldier in blue_soldiers:
        points[Color.BLUE] += nuvc_get_soldier_points(soldier, red_has)
    return points[Color.RED] / (points[Color.BLUE] * 324)


def jeroen_mets_get_soldier_points(soldier: Soldier):
    points = 0
    if not soldier.is_alive:
        points += JEROEN_METS_VALUES_TABLE[soldier.degree][2]  # captured
        return points
    if soldier.show_me:
        points += JEROEN_METS_VALUES_TABLE[soldier.degree][1]  # discovered
    if soldier.has_moved:
        points += JEROEN_METS_VALUES_TABLE[soldier.degree][0]  # moved
    return points


def jeroen_mets_evaluator(game_state: GameState, color: Color, red_agent, blue_agent):
    points = {Color.RED: 0, Color.BLUE: 0}
    for soldier in red_agent.soldiers:
        points[Color.RED] += jeroen_mets_get_soldier_points(soldier)
    for soldier in blue_agent.soldiers:
        points[Color.BLUE] += jeroen_mets_get_soldier_points(soldier)
    return points[Color.RED] / (points[Color.BLUE] * 11087)

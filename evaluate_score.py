from constants import Color, OP_COLOR, BOARD_SIZE, Degree
from game_state import GameState


def null_evaluate_score(game_state: GameState, color: Color):
    return 0


def num_soldiers_evaluator(game_state: GameState, color: Color):
    op_color = OP_COLOR[color]
    red_living_soldiers = game_state.get_knowledge_base(color).get_living_soldiers_count()
    blue_living_soldiers = game_state.get_knowledge_base(op_color).get_living_soldiers_count()
    return red_living_soldiers - blue_living_soldiers


def get_num_weights():
    pieceW, rankW, moveW, distW = 1.4, 0.045, 0.03, 0.018
    return pieceW, rankW, moveW, distW


def weighted_num_soldiers_evaluator(game_state: GameState, color: Color, get_weights=get_num_weights):
    pieceW, rankW, moveW, distW = get_weights()
    sum = 0
    op_color = OP_COLOR[color]
    kb = game_state.get_knowledge_base(color)
    op_kb = game_state.get_knowledge_base(op_color)
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
                if kb.has_soldier_moved(soldier):
                    sum -= moveW
            elif soldier.color == op_color:
                sum -= pieceW
                if soldier.show_me:
                    sum += rankW * soldier.degree
                if i > 3 and color == Color.BLUE:
                    sum += distW * (i - 3) ** 2
                elif i < 5 and color == Color.RED:
                    sum += distW * (5 - i) ** 2
                if op_kb.has_soldier_moved(soldier):
                    sum += moveW
    return sum


def naive_unit_count_evaluator(game_state: GameState, color: Color):
    friendlies = game_state.get_knowledge_base(color).get_living_soldiers_count()
    enemies = game_state.get_knowledge_base(OP_COLOR[color]).get_living_soldiers_count()
    return 1 - (1 - (float(friendlies) / (enemies * 40)) ** 8)


def jeroen_mets_evaluator(game_state: GameState, color: Color):
    # shira todo
    values_table = {
        # degree: (moved, discovered, captured)
        Degree.BOMB: (0, 100, 750),
        Degree.ONE: (100, 0, 100),
        Degree.TWO: (100, 0, 2),
        Degree.THREE: (100, 20, 50),
        Degree.FOUR: (100, 5, 5),
        Degree.FIVE: (100, 10, 10),
        Degree.SIX: (100, 15, 20),
        Degree.SEVEN: (100, 20, 50),
        Degree.EIGHT: (100, 25, 100),
        Degree.NINE: (100, 50, 250),
        Degree.TEN: (100, 100, 500),
        Degree.FLAG: (0, 0, 1000)
    }

    return 0
    # points = {Color.RED: 0, Color.BLUE: 0}
    # for c in points.keys():
    #     kb = game_state.get_knowledge_base(c)
    #     for soldier in kb:
    #         if not soldier.is_alive:
    #             points[c] += values_table[soldier.degree][2]  # captured
    #         if soldier.show_me:
    #             points[c] += values_table[soldier.degree][1]  # discovered
    #         if kb.has_soldier_moved(soldier):
    #             points[c] += values_table[soldier.degree][0]  # moved
    #
    # return points[Color.RED] / (points[Color.BLUE] * 11087)

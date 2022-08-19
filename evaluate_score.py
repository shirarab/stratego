from constants import Color, OP_COLOR, BOARD_SIZE
from game_state import GameState


def evaluate_num_soldiers(game_state: GameState, color: Color):
    op_color = OP_COLOR[color]
    red_living_soldiers = game_state.get_knowledge_base(color).get_living_soldiers_count()
    blue_living_soldiers = game_state.get_knowledge_base(op_color).get_living_soldiers_count()
    return red_living_soldiers - blue_living_soldiers


# pieceW, rankW, moveW, distW = 1, 0.05, 0.03, 0.02


def evaluate_weighted_num_soldiers(game_state: GameState, color: Color):
    pieceW, rankW, moveW, distW, flagW = 1.4, 0.045, 0.03, 0.018, 2
    sum = 0
    op_color = OP_COLOR[color]
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            soldier = game_state.board[i][j]
            if soldier.color == color:
                sum += pieceW
                if soldier.show_me:
                    sum -= rankW * soldier.degree
                if i < 6:
                    sum -= distW * (6 - i) ** 2

            elif soldier.color == op_color:
                sum -= pieceW
                if soldier.show_me:
                    sum += rankW * soldier.degree
                if i > 3:
                    sum += distW * (i - 3) ** 2
    return sum

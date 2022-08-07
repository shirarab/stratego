from game_state import GameState
from constants import Color


# from soldier import Color


def null_heuristic(game_state: GameState, color: Color):
    return 0


def try_heuristic(game_state: GameState, color: Color):
    val = 0
    for i in range(10):
        for j in range(10):
            if game_state.get_soldier_at_x_y(i, j).color == color:
                val += 1
    return val


def min_soldiers_opp_heuristic(game_state: GameState, color: Color):
    op_color = Color.RED if color == Color.BLUE else Color.BLUE
    val = 0
    dead_opp = game_state.dead[op_color]
    for i in dead_opp:
        val += dead_opp[i]
    return val


def min_opp_soldiers_max_my_soldiers_heuristic(game_state: GameState, color: Color):
    val = 0
    if game_state.done:
        val += 20
    return val + min_soldiers_opp_heuristic(game_state, color) + try_heuristic(game_state, color)

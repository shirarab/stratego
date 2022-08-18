from typing import Set

from action import Action
from game_state import GameState
from constants import Color
# from soldier import Color


def null_get_legal_actions_opponent(game_state: GameState, color: Color) -> Set[Action]:
    return set()


def do_not_use_me_ever(game_state: GameState, color: Color) -> Set[Action]:
    return game_state.get_legal_actions(color)


def null_get_successor_opponent(game_state: GameState, action: Action, color: Color) -> GameState:
    return game_state.get_successor(action)

import abc
from typing import Tuple, Set, List

from action import Direction
from degree import Degree
from game_state import GameState
from soldier import Soldier


class StrategoGraphic(object):
    def __init__(self, board_size, num_players_to_show: int = 0):
        self._board_size = board_size
        self._num_players_to_show = num_players_to_show

    @property
    def board_size(self):
        return self._board_size

    @property
    def num_players_to_show(self):
        return self._num_players_to_show

    @abc.abstractmethod
    def show_board(self, game_state: GameState):
        return

    @abc.abstractmethod
    def ask_for_initial_position(self, soldiers: List[Soldier], positions: Set[Tuple[int, int]]) \
            -> Tuple[Soldier, int, int]:
        # soldier, x, y
        return

    @abc.abstractmethod
    def ask_for_action(self, game_state: GameState) -> Tuple[int, int, Direction, int]:
        # x, y, direction, num_steps
        return

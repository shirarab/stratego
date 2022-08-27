from typing import Callable

from agents.agent import Agent
from constants import Degree, BOARD_SIZE, SOLDIER_COUNT_FOR_EACH_DEGREE
from evaluate_score import null_evaluate_score
from game_state import GameState
from graphics.graphic import Graphic
from constants import Color
from soldier import Soldier


class StrategoGame(object):
    def __init__(self, red_agent: Agent, blue_agent: Agent, graphic: Graphic,
                 evaluate_score: Callable[[GameState, Color], float] = null_evaluate_score):
        self._red_agent = red_agent
        self._blue_agent = blue_agent
        self._graphic = graphic
        self._state: GameState = None
        self._game_ended = False
        self._turn_count = 0
        self._evaluate_score = evaluate_score

    @property
    def state(self):
        return self._state

    def get_initial_board(self):
        red_board = self._red_agent.get_initial_positions()
        blue_board = self._blue_agent.get_initial_positions()
        board = [[Soldier(Degree.EMPTY, i, j, Color.GRAY) for j in range(BOARD_SIZE)]
                 for i in range(BOARD_SIZE)]
        for i in range(len(red_board)):
            for j in range(len(red_board[0])):
                board[i][j] = red_board[i][j]
                red_board[i][j].set_position(i, j)
        for i in range(2):
            for j in range(BOARD_SIZE):
                if j in {2, 3, 6, 7}:
                    board[4 + i][j] = Soldier(Degree.WATER, 4 + i, j, Color.WATER)
        for i in range(len(blue_board)):
            for j in range(len(blue_board[0])):
                board[BOARD_SIZE - 1 - i][j] = blue_board[i][j]
                board[BOARD_SIZE - 1 - i][j].set_x(BOARD_SIZE - 1 - i)
                blue_board[i][j].set_position(BOARD_SIZE - 1 - i, j)
        return board

    def start_soldiers(self, color: Color):
        soldiers = set()
        for degree in SOLDIER_COUNT_FOR_EACH_DEGREE.keys():
            for i in range(SOLDIER_COUNT_FOR_EACH_DEGREE[degree]):
                soldiers.add(Soldier(degree, 0, 0, color))
        return soldiers

    def run(self):
        self._red_agent.set_start_soldiers(self.start_soldiers(Color.RED))
        self._blue_agent.set_start_soldiers(self.start_soldiers(Color.BLUE))
        board = self.get_initial_board()
        self._state = GameState(board)
        self._graphic.show_board(self._state)
        return self._game_loop()

    def _game_loop(self):
        while not self._state.done:
            self._turn_count += 1
            red_action = self._red_agent.get_action(self._state)
            if red_action is None:
                self._state.winner = Color.BLUE
                self._state.done = True
            else:
                self._state.apply_action(red_action)
                self._graphic.show_board(self._state)
            if self._state.done:
                break
            self._turn_count += 1
            blue_action = self._blue_agent.get_action(self._state)
            if blue_action is None:
                self._state.winner = Color.RED
                self._state.done = True
            else:
                self._state.apply_action(blue_action)
                self._graphic.show_board(self._state)
            self._state.score = self._evaluate_score(self._state, Color.RED,
                                                     red_agent=self._red_agent, blue_agent=self._blue_agent)
        self._graphic.game_over(self._state.winner, self._state.score)
        return self._state.score, self._turn_count

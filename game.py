from agents.agent import Agent
from constants import Degree, BOARD_SIZE, NUM_OF_PLAYER_DEGREE_SOLDIERS
from game_state import GameState
from graphics.stratego_graphic import StrategoGraphic
from constants import Color
from soldier import Soldier


class StrategoGame(object):
    def __init__(self, red_agent: Agent, blue_agent: Agent, graphic: StrategoGraphic,
                 sleep_between_actions: bool = False):
        self._red_agent = red_agent
        self._blue_agent = blue_agent
        self._graphic = graphic
        self._state: GameState = None
        self._game_ended = False
        self._turn_count = 0
        self._sleep_between_actions = sleep_between_actions

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
        for degree in NUM_OF_PLAYER_DEGREE_SOLDIERS.keys():
            for i in range(NUM_OF_PLAYER_DEGREE_SOLDIERS[degree]):
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
            # if self._sleep_between_actions:
            #     time.sleep(10)
            self._turn_count += 1
            red_action = self._red_agent.get_action(self._state)
            self._state.apply_action(red_action)
            self._graphic.show_board(self._state)
            if self._state.done:
                break
            # if self._sleep_between_actions:
            #     time.sleep(10)
            self._turn_count += 1
            blue_action = self._blue_agent.get_action(self._state)
            self._state.apply_action(blue_action)
            self._graphic.show_board(self._state)
        self._graphic.game_over(self._state.winner, self._state.score)
        return self._state.score, self._turn_count

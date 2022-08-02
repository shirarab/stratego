from agents.agent import Agent
from degree import Degree
from game_state import GameState, BOARD_SIZE
from graphics.stratego_graphic import StrategoGraphic
from soldier import Soldier, Color

NUM_BOMB = 6
NUM_TWO = 8
NUM_THREE = 5
NUM_FOUR = 4
NUM_FIVE = 4
NUM_SIX = 4
NUM_SEVEN = 3
NUM_EIGHT = 2


class StrategoGame(object):
    def __init__(self, red_agent: Agent, blue_agent: Agent, graphic: StrategoGraphic):
        self._red_agent = red_agent
        self._blue_agent = blue_agent
        self._graphic = graphic
        self._state: GameState = None
        self._game_ended = False

    def get_initial_board(self):
        red_board = self._red_agent.get_initial_positions()
        blue_board = self._blue_agent.get_initial_positions()
        board = [[Soldier(Degree.EMPTY, i, j, Color.GRAY) for i in range(BOARD_SIZE)]
                 for j in range(BOARD_SIZE)]
        for i in range(len(red_board)):
            for j in range(len(red_board[0])):
                board[i][j] = red_board[i][j]
        for i in range(2):
            for j in range(BOARD_SIZE):
                if j in {2, 3, 6, 7}:
                    board[4 + i][j] = Soldier(Degree.WATER, 4 + i, j, Color.GRAY)
        for i in range(len(blue_board)):
            for j in range(len(blue_board[0])):
                board[BOARD_SIZE - 1 - i][j] = blue_board[i][j]
                board[BOARD_SIZE - 1 - i][j].set_x(BOARD_SIZE - 1 - i)
        return board

    def start_soldiers(self, color: Color):
        soldiers = set()
        soldiers.add(Soldier(Degree.FLAG, 0, 0, color))
        for i in range(NUM_BOMB):
            soldiers.add(Soldier(Degree.BOMB, 0, 0, color))
        soldiers.add(Soldier(Degree.ONE, 0, 0, color))
        for i in range(NUM_TWO):
            soldiers.add(Soldier(Degree.TWO, 0, 0, color))
        for i in range(NUM_THREE):
            soldiers.add(Soldier(Degree.THREE, 0, 0, color))
        for i in range(NUM_FOUR):
            soldiers.add(Soldier(Degree.FOUR, 0, 0, color))
        for i in range(NUM_FIVE):
            soldiers.add(Soldier(Degree.FIVE, 0, 0, color))
        for i in range(NUM_SIX):
            soldiers.add(Soldier(Degree.SIX, 0, 0, color))
        for i in range(NUM_SEVEN):
            soldiers.add(Soldier(Degree.SEVEN, 0, 0, color))
        for i in range(NUM_EIGHT):
            soldiers.add(Soldier(Degree.EIGHT, 0, 0, color))
        soldiers.add(Soldier(Degree.NINE, 0, 0, color))
        soldiers.add(Soldier(Degree.TEN, 0, 0, color))
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
            red_action = self._red_agent.get_action(self._state)
            self._state.apply_action(red_action)
            self._graphic.show_board(self._state)
            if self._state.done:
                break
            blue_action = self._blue_agent.get_action(self._state)
            self._state.apply_action(blue_action)
            self._graphic.show_board(self._state)
        return self._state.score

from typing import Set

from degree import Degree
from soldier import Soldier, Color
from action import Action, Direction

BOARD_SIZE = 10
DEAD_SOLDIERS = {
    Degree.BOMB: 0,
    Degree.ONE: 0,
    Degree.TWO: 0,
    Degree.THREE: 0,
    Degree.FOUR: 0,
    Degree.FIVE: 0,
    Degree.SIX: 0,
    Degree.SEVEN: 0,
    Degree.EIGHT: 0,
    Degree.NINE: 0,
    Degree.TEN: 0,
    Degree.FLAG: 0
}


class GameState(object):
    def __init__(self, board, score=0, done=False):
        # if board is None:
        #     board = [['-' for i in range(BOARD_SIZE)] for j in range(BOARD_SIZE)]
        self._board = board
        self._score = score
        self._done = done
        self._dead = {Color.RED: DEAD_SOLDIERS.copy(), Color.BLUE: DEAD_SOLDIERS.copy()}
        self._winner = Color.GRAY

    @property
    def done(self):
        return self._done

    @property
    def score(self):
        return self._score

    @property
    def board(self):
        return self._board

    @property
    def dead(self):
        return self._dead

    @property
    def winner(self):
        return self._winner

    def get_soldier_at_x_y(self, x, y) -> Soldier:
        if 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE:
            return self.board[x][y]
        return None

    def get_soldier_legal_actions(self, soldier: Soldier):
        legal_actions = set()
        if soldier.degree in {Degree.BOMB, Degree.FLAG, Degree.EMPTY, Degree.WATER}:
            return legal_actions
        if soldier.degree == Degree.TWO:
            for direction in Direction:
                for num_steps in range(1, BOARD_SIZE):
                    is_good_move, next_is_empty = self._is_legal_move(direction, soldier, num_steps)
                    if is_good_move:
                        legal_actions.add(Action(soldier, direction, num_steps))
                    if (not is_good_move) or (not next_is_empty):
                        break  # cant jump over illegal step
            return legal_actions
        # soldier degree is not TWO
        for direction in Direction:
            if self._is_legal_move(direction, soldier)[0]:
                legal_actions.add(Action(soldier, direction, 1))
        return legal_actions

    def _is_legal_move(self, direction: Direction, soldier: Soldier, num_steps: int = 1):
        opponent = None
        next_is_empty = False
        if direction == Direction.UP:
            opponent = self.get_soldier_at_x_y(soldier.x + num_steps, soldier.y)
        elif direction == Direction.DOWN:
            opponent = self.get_soldier_at_x_y(soldier.x - num_steps, soldier.y)
        elif direction == Direction.RIGHT:
            opponent = self.get_soldier_at_x_y(soldier.x, soldier.y + num_steps)
        elif direction == Direction.LEFT:
            opponent = self.get_soldier_at_x_y(soldier.x, soldier.y - num_steps)
        if opponent is None or opponent.color == soldier.color \
                or opponent.degree == Degree.WATER:
            return False, next_is_empty
        if opponent.degree == Degree.EMPTY:
            next_is_empty = True
        return True, next_is_empty

    def get_legal_actions(self, agent_color) -> Set[Action]:
        legal_actions = set()
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                soldier = self._board[i][j]
                if soldier.color == agent_color:
                    soldier_legal_actions = self.get_soldier_legal_actions(soldier)
                    legal_actions |= soldier_legal_actions
        if len(legal_actions) == 0:
            self._done = True
            self._winner = Color.RED if agent_color == Color.BLUE else Color.BLUE
        return legal_actions

    def shot_and_dead(self, killed: Soldier, winner: Soldier):
        killed.kill_me()
        self.dead[killed.color][killed.degree] += 1
        winner.set_show_me()

    def apply_action(self, action: Action):
        # we assume that action can only be legal
        if self._done or action is None:
            return
        sol_x = action.soldier.x
        sol_y = action.soldier.y
        op_x = sol_x
        op_y = sol_y
        if action.direction == Direction.UP:
            op_x += action.num_steps
        if action.direction == Direction.DOWN:
            op_x -= action.num_steps
        if action.direction == Direction.RIGHT:
            op_y += action.num_steps
        if action.direction == Direction.LEFT:
            op_y -= action.num_steps
        opponent = self.get_soldier_at_x_y(op_x, op_y)
        instead_me = Soldier(Degree.EMPTY, sol_x, sol_y, Color.GRAY)
        instead_opponent = opponent
        if opponent.degree == Degree.EMPTY:
            instead_opponent = action.soldier
            action.soldier.set_position(op_x, op_y)
        elif opponent.degree == Degree.BOMB:
            if action.soldier.degree == Degree.THREE:
                instead_opponent = action.soldier
                self.shot_and_dead(opponent, action.soldier)
                action.soldier.set_position(op_x, op_y)
            else:
                self.shot_and_dead(action.soldier, opponent)
        elif opponent.degree == Degree.FLAG:
            instead_opponent = action.soldier
            self.shot_and_dead(opponent, action.soldier)
            action.soldier.set_position(op_x, op_y)
            self._done = True
            self._winner = action.soldier.color
        elif opponent.degree == Degree.TEN and action.soldier.degree == Degree.ONE:
            instead_opponent = action.soldier
            self.shot_and_dead(opponent, action.soldier)
            action.soldier.set_position(op_x, op_y)
        elif opponent.degree > action.soldier.degree:
            self.shot_and_dead(action.soldier, opponent)
        elif opponent.degree < action.soldier.degree:
            instead_opponent = action.soldier
            self.shot_and_dead(opponent, action.soldier)
            action.soldier.set_position(op_x, op_y)
        elif opponent.degree == action.soldier.degree:
            instead_opponent = Soldier(Degree.EMPTY, sol_x, sol_y, Color.GRAY)
            self.shot_and_dead(action.soldier, opponent)
            self.shot_and_dead(opponent, action.soldier)
        self._board[sol_x][sol_y] = instead_me
        self._board[op_x][op_y] = instead_opponent

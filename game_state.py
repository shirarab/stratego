from typing import Set
from copy import deepcopy
from constants import Degree, DEAD_SOLDIERS, BOARD_SIZE, DEGREE_OPTIONS_LIST
from constants import Color, Direction
from soldier import Soldier
from action import Action


class GameState(object):
    def __init__(self, board, score=0, done=False, dead=None):
        """
        Create a new instance of game state
        
        Attributes:
            self._board : Two-dimensional array of Soldier objects
            self._score :
            self._done : Is the game over (flag revealed)
            self._dead : Dead soldiers for each color
            self._winner : winning color
            self.knowledge_base : for each color, keep a dictionary with soldier objects as keys and optional degrees
                                    as values
            
        """
        self._board = board
        self._score = score
        self._done = done
        if dead is None:
            self._dead = {Color.RED: DEAD_SOLDIERS.copy(), Color.BLUE: DEAD_SOLDIERS.copy()}
        else:
            self._dead = dead
        self._winner = Color.GRAY
        self.knowledge_base = {Color.RED: {}, Color.BLUE: {}}
        # init the knowledge base with full options for each opponent soldier:
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if board[i][j].color == Color.RED or board[i][j].color == Color.BLUE:
                    self.knowledge_base[board[i][j].color][board[i][j]] = DEGREE_OPTIONS_LIST.copy()

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

    def get_successor(self, action: Action):
        self.apply_action(action)
        return self

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

    def store(self):
        stored_info_me = {"score": self._score, "done": self._done, "winner": self._winner,
                          "dead": deepcopy(self._dead), "board": {}}
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                soldier_info = self._board[i][j].store()
                stored_info_me["board"][(i, j)] = self._board[i][j], soldier_info
        return stored_info_me

    def restore(self, stored_info_me):
        self._score = stored_info_me["score"]
        self._done = stored_info_me["done"]
        self._winner = stored_info_me["winner"]
        self._dead = stored_info_me["dead"]
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                soldier, soldier_info = stored_info_me["board"][(i, j)]
                soldier.restore(soldier_info)
                self._board[i][j] = soldier

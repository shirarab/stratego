from typing import Set
from copy import deepcopy
from constants import Degree, DEAD_SOLDIERS, BOARD_SIZE, OP_COLOR
from constants import Color, Direction
from knowledge_base import KnowledgeBase
from soldier import Soldier
from action import Action


class GameState(object):
    def __init__(self, board, score=0, done=False, dead=None, kb_info=None, can_op_soldier_be_flag=None):
        """
        Create a new instance of game state
        
        Attributes:
            self._board : Two-dimensional array of Soldier objects
            self._score :
            self._done : Is the game over (flag revealed)
            self._dead : Dead soldiers for each color
            self._winner : winning color
            self.knowledge_bases : dict with two knowledge base objects (one for each color)
        """
        self._board = board
        self._score = score
        self._done = done

        self.can_op_soldier_be_flag = can_op_soldier_be_flag  # can be None
        if dead is None:
            self._dead = {Color.RED: DEAD_SOLDIERS.copy(), Color.BLUE: DEAD_SOLDIERS.copy()}
        else:
            self._dead = dead
        self._winner = Color.GRAY

        self.knowledge_bases = {Color.RED: KnowledgeBase(color=Color.RED, board=self._board),
                                Color.BLUE: KnowledgeBase(color=Color.BLUE, board=self._board)}
        if kb_info is not None:
            for col in self.knowledge_bases:
                self.knowledge_bases[col].restore_kb(kb_info[col])

    @property
    def done(self):
        return self._done

    @done.setter
    def done(self, value):
        self._done = value

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, value):
        self._score = value

    @property
    def board(self):
        return self._board

    @property
    def dead(self):
        return self._dead

    @property
    def winner(self):
        return self._winner

    @winner.setter
    def winner(self, value):
        self._winner = value

    def get_soldier_at_x_y(self, x, y) -> Soldier:
        if 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE:
            return self.board[x][y]
        return None

    def get_knowledge_base(self, color: Color):
        return self.knowledge_bases[color]

    def get_soldier_legal_actions(self, soldier: Soldier, assumed_degree: Degree = None):
        legal_actions = set()
        if assumed_degree is None:
            assumed_degree = soldier.degree
        if assumed_degree in {Degree.BOMB, Degree.FLAG, Degree.EMPTY, Degree.WATER}:
            return legal_actions
        if assumed_degree == Degree.TWO:
            for direction in Direction:
                for num_steps in range(1, BOARD_SIZE):
                    is_good_move, next_is_empty = self._is_legal_move(direction, soldier, num_steps)
                    if is_good_move:
                        legal_actions.add(Action(soldier, direction, num_steps))
                    if (not is_good_move) or (not next_is_empty):
                        break  # can't jump over illegal step
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

    def shot_and_dead(self, killed: Soldier, winner: Soldier, keep_record=True):
        """
        Kill the given soldier and expose the identity of the winning soldier.
        """
        killed.kill_me()
        self.dead[killed.color][killed.degree] += 1
        winner.set_show_me()
        if keep_record:
            self.knowledge_bases[killed.color].remove_soldier_from_kb(killed)  # delete dead soldier from KB
            if killed.degree != winner.degree:
                self.knowledge_bases[winner.color].add_new_singleton(winner, winner.degree)

    def get_successor(self, action: Action):
        # check if we need to record in kb
        self.apply_action(action, keep_record_in_kb=False)
        return self

    def apply_action(self, action: Action, keep_record_in_kb=True):
        """
        keep_record_in_kb should be set to False if this action is part of a search tree and not an actual game
        action (this is important especially for opponent actions, as the guessed actions can lead to KB contradictions)
        """
        # we assume that action can only be legal
        if self._done or action is None:
            return

        if keep_record_in_kb:
            self.record_action_in_kb(action)

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
                self.shot_and_dead(opponent, action.soldier, keep_record_in_kb)
                action.soldier.set_position(op_x, op_y)
            else:
                self.shot_and_dead(action.soldier, opponent, keep_record_in_kb)
        elif opponent.degree == Degree.FLAG:
            instead_opponent = action.soldier
            self.shot_and_dead(opponent, action.soldier, keep_record_in_kb)
            action.soldier.set_position(op_x, op_y)
            self._done = True
            self._winner = action.soldier.color
        elif opponent.degree == Degree.TEN and action.soldier.degree == Degree.ONE:
            instead_opponent = action.soldier
            self.shot_and_dead(opponent, action.soldier, keep_record_in_kb)
            action.soldier.set_position(op_x, op_y)
        elif opponent.degree > action.soldier.degree:
            self.shot_and_dead(action.soldier, opponent, keep_record_in_kb)
        elif opponent.degree < action.soldier.degree:
            instead_opponent = action.soldier
            self.shot_and_dead(opponent, action.soldier, keep_record_in_kb)
            action.soldier.set_position(op_x, op_y)
        elif opponent.degree == action.soldier.degree:
            instead_opponent = Soldier(Degree.EMPTY, sol_x, sol_y, Color.GRAY)
            self.shot_and_dead(action.soldier, opponent, keep_record_in_kb)
            self.shot_and_dead(opponent, action.soldier, keep_record_in_kb)
        self._board[sol_x][sol_y] = instead_me
        self._board[op_x][op_y] = instead_opponent

    def record_action_in_kb(self, action):
        # if the number of steps > 1 we can update this to be degree 2 (exposed in the knowledge base)
        if action.num_steps > 1:
            self.knowledge_bases[action.soldier.color].add_new_singleton(action.soldier, Degree.TWO)
        self.knowledge_bases[action.soldier.color].record_movable_soldier(action.soldier)

    def get_unblocked_soldiers(self, color: Color) -> Set[Soldier]:
        """
        Return a set of all soldiers from this color which have any available moving directions (directions that
        are not blocked by soldiers of the same color, water/edges/etc.)
        """
        soldiers_set = set()
        free_colors = {OP_COLOR[color], Color.GRAY}
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                if self._board[r][c].color == color:
                    surrounding_indices = {(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)}
                    for (x, y) in surrounding_indices:
                        neighbor = self.get_soldier_at_x_y(x, y)
                        if neighbor and neighbor.color in free_colors:
                            soldiers_set.add(self._board[r][c])
        return soldiers_set

    def store(self):
        stored_info_me = {"score": self._score, "done": self._done, "winner": self._winner,
                          "kbs": dict(),
                          "dead": deepcopy(self._dead), "board": dict()}
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                soldier_info = self._board[i][j].store()
                stored_info_me["board"][(i, j)] = self._board[i][j], soldier_info
        for color in OP_COLOR:
            stored_info_me["kbs"][color] = self.knowledge_bases[color].store_kb()
        return stored_info_me

    def restore(self, stored_info_me):
        self._score = stored_info_me["score"]
        self._done = stored_info_me["done"]
        self._winner = stored_info_me["winner"]
        self._dead = stored_info_me["dead"]
        for color in OP_COLOR:
            self.knowledge_bases[color].restore_kb(stored_info_me["kbs"][color])
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                soldier, soldier_info = stored_info_me["board"][(i, j)]
                soldier.restore(soldier_info)
                self._board[i][j] = soldier

from collections import Counter
from copy import copy, deepcopy
from typing import Dict

from constants import Color, Degree, BOARD_SIZE, PLAYER_SOLDIER_DEGREES_LIST, SOLDIER_COUNT_FOR_EACH_DEGREE, UNMOVABLE
# from game_state import GameState
from soldier import Soldier


class KnowledgeBaseContradiction(Exception):
    pass


class KnowledgeBase(object):
    def __init__(self, color: Color, board):
        """
        Create a new knowledge base (all options possible) from given game state and color.
        
        Attributes:
            self._color : color of the player this kb is about
            self._soldier_knowledge_base: KB with soldier as keys, degrees as values
            self._degree_knowledge_base : KB with degree as key and soldiers as values
            self._singletons : count how many soldiers are identified for sure as a certain degree
            self._do_update : bool saying if new information that requires updating has been exposed
            self._degrees_to_update : set of degrees that need updating
        """
        self._color = color
        self._soldier_knowledge_base = dict()  # KB with soldier as keys, degrees as values
        self._degree_knowledge_base = {deg: [] for deg in SOLDIER_COUNT_FOR_EACH_DEGREE}
        self._singletons = Counter()
        self._do_update = False
        self._degrees_to_update = set()
        # init the knowledge base with full options for each opponent soldier:
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if board[i][j].color == self._color:
                    for deg in SOLDIER_COUNT_FOR_EACH_DEGREE:
                        self._degree_knowledge_base[deg].append(board[i][j])
                    self._soldier_knowledge_base[board[i][j]] = PLAYER_SOLDIER_DEGREES_LIST.copy()
    
    def update(self, game_state):
        """
        Get the color of a player and update its knowledge base according to game rules constraints, such as total
        number of each type of soldier
        """
        while self._do_update:
            self._do_update = False
            new_degrees_to_update = set()
            for degree in self._degrees_to_update:
                dead_count = game_state.dead[self._color][degree]
                on_board_count = SOLDIER_COUNT_FOR_EACH_DEGREE[degree] - dead_count
                # if we already detected all the soldiers of this degree
                if on_board_count == self._singletons[degree]:
                    for soldier in self._degree_knowledge_base[degree].copy():
                        if len(self._soldier_knowledge_base[soldier]) > 1:
                            self._soldier_knowledge_base[soldier].remove(degree)
                            self._degree_knowledge_base[degree].remove(soldier)
                            # if by removing the degree from the KB we created a new singleton, run another iteration
                            if len(self._soldier_knowledge_base[soldier]) == 1:
                                new_single_degree = self._soldier_knowledge_base[soldier][0]
                                self._singletons[new_single_degree] += 1
                                self._do_update = True
                                new_degrees_to_update.add(new_single_degree)
                            if len(self._soldier_knowledge_base[soldier]) == 0:
                                raise KnowledgeBaseContradiction(f"No options for soldier {soldier}")
                elif on_board_count < self._singletons[degree]:
                    raise KnowledgeBaseContradiction(
                        f"{self._singletons[degree]} soldiers were identified with degree {degree}, but only "
                        f"{on_board_count} soldiers are supposed to be on the board"
                    )
                # if the amount of soldiers that can have this degree equals to the total amount
                if len(self._degree_knowledge_base[degree]) == on_board_count:
                    for optional_soldier in self._degree_knowledge_base[degree]:
                        # self._soldier_knowledge_base[optional_soldier] = [degree]
                        self.add_new_singleton(optional_soldier, degree)
                # if the options for the degree are LESS THAN the number we should have on the board, contradiction
                elif len(self._degree_knowledge_base[degree]) < on_board_count:
                    raise KnowledgeBaseContradiction(f"Not enough optional soldiers for degree {degree}")
                self._degrees_to_update = new_degrees_to_update
    
    def remove_soldier_from_kb(self, soldier: Soldier) -> bool:
        """
        Remove a soldier from the KB
        should be called when a soldier dies, since the KB should only contain info for living soldiers.
        Returns true if soldier was found and removed successfully, false if not found in the KB.
        """
        if soldier not in self._soldier_knowledge_base:
            return False
        if len(self._soldier_knowledge_base[soldier]) == 1:  # if removing a singleton, update the counter
            self._singletons[soldier.degree] -= 1
        self._soldier_knowledge_base.pop(soldier, None)
        for deg in SOLDIER_COUNT_FOR_EACH_DEGREE:
            if soldier in self._degree_knowledge_base[deg]:
                self._degree_knowledge_base[deg].remove(soldier)
        return True
    
    def add_new_singleton(self, soldier: Soldier, deg: Degree):
        """
        Add the info for a new soldier that was detected with certainty
        """
        if len(self._soldier_knowledge_base[soldier]) > 1:
            self._do_update = True
            self._degrees_to_update.add(deg)
            self._soldier_knowledge_base[soldier] = [deg]
            self._singletons[deg] += 1
        elif len(self._soldier_knowledge_base[soldier]) == 1 and self._soldier_knowledge_base[soldier][0] != deg:
            raise KnowledgeBaseContradiction(
                f"Tried to add singleton of degree {deg}, "
                f"but soldier is already a singleton of degree {self._soldier_knowledge_base[soldier][0]} "
                f"(real degree is {soldier.degree})"
            )
        elif deg not in self._soldier_knowledge_base[soldier]:
            raise KnowledgeBaseContradiction(f"Tried to creat singleton of degree {deg}, but the current options for "
                                             f"this soldier are: {self._soldier_knowledge_base[soldier]}")
    
    def record_movable_soldier(self, soldier: Soldier):
        """
        If a soldier has moved, record that it can't be bomb or flag
        """
        for unmovable_degree in UNMOVABLE:
            if unmovable_degree in self._soldier_knowledge_base[soldier]:
                self._degrees_to_update.add(unmovable_degree)
                self._do_update = True
                self._soldier_knowledge_base[soldier].remove(unmovable_degree)
                if soldier in self._degree_knowledge_base[unmovable_degree]:
                    self._degree_knowledge_base[unmovable_degree].remove(soldier)
        # check if we created a singleton as a result of removing options
        if len(self._soldier_knowledge_base[soldier]) == 1:
            self.add_new_singleton(soldier, self._soldier_knowledge_base[soldier][0])
        if len(self._soldier_knowledge_base[soldier]) == 0:
            raise KnowledgeBaseContradiction(f"No options left for soldier {soldier}")
    
    def option_count_for_soldier(self, soldier: Soldier):
        return len(self._soldier_knowledge_base[soldier])
    
    def get_options_for_soldier(self, soldier: Soldier):
        return self._soldier_knowledge_base[soldier].copy()
    
    def store_kb(self):
        store_soldier_kb, store_degree_kb = dict(), dict()
        for sol in self._soldier_knowledge_base:
            store_soldier_kb[sol] = copy(self._soldier_knowledge_base[sol])
        for deg in self._degree_knowledge_base:
            store_degree_kb[deg] = copy(self._degree_knowledge_base[deg])
        data = self._color, store_soldier_kb, store_degree_kb, \
            deepcopy(self._singletons), self._do_update, set(self._degrees_to_update)
        return data
    
    def restore_kb(self, stored_info):
        (self._color, self._soldier_knowledge_base, self._degree_knowledge_base, self._singletons, self._do_update,
         self._degrees_to_update) = stored_info
    
    def get_living_soldiers(self):
        return list(self._soldier_knowledge_base.keys())
    
    def is_assignment_consistent(self, assignment: Dict[Soldier, Degree], game_state) -> bool:
        """
        Receives a partial assignment to soldiers, returns whether it is consistent with the current knowledge base
        """
        current_kb_data = self.store_kb()
        # temp_state = game_state.clone()
        is_consistent = True
        try:
            for sol, deg in assignment.items():
                self.add_new_singleton(sol, deg)
            self.update(game_state)
        except KnowledgeBaseContradiction:
            is_consistent = False
        self.restore_kb(current_kb_data)
        return is_consistent
    
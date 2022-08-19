import random
from copy import deepcopy, copy
from typing import Set

from action import Action
from constants import Color, PLAYER_SOLDIER_DEGREES_LIST, SOLDIER_COUNT_FOR_EACH_DEGREE
from game_state import GameState


def null_get_legal_actions_opponent(game_state: GameState, color: Color) -> Set[Action]:
    return set()


def legal_actions_from_subset_guess(game_state: GameState, color: Color) -> Set[Action]:
    """
    Guess an assignment for the movable soldiers, make sure that it's consistent with the KB, and return set of
    actions based on that assignment.
    """
    game_state.get_knowledge_base(color).update()
    movable_soldiers = game_state.get_unblocked_soldiers(color)
    found_assignment = False
    assignment = dict()
    unknown_soldiers = []
    degree_weights = [SOLDIER_COUNT_FOR_EACH_DEGREE[d] - game_state.dead[color][d] for d in PLAYER_SOLDIER_DEGREES_LIST]
    for soldier in movable_soldiers:
        if soldier.show_me:
            assignment[soldier] = soldier.degree
        else:
            unknown_soldiers.append(soldier)
    while not found_assignment:
        guessed_degrees = random.choices(PLAYER_SOLDIER_DEGREES_LIST, weights=degree_weights, k=len(unknown_soldiers))
        assignment.update(dict(zip(unknown_soldiers, guessed_degrees)))
        found_assignment = game_state.get_knowledge_base(color).is_assignment_consistent(assignment, game_state)
    actions = set()
    for soldier, degree in assignment.items():
        actions |= game_state.get_soldier_legal_actions(soldier, assumed_degree=degree)
    return actions


def naive_opp_get_successor(game_state: GameState, action: Action, color: Color) -> GameState:
    # prev_info = game_state.store()
    game_state.apply_action(action, keep_record_in_kb=False)
    return game_state
    

def do_not_use_me_ever(game_state: GameState, color: Color) -> Set[Action]:
    return game_state.get_legal_actions(color)


def null_get_successor_opponent(game_state: GameState, action: Action, color: Color) -> GameState:
    return game_state.get_successor(action)

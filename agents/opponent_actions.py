import itertools
import random
from copy import deepcopy, copy
from typing import Set, List, Tuple

from action import Action
from constants import Color, PLAYER_SOLDIER_DEGREES_LIST, SOLDIER_COUNT_FOR_EACH_DEGREE, Degree
from game_state import GameState
from soldier import Soldier


def null_get_legal_actions_opponent(game_state: GameState, color: Color) -> Set[Action]:
    return set()


def legal_actions_from_subset_guess(game_state: GameState, color: Color) -> Set[Action]:
    """
    Guess an assignment for the movable soldiers, make sure that it's consistent with the KB, and return set of
    actions based on that assignment.
    """
    # game_state.get_knowledge_base(color).update(game_state)

    degree_pool = get_degree_pool(color, game_state)
    random.shuffle(degree_pool)
    exposed_soldiers, unknown_soldiers = divide_movable_soldiers(color, game_state)
    found_assignment = False
    assignment = dict()
    for guessed_degrees in itertools.permutations(degree_pool, len(unknown_soldiers)):
        # guessed_degrees = random.choices(PLAYER_SOLDIER_DEGREES_LIST, weights=degree_weights, k=len(unknown_soldiers))
        assignment = dict(zip(unknown_soldiers, guessed_degrees))
        found_assignment = game_state.get_knowledge_base(color).is_assignment_consistent(assignment, game_state)
        if found_assignment:
            break
    if not found_assignment:
        # raise ValueError("no possible assignment")
        for x in unknown_soldiers:
            assignment[x] = Degree.FOUR
    actions = set()
    for soldier, degree in assignment.items():
        actions |= game_state.get_soldier_legal_actions(soldier, assumed_degree=degree)
    for soldier in exposed_soldiers:
        actions |= game_state.get_soldier_legal_actions(soldier)
    return actions


def divide_movable_soldiers(color, game_state) -> Tuple[List[Soldier], List[Soldier]]:
    """
    Returns all the movable soldier from given color, divided into two lists: exposed and unknown
    """
    movable_soldiers = game_state.get_unblocked_soldiers(color)
    unknown_soldiers = []
    exposed_soldiers = []
    for soldier in movable_soldiers:
        if game_state.get_knowledge_base(color).is_soldier_exposed(soldier):
            exposed_soldiers.append(soldier)
        else:
            unknown_soldiers.append(soldier)
    return exposed_soldiers, unknown_soldiers


def get_degree_pool(color, game_state) -> List[Degree]:
    """
    Return pool of available degrees (all degrees present on the board, each degree appears as many times as it is
    present on the board)
    """
    on_board_counts = [SOLDIER_COUNT_FOR_EACH_DEGREE[d] -
                       game_state.dead[color][d] -
                       game_state.get_knowledge_base(color).get_singleton_count(d)
                       for d in PLAYER_SOLDIER_DEGREES_LIST]
    degree_pool = []
    for degree, count in zip(PLAYER_SOLDIER_DEGREES_LIST, on_board_counts):
        for i in range(count):
            degree_pool.append(degree)
    return degree_pool


def naive_opp_get_successor(game_state: GameState, action: Action, color: Color) -> GameState:
    # prev_info = game_state.store()
    game_state.apply_action(action, keep_record_in_kb=False)
    return game_state
    

def get_real_legal_actions(game_state: GameState, color: Color) -> Set[Action]:
    """
    Real legal actions based on actual soldier degrees. Should never be called in the case of hidden information.
    """
    return game_state.get_legal_actions(color)


def null_get_successor_opponent(game_state: GameState, action: Action, color: Color) -> GameState:
    return game_state.get_successor(action)

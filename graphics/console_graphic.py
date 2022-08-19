from typing import Set, Tuple, List

from constants import Degree, Color, Direction
from game_state import GameState
from graphics.stratego_graphic import StrategoGraphic, RED, BLUE, DEGREE_TO_STR, DIRECTION_MAP
from soldier import Soldier


class ConsoleGraphic(StrategoGraphic):

    def show_board(self, game_state: GameState):
        if self.num_players_to_show == 0:
            return
        print()
        print()
        print()
        print("------" * self.board_size)
        for i in range(self.board_size):
            line_to_print = "|"
            for j in range(self.board_size):
                square_to_print = " "
                soldier = game_state.get_soldier_at_x_y(i, j)
                degree = self.degree_to_print(soldier.degree)
                if soldier.color == Color.RED:
                    # square_to_print += RED + degree + ' |'
                    square_to_print += RED + degree
                    if soldier.show_me:
                        square_to_print += '*|'
                    else:
                        square_to_print += ' |'
                elif soldier.color == Color.BLUE:
                    square_to_print += BLUE
                    if self.num_players_to_show == 2 or soldier.show_me:
                        square_to_print += degree + ' |'
                    else:
                        square_to_print += '  ' + ' |'
                else:
                    square_to_print += ' ' + degree + ' |'
                line_to_print += square_to_print
            print(line_to_print)
            print("------" * self.board_size)

    def degree_to_print(self, degree: Degree):
        return DEGREE_TO_STR[degree]

    def ask_for_initial_position(self, soldiers: List[Soldier], positions: Set[Tuple[int, int]],
                                 color: Color) -> Tuple[Soldier, int, int]:
        # soldier, x, y
        print("Please choose a soldier index and a position from:")
        print("soldiers:", end=' ')
        for i, s in enumerate(soldiers):
            end = '\n' if (i + 1) % 10 == 0 else ', '
            print(f"{i}:{DEGREE_TO_STR[s.degree]}", end=end)
        print("positions:", end=' ')
        for i, p in enumerate(positions):
            end = '\n' if (i + 1) % 10 == 0 else ', '
            print(p, end=end)
        print()
        s_ind, x, y = input("index x y: ").split()
        print()
        return soldiers[int(s_ind)], int(x), int(y)

    def ask_for_action(self, game_state: GameState) -> Tuple[int, int, Direction, int]:
        # x, y, direction, num_steps
        x, y, direction, num_steps = input("x y direction num_steps: ").split()
        return int(x), int(y), DIRECTION_MAP[direction.lower()], int(num_steps)

    def game_over(self, color: Color, score: int = 0):
        print(f"GAME OVER winner is {color.name} with score {score}")

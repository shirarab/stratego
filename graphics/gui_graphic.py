from typing import List, Set, Tuple
from constants import Degree, Color, DEAD_SOLDIERS, Direction
from game_state import GameState
from graphics.stratego_graphic import StrategoGraphic, DEGREE_TO_STR
from soldier import Soldier

from graphics.gui_graphics.texts import *
from graphics.gui_graphics.styles import *
from tkinter import messagebox, PhotoImage

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 580
SOLDIERS_ROWS = 4

SOLDIER_COLOR_TO_STYLE = {
    Color.GRAY: EMPTY_SOLDIER_STYLE,
    Color.WATER: WATER_SOLDIER_STYLE,
    Color.BLUE: BLUE_SOLDIER_STYLE,
    Color.RED: RED_SOLDIER_STYLE
}

SIDE_SOLDIERS_DEGREES = [
    [Degree.BOMB, Degree.BOMB, Degree.BOMB, Degree.BOMB, Degree.BOMB,
     Degree.BOMB, Degree.ONE, Degree.TWO, Degree.TWO, Degree.TWO],
    [Degree.TWO, Degree.TWO, Degree.TWO, Degree.TWO, Degree.TWO,
     Degree.THREE, Degree.THREE, Degree.THREE, Degree.THREE, Degree.THREE],
    [Degree.FOUR, Degree.FOUR, Degree.FOUR, Degree.FOUR, Degree.FIVE,
     Degree.FIVE, Degree.FIVE, Degree.FIVE, Degree.SIX, Degree.SIX],
    [Degree.SIX, Degree.SIX, Degree.SEVEN, Degree.SEVEN, Degree.SEVEN,
     Degree.EIGHT, Degree.EIGHT, Degree.NINE, Degree.TEN, Degree.FLAG]
]


class GuiGraphic(StrategoGraphic):
    def __init__(self, board_size, num_players_to_show: int = 0):
        super().__init__(board_size, num_players_to_show)
        if num_players_to_show == 0:
            return
        self._board = self._get_initial_board()
        self._board_buttons = [[None for j in range(self.board_size)] for i in range(self.board_size)]
        self._board_red = [[False for j in range(self.board_size)] for i in range(SOLDIERS_ROWS)]
        self._board_buttons_red = [[None for j in range(self.board_size)] for i in range(SOLDIERS_ROWS)]
        self._board_blue = [[False for j in range(self.board_size)] for i in range(SOLDIERS_ROWS)]
        self._board_buttons_blue = [[None for j in range(self.board_size)] for i in range(SOLDIERS_ROWS)]
        self._root = tk.Tk()
        self._root.title(ROOT_TITLE)
        self._root.resizable(False, False)
        self._root.geometry(f"{SCREEN_WIDTH}x{SCREEN_HEIGHT}")
        self._build_ui()
        self._first_soldier: Soldier = None
        self._second_soldier: Soldier = None
        self._side_soldier: Soldier = None
        self._first_clicked = tk.BooleanVar()
        self._second_clicked = tk.BooleanVar()
        self._side_clicked = tk.BooleanVar()
        self._red_flag_is_first_time = True
        self._blue_flag_is_first_time = True

    @property
    def board(self):
        return self._board

    def _get_initial_board(self):
        board = [[Soldier(Degree.EMPTY, i, j, Color.GRAY) for j in range(self.board_size)]
                 for i in range(self.board_size)]
        for i in range(2):
            for j in range(self.board_size):
                if j in {2, 3, 6, 7}:
                    board[4 + i][j] = Soldier(Degree.WATER, 4 + i, j, Color.WATER)
        return board

    def _get_initial_soldiers_board(self, color: Color):
        pass

    def _build_ui(self):
        self._create_frames()
        self._pack_frames()
        self._create_cells()
        self._create_all_soldiers_cells(self._red_board_frame, self._board_buttons_red)
        self._create_all_soldiers_cells(self._blue_board_frame, self._board_buttons_blue)
        self._add_widgets()
        # self.animate_message()
        # self.animate_buttons()

    def _create_frames(self):
        """ Creates GUI's Frames """
        self._background_frame = tk.Frame(self._root, **MAIN_STYLE, bd=5)
        self._screen_frame = tk.Frame(self._background_frame, **NORMAL_BG, height=TITLE_FRAME_SIZE)
        self._outline_board_frame = tk.Frame(self._background_frame, height=OUTLINE_BOARD_FRAME_SIZE,
                                             width=OUTLINE_BOARD_FRAME_SIZE, **OUTLINE_BOARD_FRAME_STYLE)
        self._board_frame = tk.Frame(self._outline_board_frame, width=BOARD_FRAME_SIZE, height=BOARD_FRAME_SIZE)

        # right side
        self._outline_soldiers_frame = tk.Frame(self._background_frame, highlightthickness=1,
                                                **OUTLINE_SOLDIERS_FRAME_STYLE)
        self._outline_red_frame = tk.Frame(self._outline_soldiers_frame, **OUTLINE_RED_FRAME_STYLE)
        self._outline_blue_frame = tk.Frame(self._outline_soldiers_frame, **OUTLINE_BLUE_FRAME_STYLE)
        self._red_board_frame = tk.Frame(self._outline_red_frame, **OUTLINE_RED_FRAME_STYLE)
        self._blue_board_frame = tk.Frame(self._outline_blue_frame, **OUTLINE_BLUE_FRAME_STYLE)

    def _pack_frames(self):
        """ Packs frames """
        self._background_frame.pack(fill=tk.BOTH, expand=True)
        self._outline_soldiers_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=False)
        self._outline_soldiers_frame.pack_propagate(False)
        self._screen_frame.pack(fill=tk.BOTH, expand=True)
        self._screen_frame.pack_propagate(False)
        self._outline_board_frame.pack(side=tk.LEFT)
        self._board_frame.pack(side=tk.LEFT, expand=False)
        # self._outline_board_frame.place(x=SCREEN_WIDTH/3-OUTLINE_BOARD_FRAME_SIZE/3,
        #                                 y=SCREEN_HEIGHT/2-OUTLINE_BOARD_FRAME_SIZE/3)
        self._board_frame.grid_propagate(False)

        # right side
        self._outline_red_frame.pack(side=tk.TOP)
        self._red_board_frame.pack()
        # self._red_board_frame.grid_propagate(False)
        self._outline_blue_frame.pack(side=tk.BOTTOM)
        self._blue_board_frame.pack()
        # self._blue_board_frame.grid_propagate(False)

        # self._soldiers_frame.pack(fill=tk.X)

    def _create_cells(self):
        """ Creates Boarder's cells, containing buttons """
        for i in range(self.board_size):
            tk.Grid.rowconfigure(self._board_frame, i, weight=1)

        for j in range(self.board_size):
            tk.Grid.columnconfigure(self._board_frame, j, weight=1)

        for i in range(self.board_size):
            for j, soldier in enumerate(self.board[i]):
                self._make_button(soldier, i, j)

    def _create_all_soldiers_cells(self, frame_to_put_on, table):
        for i in range(SOLDIERS_ROWS):
            tk.Grid.rowconfigure(frame_to_put_on, i, weight=1)

        for j in range(self.board_size):
            tk.Grid.columnconfigure(frame_to_put_on, j, weight=1)

        for i in range(SOLDIERS_ROWS):
            for j in range(self.board_size):
                self._make_side_soldiers_button(i, j, frame_to_put_on, table)

    def _add_widgets(self):
        """ Adds widgets to frames """
        # Game title:
        self._boggle_label = tk.Label(self._screen_frame, text=ROOT_TITLE,
                                      **TITLE_LABEL_STYLE)
        self._boggle_label.pack(side=tk.TOP, pady=(0, 0), expand=True)

    def _make_button(self, soldier: Soldier, row: int, col: int):
        """ Creates a single button """
        btn_style, text = self._get_soldier_btn_style_and_text(soldier)
        button = tk.Button(self._board_frame, text=text, **btn_style)
        button.config(command=lambda: self._click_btn_soldier_selected_pos(row, col))
        button.grid(row=row, column=col, rowspan=1, columnspan=1,
                    sticky=tk.NSEW, pady=1, padx=1)
        self._board_buttons[row][col] = button

    def _make_side_soldiers_button(self, i, j, frame_to_put_on, table):
        btn_style, text = EMPTY_SOLDIER_STYLE, ""
        button = tk.Button(frame_to_put_on, text=text, **btn_style)
        button.config(command=lambda: self._click_btn_side_soldier_selected_pos(i, j))
        button.grid(row=i, column=j, rowspan=1, columnspan=1,
                    sticky=tk.NSEW, pady=1, padx=1)
        table[i][j] = button

    def _click_btn_side_soldier_selected_pos(self, i, j):
        self._side_soldier = SIDE_SOLDIERS_DEGREES[i][j], i, j
        self._side_clicked.set(True)

    def _get_soldier_btn_style_and_text(self, soldier: Soldier):
        text = DEGREE_TO_STR[soldier.degree]
        btn_style = SOLDIER_COLOR_TO_STYLE[soldier.color]
        if soldier.color in {Color.WATER, Color.GRAY}:
            text = ""
        if soldier.color == Color.BLUE and self.num_players_to_show == 1 and not soldier.show_me:
            text = ""
        if soldier.color == Color.RED and self.num_players_to_show > 0 and soldier.show_me:
            text += "*"
        if soldier.color == Color.BLUE and self.num_players_to_show == 2 and soldier.show_me:
            text += "*"

        return btn_style, text

    def reset_first_second_soldier_click(self):
        self._first_soldier = None
        self._first_clicked.set(False)
        self._second_soldier = None
        self._second_clicked.set(False)

    def _click_btn_soldier_selected_pos(self, row, col):
        if self._first_soldier is None:
            self._first_soldier = self.board[row][col]
            self._first_clicked.set(True)
        elif self._second_soldier is None:
            self._second_soldier = self.board[row][col]
            self._second_clicked.set(True)
        else:
            self.reset_first_second_soldier_click()

    def _update_board(self):
        for i in range(self.board_size):
            for j, soldier in enumerate(self.board[i]):
                btn = self._board_buttons[i][j]
                btn_style, text = self._get_soldier_btn_style_and_text(self.board[i][j])
                btn.configure(state=tk.NORMAL, **btn_style, text=text)

    def _update_side_board(self, color: Color, dead=DEAD_SOLDIERS):
        board = self._board_red if color == Color.RED else self._board_blue
        btn_board = self._board_buttons_red if color == Color.RED else self._board_buttons_blue
        # do not delete
        # print()
        # print("dead:", dead)
        # print()
        cpy_dead = dead.copy()
        for i in range(SOLDIERS_ROWS):
            for j in range(self.board_size):
                degree = SIDE_SOLDIERS_DEGREES[i][j]
                if cpy_dead[degree] > 0:
                    board[i][j] = True
                    cpy_dead[degree] -= 1
                btn_style, text = EMPTY_SOLDIER_STYLE, ""
                if board[i][j] == True:
                    btn_style = RED_SOLDIER_STYLE if color == Color.RED else BLUE_SOLDIER_STYLE
                    text = DEGREE_TO_STR[degree]
                btn_board[i][j].configure(state=tk.NORMAL, **btn_style, text=text)

    def show_board(self, game_state: GameState):
        """ Runs the main loop """
        self._board = game_state.board
        self._update_board()
        self._update_side_board(Color.RED, game_state.dead[Color.RED])
        self._update_side_board(Color.BLUE, game_state.dead[Color.BLUE])
        self._root.update_idletasks()
        self._root.update()

    def ask_for_initial_position(self, soldiers: List[Soldier], positions: Set[Tuple[int, int]],
                                 color: Color) -> Tuple[Soldier, int, int]:
        # soldier, x, y
        board = self._board_red if color == Color.RED else self._board_blue
        flag = self._red_flag_is_first_time if color == Color.RED else self._blue_flag_is_first_time
        if flag:
            if color == Color.RED:
                self._red_flag_is_first_time = False
            else:
                self._blue_flag_is_first_time = False
            for i in range(SOLDIERS_ROWS):
                for j in range(self.board_size):
                    board[i][j] = True

        self._update_side_board(color)
        degree, i, j, x, y = None, -1, -1, -1, -1
        self._first_soldier = None
        self._second_soldier = None
        self._root.waitvar(self._side_clicked)
        self._first_soldier = None
        self._second_soldier = None
        self._root.waitvar(self._first_clicked)
        if self._first_soldier is not None and self._side_soldier is not None:
            x, y = self._first_soldier.x, self._first_soldier.y
            degree, i, j = self._side_soldier
        # if i >= 0 and j >= 0:
        #     board[i][j] = False
        # # do not delete
        # print("side:", x, y)
        self.reset_first_second_soldier_click()
        self._side_soldier = None
        self._side_clicked.set(False)

        soldier = None
        for s in soldiers:
            if s.degree == degree:
                soldier = s
                break
        m = x
        if soldier.color == Color.BLUE:
            m = self.board_size - 1 - x
        if (m, y) in positions and board[i][j]:
            board[i][j] = False
            self.board[x][y] = soldier
            self._update_board()
            return soldier, m, y
        return None, -1, -1

    def _get_click_direction(self, x, y, x_sec, y_sec):
        if x == x_sec and y < y_sec:
            return Direction.RIGHT, y_sec - y
        if x == x_sec and y > y_sec:
            return Direction.LEFT, y - y_sec
        if x < x_sec and y == y_sec:
            return Direction.UP, x_sec - x
        if x > x_sec and y == y_sec:
            return Direction.DOWN, x - x_sec
        return None, 0

    def ask_for_action(self, game_state: GameState) -> Tuple[int, int, Direction, int]:
        # x, y, direction, num_steps
        self.reset_first_second_soldier_click()
        # print("ask_for_action", self._first_soldier, self._second_soldier)
        x, y, direction, num_steps = 0, 0, None, 0
        x_sec, y_sec = 0, 0
        self._root.waitvar(self._first_clicked)
        self._root.waitvar(self._second_clicked)
        # print("ask_for_action after clicked", self._first_soldier, self._second_soldier)
        if self._first_soldier is not None and self._second_soldier is not None:
            x, y = self._first_soldier.x, self._first_soldier.y
            x_sec, y_sec = self._second_soldier.x, self._second_soldier.y
        direction, num_steps = self._get_click_direction(x, y, x_sec, y_sec)
        # # do not delete
        # print("chosen: x", x, "y", y, "dir", direction, "num steps", num_steps)
        # print("x_sec", x_sec, "y_sec", y_sec)
        self._first_soldier = None
        self._second_soldier = None
        self._first_clicked.set(False)
        self._second_clicked.set(False)
        return x, y, direction, num_steps

    def game_over(self, color: Color, score: int = 0):
        """ Ends the game """
        # self._model.stop_game()
        # message = self._create_end_message()
        message = f"GAME OVER winner is {color.name} with score {score}"
        messagebox.showinfo(GAME_OVER_TITLE, message)
        # play_again = messagebox.askyesno(TIME_UP, message)
        # if play_again:
        #     if self._start_btn_command:
        #         self._start_btn_command()
        # else:
        self._root.destroy()

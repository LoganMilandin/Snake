from tkinter import *
from PIL.ImageTk import PhotoImage
from PIL import Image
from cell import Cell
from snake import Snake
from direction import Direction

import random as rand


MENU_WIDTH = 150
GAME_WIDTH = 500
GAME_GRID_DIMENSIONS = 20
SQUARE_WIDTH = GAME_WIDTH / GAME_GRID_DIMENSIONS
SCORE_FRAME_HEIGHT = 50
INVERSE_PROP_CONSTANT = 2000
TIME_BETWEEN_MOVES = int(INVERSE_PROP_CONSTANT / GAME_GRID_DIMENSIONS)
SQUARE_OUTLINE_COLOR = "#888888"
GAME_BACKGROUND_COLOR = "#123456"
SNAKE_COLOR = "#45d66b"
MENU_COLOR = "#888888"
BORDER_COLOR = "#222222"


class Board(Canvas):
    """Represents the canvas with the blue background appearing on the left of the screen.

    Args:
        Canvas - the basic drawing panel provided by tkinter
    """

    def __init__(self, parent=None, score_label=None, **kwargs):
        """constructs a new game board (only called once, not on each new game)

        Args:
            parent (widget) the frame/window this canvas belongs to
            score_label (Label) the label for the snake's size
            **kwargs (arg list) other optional arguments for canvas
        """

        Canvas.__init__(self, parent, kwargs)
        self.pack(side=BOTTOM)

        self.changedDirectionThisTurnAlready = False
        self.initialize_directions()
        self.bind_all("<Key>", self.change_direction)
        self.score_label = score_label

        self.initialize_empty_cells()
        self.draw_all_cells()
        self.initialize_snake(score_label)
        self.initialize_food_img()
        self.make_new_food()

    def initialize_empty_cells(self):
        """sets up cells with the correct dimensions for the current game"""

        self.empty_cells = set()
        self.cells = [[Cell(self, (col * SQUARE_WIDTH, row * SQUARE_WIDTH, col * SQUARE_WIDTH + SQUARE_WIDTH, row * SQUARE_WIDTH + SQUARE_WIDTH),
                            (row, col)) for col in range(GAME_GRID_DIMENSIONS)] for row in range(GAME_GRID_DIMENSIONS)]
        for row in self.cells:
            for cell in row:
                self.empty_cells.add(cell)

    def initialize_snake(self, score_label):
        """initializes snake for the current game

        Args:
            score_label (Label) size label to be passed to snake
        """

        middle = GAME_GRID_DIMENSIONS // 2
        starting_cell = self.cells[middle][middle]
        self.snake = Snake(self, starting_cell, score_label, self.empty_cells)

    def initialize_directions(self):
        """initializes each of the 4 direction objects"""

        self.up = Direction((0, -1))
        self.right = Direction((1, 0))
        self.down = Direction((0, 1))
        self.left = Direction((-1, 0))
        self.current_direction = None

    def move_snake(self):
        """makes the snake move a single time, also checking for game over"""

        # global TIME_BETWEEN_MOVES
        # TIME_BETWEEN_MOVES += 5
        self.changedDirectionThisTurnAlready = False
        (row, col) = self.snake.get_head().get_row_col()
        (dx, dy) = self.current_direction.get_deltas()

        if (not self.check_for_collision((row + dy, col + dx))):
            new_cell = self.cells[row + dy][col + dx]
            need_more_food = new_cell.get_type() == "FOOD"
            self.snake.move(new_cell, self.current_direction)
            if (need_more_food):
                self.make_new_food()
            self.after(TIME_BETWEEN_MOVES, self.move_snake)
        else:
            self.create_text(GAME_WIDTH / 2, GAME_WIDTH / 2, fill="white", font="Roboto 30 bold",
                             text="Game Over! ")

    def check_for_collision(self, new_coords):
        """checks if the cell that the snake is about to move into will result in a game over

        Args:
            new_coords (tuple) the grid indexes of the cell being moved to

        Returns:
            true if game is over, else false
        """

        (new_x, new_y) = new_coords
        if new_x >= GAME_GRID_DIMENSIONS or new_y >= GAME_GRID_DIMENSIONS or new_x < 0 or new_y < 0 \
                or self.cells[new_x][new_y].get_type() == "SNAKE":
            return True
        return False

    def make_new_food(self):
        """generates a new piece of food on the board randomly"""
        size = len(self.empty_cells)
        if size > 0:
            stop_sample = rand.randint(0, 10 if size > 10 else size - 1)
            i = 0
            for cell in self.empty_cells:
                if i == stop_sample:
                    cell.set_type("FOOD").draw()
                    break
                i += 1

    def initialize_food_img(self):
        """initializes the apple png used for the food"""

        img = Image.open("food.png")
        img = img.resize(
            (int(SQUARE_WIDTH), int(SQUARE_WIDTH)), Image.ANTIALIAS)
        self.tk_img = PhotoImage(img)

    def change_direction(self, event):
        """changes the direction of the snake so that next time it moves, it makes a turn

        Args:
            event (keyboard press) the event triggered when user presses arrow keys
        """

        if not self.changedDirectionThisTurnAlready:
            key = event.keysym
            new_direction = self.current_direction
            if key == "Up" and not self.current_direction == self.down:
                new_direction = self.up
            elif key == "Right" and not self.current_direction == self.left:
                new_direction = self.right
            elif key == "Down" and not self.current_direction == self.up:
                new_direction = self.down
            elif key == "Left" and not self.current_direction == self.right:
                new_direction = self.left

            first_move = self.current_direction == None
            if new_direction != self.current_direction:
                self.current_direction = new_direction
                self.snake.get_head().set_direction(new_direction)
                self.changedDirectionThisTurnAlready = True
                if first_move:
                    self.move_snake()

    def draw_all_cells(self):
        """draws all the empty cells on the board (these are only drawn once, snake goes on top)"""

        for row in self.cells:
            for cell in row:
                self.create_rectangle(
                    cell.get_coords(), fill=GAME_BACKGROUND_COLOR, outline=SQUARE_OUTLINE_COLOR)

    def restart_game(self):
        """restarts the game (called when play again is pressed, and when user changes board dimensions)"""

        self.delete("all")
        self.current_direction = None
        self.changedDirectionThisTurnAlready = False
        self.score_label["text"] = "Score: 1"

        self.initialize_empty_cells()
        self.draw_all_cells()
        self.initialize_snake(self.score_label)
        self.initialize_food_img()
        self.make_new_food()

    def handle_dimension_change(self, event):
        """handler for when the user changes board dimensions. Starts a new game

        Args:
            event (submission) submission event triggered when user presses enter from inside the entry field
        """

        global GAME_GRID_DIMENSIONS, GAME_WIDTH, SQUARE_WIDTH, TIME_BETWEEN_MOVES, INVERSE_PROP_CONSTANT
        try:
            new_dimens = int(event.widget.get())
            if new_dimens < 2 or new_dimens > 10000:
                raise ValueError('A very specific bad thing happened.')
            GAME_GRID_DIMENSIONS = int(event.widget.get())
            SQUARE_WIDTH = GAME_WIDTH / GAME_GRID_DIMENSIONS
            TIME_BETWEEN_MOVES = int(
                INVERSE_PROP_CONSTANT / GAME_GRID_DIMENSIONS)
            self.restart_game()
            self.focus_set()
        except:
            print("you fucked up")

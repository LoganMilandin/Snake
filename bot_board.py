from board import *
from snakebot import Snakebot


class BotBoard(Board):

    def start_bot(self):
        """makes the bot start playing"""

        print("bot starting")
        self.bot = Snakebot(self.snake.get_head(), self)
        self.current_direction = self.bot.get_new_direction()
        self.move_snake()

    def move_snake(self):
        # Overridden from Board
        (row, col) = self.snake.get_head().get_row_col()
        (dx, dy) = self.current_direction.get_deltas()

        if (not self.check_for_collision((row + dy, col + dx))):
            new_cell = self.cells[row + dy][col + dx]
            need_more_food = new_cell.get_type() == "FOOD"
            self.snake.move(new_cell, self.current_direction)
            if (need_more_food):
                self.make_new_food()

            self.bot.update_position(self.snake.get_head())
            self.current_direction = self.bot.get_new_direction()
            self.snake.get_head().set_direction(self.current_direction)
            self.after(1, self.move_snake)
        else:
            self.create_text(GAME_WIDTH / 2, GAME_WIDTH / 2, fill="white", font="Roboto 30 bold",
                             text="Game Over! ")

    def restart_game(self):
        # Overridden from Board
        Board.restart_game(self)
        self.after(1000, self.start_bot)

    def change_direction(self, event):
        """prints an error message because user can't change direction while bot is playing

        Args:
            event (keyboard press) the event triggered when user presses arrow keys
        """

        # Overridden from Board
        print("Can't change direction while bot is playing")

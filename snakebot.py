import board


class Snakebot:
    """Represents an autonomously played game of Snake that wins every time with brute force"""

    def __init__(self, initial_cell, board):
        """sets up bot with initial position

        Args:
            initial_cell(Cell): cell containing head to start with
            board(BotBoard): the board this bot is playing on
        """
        self.board = board
        self.head_cell = initial_cell
        self.direction = None

    def get_new_direction(self):
        """computes a direction for the snake head based on its current position and direction

        Returns:
            Direction: one of board.up, board.right, board.down, board.left
        """

        if not self.direction:
            return self.board.down
        up, right, down, left = self.board.up, self.board.right, self.board.down, self.board.left
        (y, x) = self.head_cell.get_row_col()
        if self.direction is down and y == board.GAME_GRID_DIMENSIONS - 1:
            return left
        elif self.direction is left and x == 0:
            return up
        elif self.direction is right:
            if x == board.GAME_GRID_DIMENSIONS - 1:
                return down
            elif x == board.GAME_GRID_DIMENSIONS - 2 and y > 0:
                return up
        elif self.direction is up:
            return right if x == 0 else left

        return self.direction

    def update_position(self, new_head):
        """notifies snakebot of a change in head position after snake completes a move

        Args:
            new_head(Cell) the cell now containing the snake head
        """
        self.head_cell = new_head
        self.direction = new_head.get_direction()

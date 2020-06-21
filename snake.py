class Snake:
    """Represents the player's snake in a given game. Resets at the start of a new game"""

    def __init__(self, board, initial_cell, score_label, empty_cells):
        """initializes the snake

        Args:
            board (Board) the board this snake belongs to
            initial_cell (Cell) the cell to become the head
            score_label (tkinter.Label) the label that reports snake size
            empty_cells (set) a set containing cells that are currently empty, i.e. those that can have food rendered
        """

        self.board = board
        self.score_label = score_label
        self.empty_cells = empty_cells
        self.body = []
        initial_cell.set_type("HEAD").draw()
        self.body.insert(0, initial_cell)
        self.empty_cells.remove(initial_cell)

    def move(self, next_cell, direction):
        """completes a single move for the snake

        Args:
            next_cell(Cell) the cell the head is trying to move into
            direciton(Direction) the direction the head is facing as it enters next_cell
        """

        # reference the previous head because we'll need to turn it into a body part or tail later
        prev_head = self.body[0]
        # insert the new head at the start of the list and remove it from the set of empty cells
        self.body.insert(0, next_cell)
        if next_cell.get_type() == "SNAKE":
            self.board.game_over = True
            return
        if next_cell in self.empty_cells:
            self.empty_cells.remove(next_cell)
        if next_cell.get_type() == "FOOD":
            # update score label if we found food and leave the tail the same
            self.score_label["text"] = "Score: " + str(len(self.body))
        else:
            # otherwise, we need to remove the tail and add it to the set of empty cells
            prev_tail = self.body.pop()
            self.empty_cells.add(prev_tail)
            prev_tail.set_type("EMPTY").delete_drawing()
        # make the new cell the head and draw it
        next_cell.set_type("HEAD").set_direction(direction).draw()
        if len(self.body) > 1:
            self.body[len(self.body) - 1].set_type("TAIL").draw()
        if len(self.body) > 2:
            # if it's longer than 2, the previous head is now a body part
            prev_head.set_type("SNAKE").draw()

    def get_head(self):
        """return the current head of the snake"""

        return self.body[0]

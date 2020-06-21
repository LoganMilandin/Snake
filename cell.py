import board
import tkinter


class Cell:
    def __init__(self, board, coords, row_col):
        """constructs a new cell

        Args:
            board (Board) the board this cell exists on
            coords (tuple) canvas coordinates of this cell
            row_col (tuple) grid indices of this cell
        """

        self.board = board
        self.type = "EMPTY"
        self.coords = coords
        self.row_col = row_col
        self.drawn_items = []
        self.direction = None

        self.eye_radius = (self.coords[2] - self.coords[0]) / 20
        self.eye_containers = self.get_eye_containers()
        self.smiley_face_box = self.get_smiley_face_box()

    def set_type(self, new_type):
        """sets the type of this cell, used for snake or food

        Args:
            new_type (str) the new cell type
        """

        self.type = new_type
        return self

    def set_direction(self, direction):
        """sets the direction that the snake head was facing when it reached this cell. Used for directionality with
            head/tail drawing

        Args:
            direction (Direction) the direction to set
        """

        self.direction = direction
        return self

    def get_direction(self):
        """getter for this cell's direction"""
        return self.direction

    def get_type(self):
        """gets the current type of this cell"""

        return self.type

    def get_coords(self):
        """gets this cell's canvas coordinates"""

        return self.coords

    def get_row_col(self):
        """gets this cell's grid indices"""

        return self.row_col

    def draw(self):
        """draws the cell depending on its current content. Does nothing if type == 'EMPTY'"""

        self.delete_drawing()
        if self.type == "HEAD":
            self.draw_head()
        elif self.type == "SNAKE":
            self.draw_body()
        elif self.type == "TAIL":
            self.draw_tail()
        elif self.type == "FOOD":
            self.draw_food()

    def draw_head(self):
        """draws the snake head (direction dependent)"""

        (x1, y1, x2, y2) = self.coords
        eyes_to_draw = []
        if self.direction == self.board.left:
            rectangle_coords = ((x1 + x2) / 2, y1, x2, y2)
            start_angle = 90
            mouth_start_angle = 300
            eyes_to_draw = [self.eye_containers[0], self.eye_containers[3]]
        elif self.direction == self.board.up or not self.direction:
            rectangle_coords = (x1, (y1 + y2) / 2, x2, y2)
            start_angle = 0
            mouth_start_angle = 210
            eyes_to_draw = [self.eye_containers[0], self.eye_containers[1]]
        elif self.direction == self.board.right:
            rectangle_coords = (x1, y1, (x1 + x2) / 2, y2)
            start_angle = 270
            mouth_start_angle = 120
            eyes_to_draw = [self.eye_containers[1], self.eye_containers[2]]
        else:
            rectangle_coords = (x1, y1, x2, (y1 + y2) / 2)
            start_angle = 180
            mouth_start_angle = 30
            eyes_to_draw = [self.eye_containers[2], self.eye_containers[3]]
        self.drawn_items.append(self.board.create_rectangle(
            rectangle_coords, fill=board.SNAKE_COLOR, outline=""))
        self.drawn_items.append(self.board.create_arc(
            self.coords, fill=board.SNAKE_COLOR, start=start_angle, extent=180, outline=""))
        for container in eyes_to_draw:
            self.drawn_items.append(
                self.board.create_oval(container, fill="black"))
        self.drawn_items.append(self.board.create_arc(self.smiley_face_box, fill="black", start=mouth_start_angle,
                                                      extent=120, width=self.eye_radius * 1.5, style=tkinter.ARC))

    def draw_body(self):
        """draws a single body square of the snake (exlcudes tail or head)"""

        self.drawn_items.append(self.board.create_rectangle(
            self.coords, fill=board.SNAKE_COLOR, outline=board.SQUARE_OUTLINE_COLOR))

    def draw_food(self):
        """draws a food square"""

        (x1, y1, x2, y2) = self.coords
        self.drawn_items.append(self.board.create_image(
            x1, y1, image=self.board.tk_img, anchor=tkinter.NW))

    def draw_tail(self):
        """draws snake tail (direction dependent)"""

        (x1, y1, x2, y2) = self.coords
        cell_width = x2 - x1
        if self.direction == self.board.left:
            tail_coords = (x1, y1, x1, y2, x2, y2 -
                           cell_width / 3, x2, y1 + cell_width / 3)
        elif self.direction == self.board.up or not self.direction:
            tail_coords = (x1, y1, x2, y1, x2 - cell_width /
                           3, y2, x1 + cell_width / 3, y2)
        elif self.direction == self.board.right:
            tail_coords = (x2, y1, x2, y2, x1, y2 -
                           cell_width / 3, x1, y1 + cell_width / 3)
        else:
            tail_coords = (x1, y2, x2, y2, x2 - cell_width /
                           3, y1, x1 + cell_width / 3, y1)
        self.drawn_items.append(self.board.create_polygon(
            tail_coords, fill=board.SNAKE_COLOR, outline=board.SQUARE_OUTLINE_COLOR))

    def get_eye_containers(self):
        """computes bounding rectangles for 4 possible eye locations

        Returns:
            tuple of tuples containing coordinates for bounding rectangles
        """

        (x1, y1, x2, y2) = self.coords
        distance_to_box_edge = (x2 - x1) / 3
        curr_x = x1 + distance_to_box_edge
        curr_y = y1 + distance_to_box_edge

        def produce_tuple_with_offset():
            return (curr_x - self.eye_radius, curr_y - self.eye_radius, curr_x + self.eye_radius, curr_y + self.eye_radius)
        top_left = produce_tuple_with_offset()
        curr_x += distance_to_box_edge
        top_right = produce_tuple_with_offset()
        curr_y += distance_to_box_edge
        bottom_right = produce_tuple_with_offset()
        curr_x -= distance_to_box_edge
        bottom_left = produce_tuple_with_offset()
        return (top_left, top_right, bottom_right, bottom_left)

    def get_smiley_face_box(self):
        """computes bounding rectangle for the mouth curve (just a box centered at the middle of this cell)

        Returns:
            tuple containing coordinates of bounding rectangle for mouth
        """

        (x1, y1, x2, y2) = self.coords
        distance_to_box_edge = (x2 - x1) / 5
        return (x1 + distance_to_box_edge, y1 + distance_to_box_edge, x2 - distance_to_box_edge, y2 - distance_to_box_edge)

    def delete_drawing(self):
        """deletes everything that has been drawn in this cell, except the background"""

        for drawing in self.drawn_items:
            self.board.delete(drawing)
        self.drawn_items = []

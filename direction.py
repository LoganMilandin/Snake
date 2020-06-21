class Direction:
    """represents one of up, right, down, left. Contains information about coordinate deltas
        for direction being represented
    """

    def __init__(self, deltas):
        """initializes direction object

        Args:
            deltas (tuple) a tuple of the form (dx, dy) for this direction, in grid coordinates
        """

        self.deltas = deltas

    def get_deltas(self):
        """returns the deltas associated to this direction"""
        return self.deltas

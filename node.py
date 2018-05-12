

class Node:

    def __init__(self, board, x, y, maximizing, depth):
        self.board = board
        self.x = x
        self.y = y
        self.maximizing = maximizing
        self.depth = depth

    def get_coordinates(self):
        pass

    def get_value(self):
        pass

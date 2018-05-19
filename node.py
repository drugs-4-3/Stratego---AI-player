

class Node:

    def __init__(self, board, x, y, maximizing, depth):
        self.board = board
        self.x = x
        self.y = y
        self.maximizing = maximizing
        self.depth = depth
        self.value = None

        points = self.board.insert_pos(x, y)
        if maximizing:
            board.computer_points += points
        else:
            board.player_points += points

        self.value = self.minmax()

    def get_coordinates(self):
        return self.x, self.y

    def get_value(self):
        if self.value is None:
            self.value = self.minmax()
        return self.value

    def minmax(self):
        """
        Returns potential value that player can achieve from given move using minmax algorithm
        :return: int
        """
        if self.depth <= 0:
            return self.board.computer_points - self.board.player_points
        else:
            children = []
            available_positions = self.board.get_available_positions()
            for (x, y) in available_positions:
                children.append(Node(self.board.copy(), x, y, not self.maximizing, self.depth-1))
            if len(children) > 0:
                best_child = children[0]
                for child in children:
                    if child.get_value() > best_child.get_value():
                        best_child = child
                return best_child.get_value()
            else:
                return self.board.computer_points - self.board.player_points

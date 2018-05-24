MINMAX_TREE_DEPTH = 6


class Node:

    def __init__(self, board, x, y, maximizing, depth):
        self.board = board
        self.x = x
        self.y = y
        self.maximizing = maximizing
        self.depth = depth
        self.minmax_value = None

        points = self.board.insert_pos(x, y)
        if maximizing:
            board.computer_points += points
        else:
            board.player_points += points

    def get_coordinates(self):
        return self.x, self.y

    def minmax(self):
        """
        Returns potential value that player can achieve from given move using minmax algorithm
        :return: int
        """
        if self.minmax_value is not None:
            return self.minmax_value

        available_positions = self.board.get_available_positions()
        if self.depth <= 0 or not available_positions:
            self.minmax_value = self.heuristic_value()
            self.print_node()
            return self.minmax_value

        children = []
        for (x, y) in available_positions:
            children.append(Node(self.board.copy(), x, y, not self.maximizing, self.depth - 1))

        best_child = children[0]
        if self.maximizing:
            for child in children:
                if child.minmax() > best_child.minmax():
                    best_child = child
        else:
            for child in children:
                if child.minmax() < best_child.minmax():
                    best_child = child

        self.minmax_value = best_child.minmax()
        self.print_node()
        return self.minmax_value

    def heuristic_value(self):
        """
        Returns heuristic value for a game at current node state
        :return:
        """
        return self.board.computer_points - self.board.player_points

    def print_node(self):
        indent = "   "*(MINMAX_TREE_DEPTH - self.depth)
        print(indent + "Node({},{}): value: {}".format(self.x, self.y, self.minmax_value))

    

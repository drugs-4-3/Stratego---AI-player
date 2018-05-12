
from board import Board
from random import randint
from node import Node


class ComputerPlayer:

    ALGORITHM_RANDOM_CODE = 0
    ALGORITHM_GREEDY_CODE = 1
    ALGORITHM_MINMAX_CODE = 2
    ALGORITHM_ALPHABETA_CODE = 3
    MINMAX_TREE_DEPTH= 5

    def __init__(self, alg_type):
        """
        Initialize artificial player with chosen algorithm to play
        :param alg_type: algorithm type that decides ComputerPlayer moves
        """
        if alg_type not in [ComputerPlayer.ALGORITHM_RANDOM_CODE, ComputerPlayer.ALGORITHM_GREEDY_CODE, ComputerPlayer.ALGORITHM_MINMAX_CODE, ComputerPlayer.ALGORITHM_ALPHABETA_CODE]:
            print("No matched algorithm for input " + str(alg_type) + ". Choosing ALGORITHM_RANDOM. ")
            self.alg_type = ComputerPlayer.ALGORITHM_RANDOM_CODE
        else:
            self.alg_type = alg_type

    def get_move(self, board: Board):
        """
        Returns (x, y) coords of move chosen by computer according to chosen algorithm for board passed as a parameter
        Returns only coords that are free at moment of choosing - can be taken
        :param board: game board
        :return: tuple (x: int, y: int)
        """
        if self.alg_type == ComputerPlayer.ALGORITHM_RANDOM_CODE:
            return self.random_move(board)
        elif self.alg_type == ComputerPlayer.ALGORITHM_GREEDY_CODE:
            return self.greedy_move(board)
        elif self.alg_type == ComputerPlayer.ALGORITHM_ALPHABETA_CODE:
            return self.alphabeta_move(board)
        else:
            return self.minmax_move(board)

    def random_move(self, board: Board):
        """
        Returns random (x, y)
        :param board:
        :return:
        """
        x, y = (randint(0, board.size - 1), randint(0, board.size - 1))
        while board.data[x][y] != 0:
            x, y = (randint(0, board.size - 1), randint(0, board.size - 1))
        return x, y

    def greedy_move(self, board: Board):
        """
        Returns (x, y) coords that give the most benefit on short term.
        :param board:
        :return:
        """
        # no initial position picked - we have to search for first free
        best_x = -1
        best_y = -1
        best_gain = board.count_points(best_x, best_y)
        for y in range(board.size):
            for x in range(board.size):
                if board.data[x][y] != 0:
                    continue  # don't check position already taken
                if best_x == -1 and best_y == -1:
                    best_x = x
                    best_y = y
                gain = board.count_points(x, y)
                print("gain(" + str(x) + "," + str(y) + ") gain: " + str(gain))
                if gain > best_gain:
                    best_gain = gain
                    best_x = x
                    best_y = y
        return best_x, best_y
        pass

    def minmax_move(self, board: Board):
        """
        Returns (x,y) move chosen by minmax algorithm
        :param board:
        :return:
        """

        children_nodes = []
        for (x, y) in board.get_available_positions():
            children_nodes.append(Node(board.copy(), x, y, True, ComputerPlayer.MINMAX_TREE_DEPTH))
        best_node = children_nodes[0]
        for node in children_nodes:
            if node.get_value() > best_node.get_value():
                best_node = node
        return best_node.get_coordinates()

    def alphabeta_move(self, board: Board):
        """
        Returns (x,y) move chosen by alpha beta pruning algorithm
        :param board:
        :return:
        """
        pass

    def get_gain(self, board, x, y):
        """
        Return possible gain points
        :param board:
        :param x:
        :param y:
        :return:
        """
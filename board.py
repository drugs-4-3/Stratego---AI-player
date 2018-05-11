
class Board:

    def __init__(self, size, data=None):
        # dimension of board
        self.size = size

        # list of X coordinates in range (0, size-1) of vertical lines that were already crossed
        self.crossed_vertical_lines = []

        # list of Y coordinates in range (0, size-1) of horizontal lines that were already crossed
        self.crossed_horizontal_lines = []

        # list of tuples (x,y) where each element is top left coordinate of diagonal line that was already crossed
        self.crossed_diagonal_lines_top_left = []

        # list of tuples (x,y) where each element is top right coordinate of diagonal line that was already crossed
        self.crossed_diagonal_lines_top_right = []

        # data is two dimensional array that contains selected by players coordinates
        if data is not None:
            self.data = data
        else:
            self.data = Board.init_data(size)

    def __str__(self):
        res = "BOARD " + str(self.size) + "x" + str(self.size) + "\n"
        for y in range(self.size):
            for x in range(self.size):
                res += str(self.data[x][y])
            res += "\n"
        return res

    @classmethod
    def init_data(cls, dimension):
        """
        Creates empty initial board NxN size
        :param dimension: Number
        :return: array[N][N] filled with zeros
        """
        return [[0 for _ in range(dimension)] for _ in range(dimension)]

    @staticmethod
    def load_from_file(filename):
        """
            Returns board prepared in text file
            :param filename: String
            :return:
            """
        data = list()
        file = open(filename, 'r')
        for line in file:
            elements = line.split(" ")
            data.append(list(map(int, elements)))
        return Board(len(data), data)

    def print_board(self):
        """
        Prints NxN size board into screen
        :param board: NxN size array
        """
        for i in range(self.size):
            for j in range(self.size):
                print(str(self.data[i][j]) + " ", end='')
            print()

    def insert_pos(self, x, y):
        """
        Inserts mark at position (x, y) and returns points achieved by this move
        Also remembers crossed lines to prevent them from being taken into account in future
        :param x:
        :param y:
        :return:
        """
        self.data[x][y] = 1

        vertical_points = self.__check_vertical_lines(x)
        if vertical_points == self.size:
            self.crossed_vertical_lines.append(x)

        horizontal_points = self.__check_horizontal_lines(y)
        if horizontal_points == self.size:
            self.crossed_horizontal_lines.append(y)

        diagonal_left_points = self.__check_diagonal_left(x, y)
        if diagonal_left_points >= 2:
            self.crossed_diagonal_lines_top_left.append(self.__get_top_left_diagonal_coords(x, y))

        diagonal_right_points = self.__check_diagonal_right(x, y)
        if diagonal_right_points >= 2:
            self.crossed_diagonal_lines_top_right.append(self.__get_top_right_diagonal_coords(x, y))

        return vertical_points + horizontal_points + diagonal_left_points + diagonal_right_points

    def count_points(self, x, y):
        """
        Counts how many points one can achieve from given position.
        Returns points achived
        :param x:
        :param y:
        :return: int
        """
        prev_val = self.data[x][y]
        self.data[x][y] = 1
        points = 0
        points += self.__check_vertical_lines(x)
        points += self.__check_horizontal_lines(y)
        points += self.__check_diagonal_lines(x, y)
        self.data[x][y] = prev_val
        return points

    def __check_vertical_lines(self, x):
        """
        Returns tuple(x, N) if found newly crossed vertical line.
        Remembers found line.
        If nothing found, returns False
        :return: tuple(x, N) of False
        """
        if x in self.crossed_vertical_lines:
            return 0

        for i in range(self.size):
            if self.data[x][i] == 0:
                return 0
        return self.size

    def __check_horizontal_lines(self, y):
        """
        Returns tuple(x, N) if found newly crossed vertical line.
        Remembers found line.
        If nothing found, returns False
        :return: tuple(x, N) of False
        """
        if y in self.crossed_horizontal_lines:
            return 0

        for i in range(self.size):
            if self.data[i][y] == 0:
                return 0
        return self.size

    def __check_diagonal_lines(self, x, y):
        """
        Counts how many points can be achieved from diagonal lines by taking move at (x, y)
        :param x:
        :param y:
        :return:
        """
        points = 0
        points += self.__check_diagonal_left(x, y)
        points += self.__check_diagonal_right(x, y)
        return points

    def __check_diagonal_left(self, x, y):
        """
        Counts how many points can be achieved by taking move at (x, y) from crossing diagonal right-to-left
        :param x:
        :param y:
        :return: int points
        """
        x, y = self.__get_top_left_diagonal_coords(x, y)
        if (x, y) in self.crossed_diagonal_lines_top_left:
            return 0
        count = 0
        while x < self.size and y < self.size:
            count += 1
            if self.data[x][y] == 0:
                return 0
            x += 1
            y += 1
        if count < 2:  # 2 is minimal amount of diagonal points
            return 0
        return count

    def __check_diagonal_right(self, x, y):
        """
        Counts how many points can be achieved by taking move at (x, y) from crossing diagonal left-to-right
        :param x:
        :param y:
        :return: int points
        """
        x, y = self.__get_top_right_diagonal_coords(x, y)
        if (x, y) in self.crossed_diagonal_lines_top_right:
            return 0
        count = 0
        while x >= 0 and y < self.size:
            count += 1
            if self.data[x][y] == 0:
                return 0
            x -= 1
            y += 1
        if count < 2:  # 2 is minimal amount of diagonal points
            return 0
        return count

    def __get_top_left_diagonal_coords(self, x, y):
        while x > 0 and y > 0:
            x -= 1
            y -= 1
        return x, y

    def __get_top_right_diagonal_coords(self, x, y):
        while x < (self.size - 1) and y > 0:
            x += 1
            y -= 1
        return x, y

import copy


class Board:
    """
    Class representing board on which the game is being played.
    For each position on board the coordinates are represented as (x, y)
    Top left position is (0, 0),
    x is incrementing as we go right,
    y is incremented as we go down,
    bottom-down position is (board.size - 1, board.size - 1)
    """

    def __init__(self,
                 size,
                 data=None,
                 crossed_vertical_lines=None,
                 crossed_horizontal_lines=None,
                 crossed_diagonal_lines_left=None,
                 crossed_diagonal_lines_right=None,
                 c_points=0,
                 p_points=0):

        # dimension of board
        self.size = size

        # data is two dimensional array that contains selected by players coordinates
        if data is not None:
            self.data = data
        else:
            self.data = Board.init_data(size)

        # list of X coordinates in range (0, size-1) of vertical lines that were already crossed
        if crossed_vertical_lines is not None:
            self.crossed_vertical_lines = crossed_vertical_lines
        else:
            self.crossed_vertical_lines = []

        # list of Y coordinates in range (0, size-1) of horizontal lines that were already crossed
        if crossed_horizontal_lines is not None:
            self.crossed_horizontal_lines = crossed_horizontal_lines
        else:
            self.crossed_horizontal_lines = []

        # list of tuples (x,y) where each element is top left coordinate of diagonal line that was already crossed
        if crossed_diagonal_lines_left is not None:
            self.crossed_diagonal_lines_top_left = crossed_diagonal_lines_left
        else:
            self.crossed_diagonal_lines_top_left = []

        # list of tuples (x,y) where each element is top right coordinate of diagonal line that was already crossed
        if crossed_diagonal_lines_right is not None:
            self.crossed_diagonal_lines_top_right = crossed_diagonal_lines_right
        else:
            self.crossed_diagonal_lines_top_right = []

        self.computer_points = c_points
        self.player_points = p_points

    def __str__(self):
        res = ""
        for y in range(self.size):
            for x in range(self.size):
                res += str(self.data[y][x])
            res += "\n"
        res = res[:-1]
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
            Returns board prepared in text file.
            This method doesn't fills the "crossed lines" fields so counting points from such board may be incorrect.
            This also doesn't include players points
            TODO: need to implement method that will fill crossed lines for board
            :param filename: String
            :return:
            """
        data = list()
        file = open(filename, 'r')
        for line in file:
            elements = line.split(" ")
            data.append(list(map(int, elements)))
        file.close()
        return Board(len(data), data)

    def to_string(self):
        """
        Returns string representation of board
        :return:
        """
        result = ""
        result += ("c_points: " + str(self.computer_points) + "\n")
        result += ("p_points: " + str(self.player_points) + "\n")
        for y in range(self.size):
            for x in range(self.size):
                result += (str(self.data[y][x]) + " ")
            result += "\n"
        return result

    def insert_pos(self, x, y, val=1):
        """
        Inserts mark at position (x, y) and returns points achieved by this move
        Also remembers crossed lines to prevent them from being taken into account in future
        Coords are visual coords - not array coords
        """
        self.data[y][x] = val

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

    def get_position(self, x, y):
        """
        Returns "0" or "1" value of board at coords (x,y)
        Coords are in visual format - not array positions
        :param x:
        :param y:
        :return:
        """
        return self.data[y][x]

    def count_points(self, x, y):
        """
        Counts how many points one can achieve from given position.
        Returns points achived
        :param x:
        :param y:
        :return: int
        """
        prev_val = self.get_position(x, y)
        self.data[y][x] = 1
        points = 0
        points += self.__check_vertical_lines(x)
        points += self.__check_horizontal_lines(y)
        points += self.__check_diagonal_lines(x, y)
        self.data[y][x] = prev_val
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
            if self.data[i][x] == 0:
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
            if self.data[y][i] == 0:
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
        Counts how many points can be achieved by taking move at (x, y) from crossing diagonal left-to-right
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
            if self.get_position(x, y) == 0:
                return 0
            x += 1
            y += 1
        if count < 2:  # 2 is minimal amount of diagonal points
            return 0
        return count

    def __check_diagonal_right(self, x, y):
        """
        Counts how many points can be achieved by taking move at (x, y) from crossing diagonal right-to-left
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
            if self.get_position(x, y) == 0:
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

    def get_available_positions(self):
        """
        Returns list with tuples (x, y) for each available (not crossed, 0 value) position on board
        :return:
        """
        available_positions = []
        for y in range(self.size):
            for x in range(self.size):
                if self.get_position(x, y) == 0:
                    available_positions.append((x, y))
        return available_positions

    def copy(self):
        """
        Returns exact value copy of a Board instance
        :return:
        """
        return Board(self.size,
                     copy.deepcopy(self.data),
                     copy.deepcopy(self.crossed_vertical_lines),
                     copy.deepcopy(self.crossed_horizontal_lines),
                     copy.deepcopy(self.crossed_diagonal_lines_top_left),
                     copy.deepcopy(self.crossed_diagonal_lines_top_right))
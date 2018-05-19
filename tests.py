import unittest
from board import Board


class TestStrategoMethods(unittest.TestCase):
    """
    Tests depend on test_board.txt file, that contains such board:

    0 1 1 1 1
    1 1 0 0 1
    1 1 1 1 1
    1 1 1 1 1
    1 1 1 1 1
    """

    def test_loading_from_file(self):
        board = Board.load_from_file("test_board.txt")
        self.assertTrue(board.data[0][0] == 0)
        self.assertTrue(board.data[3][1] == 1)

    def test_board_copy(self):
        """
        Make sure copying boards make two totally separate instances
        :return:
        """
        board_original = Board.load_from_file("test_board.txt")
        board_copy = board_original.copy()
        self.assertEqual(board_original.data[0][0], 0)
        self.assertEqual(board_copy.data[0][0], 0)

        board_original.data[0][0] = 1
        self.assertEqual(board_original.data[0][0], 1)
        self.assertEqual(board_copy.data[0][0], 0)
        self.assertLess(len(board_original.get_available_positions()), len(board_copy.get_available_positions()))

    def test_visual_representation_of_board(self):
        """
        Make sure that visual representation of coords (x, y) is properly read and outputed
        :return:
        """
        board = Board(4)
        lines = board.__str__().split("\n")
        self.assertEqual(lines[0][1], '0')
        self.assertEqual(lines[1][0], '0')

        board.insert_pos(1, 0)
        lines = board.__str__().split("\n")
        self.assertEqual(lines[0][1], '1')
        self.assertEqual(lines[1][0], '0')

    def test_choosing_selected_position(self):
        """
        Make sure that insert_pos(x, y) places point on correct position and the position afterwards is not available
        :return:
        """
        board = Board(4)

        lines = board.__str__().split("\n")
        self.assertEqual(lines[0][1], '0')
        self.assertEqual(lines[1][0], '0')
        self.assertEqual(board.get_position(1, 0), 0)
        self.assertEqual(board.get_position(0, 1), 0)

        board.insert_pos(1, 0)
        self.assertEqual(board.get_position(1, 0), 1)
        self.assertEqual(board.get_position(0, 1), 0)
        lines = board.__str__().split("\n")
        self.assertEqual(lines[0][1], '1')
        self.assertEqual(lines[1][0], '0')
        available_positions = board.get_available_positions()
        self.assertFalse((1, 0) in available_positions)
        self.assertTrue((0, 1) in available_positions)

    def test_adding_crossed_lines(self):
        """
        Make sure that after crossing line and gaining points,
        crossed line is being properly remembered to not return points in the future
        :return:
        """
        board = Board(4, [[1, 0, 0, 0],
                          [0, 0, 0, 0],
                          [0, 0, 0, 0],
                          [1, 1, 1, 0]])
        self.assertTrue(not board.crossed_vertical_lines)
        self.assertTrue(not board.crossed_horizontal_lines)
        board.insert_pos(3, 3)
        self.assertTrue(3 in board.crossed_horizontal_lines)
        self.assertTrue(not board.crossed_vertical_lines)
        board.insert_pos(0, 1)
        board.insert_pos(0, 2)
        self.assertTrue(3 in board.crossed_horizontal_lines)
        self.assertTrue(0 in board.crossed_vertical_lines)

    def test_available_positions(self):
        """
        Make sure that all available positions are being properly returned
        :return:
        """
        board = Board.load_from_file("test_board.txt")
        available_positions = board.get_available_positions()
        self.assertEqual(3, len(available_positions))
        self.assertTrue((0, 0) in available_positions)
        self.assertTrue((2, 1) in available_positions)
        self.assertTrue((3, 1) in available_positions)

        board.insert_pos(2, 1)
        available_positions = board.get_available_positions()
        self.assertEqual(2, len(available_positions))
        self.assertTrue((0, 0) in available_positions)
        self.assertFalse((2, 1) in available_positions)
        self.assertTrue((3, 1) in available_positions)

    def test_gaining_points_straight_lines(self):
        """
        Make sure that points from crossing vertical and horizontal lines are being properly counted
        :return:
        """
        board = Board(4, [[1, 0, 1, 0],
                          [0, 0, 0, 0],
                          [0, 0, 0, 0],
                          [1, 1, 1, 0]])

        points = board.insert_pos(3, 3)
        self.assertEqual(points, 4)

        points = board.insert_pos(2, 1)
        self.assertEqual(points, 0)

        points = board.insert_pos(2, 2)
        self.assertEqual(points, 4)

    def test_gaining_points_diagonal_lines(self):
        board = Board(4, [[1, 0, 0, 0],
                          [0, 0, 0, 0],
                          [0, 0, 1, 0],
                          [0, 0, 0, 0]])

        points = board.insert_pos(1, 1)
        self.assertEqual(points, 0) # not gaining points from not crossing full diagonal
        points = board.insert_pos(3, 3)
        self.assertEqual(points, 4) # gain 4 points from crossing full diagonal

        points = board.insert_pos(3, 0)
        self.assertEqual(points, 0) # not gaining points from putting only one point in corner

        points = board.insert_pos(2, 1)
        self.assertEqual(points, 0) # not gaining points from not crossing full diagonal
        points = board.insert_pos(1, 2)
        self.assertEqual(points, 0) # same as above
        points = board.insert_pos(0, 3)
        self.assertEqual(points, 4) # gain 4 points from crossing full diagonal

        board.insert_pos(2, 0)
        points = board.insert_pos(3, 1)
        self.assertEqual(points, 2) # gain 2 points from crossing 2-point diagonal


    def test_gaining_points_from_crossing_multiple_straight_lines(self):
        board = Board(4, [[0, 1, 1, 1],
                          [1, 0, 0, 0],
                          [1, 0, 1, 0],
                          [1, 0, 0, 0]])
        points = board.insert_pos(0, 0)
        self.assertEqual(points, 8)

    def test_gaining_points_from_crossing_multiple_diagonal_lines(self):
        board = Board(5, [[1, 0, 0, 0, 1],
                          [0, 1, 0, 1, 0],
                          [0, 0, 0, 0, 0],
                          [0, 1, 0, 1, 0],
                          [1, 0, 0, 0, 1]])
        points = board.insert_pos(2, 2)
        self.assertEqual(points, 10)

    def test_gaining_points_from_crossing_diagonal_and_straight_lines(self):
        board = Board(5, [[1, 0, 1, 0, 1],
                          [0, 1, 1, 1, 0],
                          [1, 1, 0, 1, 1],
                          [0, 1, 1, 1, 0],
                          [1, 0, 1, 0, 1]])
        points = board.insert_pos(2, 2)
        self.assertEqual(points, 20)


if __name__ == '__main__':
    unittest.main()
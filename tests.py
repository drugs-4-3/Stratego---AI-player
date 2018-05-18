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

    def test_available_positions(self):
        """
        Make sure that all available positions are being properly returned
        :return:
        """
        board = Board.load_from_file("test_board.txt")
        available_positions = board.get_available_positions()
        self.assertEqual(3, len(available_positions))
        self.assertTrue((0, 0) in available_positions)
        self.assertTrue((1, 2) in available_positions)

    def test_gaining_points(self):
        # TODO: implement method for filling crossed lines for board loaded from file
        pass

    def test_choosing_selected_position(self):
        pass

if __name__ == '__main__':
    unittest.main()
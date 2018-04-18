
from board import Board
from random import randint
from computer_player import ComputerPlayer


def get_computer_input(board):
    return randint(0, board.size - 1), randint(0, board.size - 1)


menu = """
Stratego: 
1. to select position enter input in form: x y
2. to quit game write "quit"
"""

board = Board(4)
loop = True
print(board)
counter = 0

computer_points = 0
player_points = 0
cp = ComputerPlayer(ComputerPlayer.ALGORITHM_GREEDY)

while loop:
    if counter % 2 != 0:
        (x, y) = cp.get_move(board)
        print("computer chooses: (" + str(x) + "," + str(y) + ")")
        points = board.insert_pos(x, y)
        computer_points += points
        print("computer gets: " + str(points))
    else:
        inp = input(menu)
        (x, y) = (inp.split(" ")[0], inp.split(" ")[1])
        points = board.insert_pos(int(x), int(y))
        print("player gets: " + str(points))
        player_points += points
    counter += 1
    print(board)
    print("P: " + str(player_points))
    print("C: " + str(computer_points))
    # (x, y) = (inp.split(" ")[0], inp.split(" ")[1])
    # points = board.insert_pos(int(x), int(y))
    # print("player gets: " + str(points))
    # player_points += points



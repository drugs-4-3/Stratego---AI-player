
from board import Board
from random import randint
from computer_player import ComputerPlayer


def finish_game():
    print("GAME OVER!\n")
    print("Computer points: {}\n", computer_points)
    print("Player points: {}\n", player_points)
    if computer_points > player_points:
        print("COMPUTER WINS!\n")
    elif player_points > computer_points:
        print("PLAYER WINS!\n")
    else:
        print("DRAW!\n")


menu = """
Stratego: 
1. to select position enter input in form: x y
2. to quit game write "quit"
"""

board_dimension = 5
board = Board(board_dimension)
computer_points = 0
player_points = 0
cp = ComputerPlayer(ComputerPlayer.ALGORITHM_GREEDY)
counter = 0
print(board)


while counter < board_dimension*board_dimension - 1:
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

finish_game()

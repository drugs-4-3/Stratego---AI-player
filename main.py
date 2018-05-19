
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

board_dimension = 4
board = Board(board_dimension)
computer_points = 0
player_points = 0
cp = ComputerPlayer(ComputerPlayer.ALGORITHM_MINMAX_CODE)
counter = 0
print(board)


while counter < board_dimension*board_dimension:
    if counter % 2 != 0:
        (x, y) = cp.get_move(board)
        print("computer chooses: (" + str(x) + "," + str(y) + ")")
        points = board.insert_pos(x, y)
        computer_points += points
        board.computer_points = computer_points
        print("computer gets: " + str(points))
    else:
        inp = input(menu).split(" ")
        (x, y) = (int(inp[0]), int(inp[1])) #reverse x and y because of the difference in array representation and coords
        if board.get_position(x, y) == 1:
            print("This position is already taken! Choose something different. ")
            continue
        points = board.insert_pos(int(x), int(y))
        print("player gets: " + str(points))
        player_points += points
        board.player_points = player_points
    counter += 1
    print(board)
    print("P: " + str(player_points))
    print("C: " + str(computer_points))

finish_game()

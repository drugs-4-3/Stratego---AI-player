
from board import Board
from random import randint
from time import sleep
from computer_player import ComputerPlayer


def finish_game(computer_points, player_points):
    print("GAME OVER!\n")
    print("Computer points: {}\n", computer_points)
    print("Player points: {}\n", player_points)
    if computer_points > player_points:
        print("COMPUTER WINS!\n")
    elif player_points > computer_points:
        print("PLAYER WINS!\n")
    else:
        print("DRAW!\n")

def minmax_greedy_game():
    greedy_points = 0
    minmax_points = 0
    greedy_player = ComputerPlayer(ComputerPlayer.ALGORITHM_GREEDY_CODE)
    minmax_player = ComputerPlayer(ComputerPlayer.ALGORITHM_MINMAX_CODE)
    counter = 0
    print(board)

    while counter < board_dimension * board_dimension:
        if counter % 2 != 0:
            # greedy_move
            print("GREEDY MOVE:")
            (x, y) = greedy_player.get_move(board)
            print("greedy chooses: (" + str(x) + "," + str(y) + ")")
            points = board.insert_pos(x, y)
            greedy_points += points
            print("greedy gets: " + str(points))
        else:
            print("MINMAX MOVE:")
            (x, y) = minmax_player.get_move(board)
            print("minmax chooses: (" + str(x) + "," + str(y) + ")")
            points = board.insert_pos(x, y)
            minmax_points += points
            print("minmax gets: " + str(points))
        counter += 1
        print(board)
        print("GREEDY: " + str(greedy_points))
        print("MINMAX: " + str(minmax_points))
        sleep(4)

    print("GAME OVER!")
    print("GREEDY POINTS: " + str(greedy_points))
    print("MINMAX POINTS: " + str(minmax_points))
    if minmax_points > greedy_points:
        print("MINMAX WINS!")
    else:
        print("GREEDY WINS!")


def computer_player_game():
    computer_points = 0
    player_points = 0
    cp = ComputerPlayer(ComputerPlayer.ALGORITHM_GREEDY_CODE)
    counter = 0
    print(board)

    while counter < board_dimension * board_dimension:
        if counter % 2 != 0:
            print("Please wait. The computer is calculating next move...")
            (x, y) = cp.get_move(board)
            print("computer chooses: (" + str(x) + "," + str(y) + ")")
            points = board.insert_pos(x, y)
            computer_points += points
            board.computer_points = computer_points
            print("computer gets: " + str(points))
        else:
            inp = input(menu).split(" ")
            (x, y) = (int(inp[0]), int(inp[1]))
            if board.get_position(x, y) == 1:
                print("This position is already taken! Choose something different. ")
                continue
            points = board.insert_pos(int(x), int(y))
            print("player gets: " + str(points))
            player_points += points
            board.player_points = player_points
        av_pos = board.get_available_positions()
        print("available positions: ")
        print(str(av_pos))
        counter += 1
        print(board)
        print("P: " + str(player_points))
        print("C: " + str(computer_points))

    finish_game(computer_points, player_points)


menu = """
Please write your input. 
(To select position enter input in form: x y)
"""

board_dimension = 4
board = Board(board_dimension)
# computer_player_game()
minmax_greedy_game()

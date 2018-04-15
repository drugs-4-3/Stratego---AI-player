
from board import Board
from random import randint


def get_computer_input(board):
    return randint(0, board.size), randint(0, board.size)


menu = """
Stratego: 
1. to select position enter input in form: x y
2. to quit game write "quit"
"""

board = Board(10)
loop = True
print(board)
counter = 0

while loop:
    if counter % 2 != 0:
        (x, y) = get_computer_input(board)
        while board.data[x][y] != 0:
            (x, y) = get_computer_input(board)
        board.insert_pos(x, y)
    else:
        inp = input(menu)
        if inp == "quit" or inp == "exit" or inp == "q":
            loop = False
        (x, y) = (inp.split(" ")[0], inp.split(" ")[1])
        board.insert_pos(int(x), int(y))
    counter += 1
    print(board)


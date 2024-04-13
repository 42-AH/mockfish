import sys

import chess

from eval import evaluate
from minimax import find_best_move


def check():
  if board.is_checkmate():
    if board.turn:
        print("Black won")
        sys.exit()
    else:
        print("White won")
        sys.exit()
  if board.is_stalemate():
    print("Draw")
    sys.exit()
  if board.is_insufficient_material():
    print("Insufficient material")
    sys.exit()
  if board.is_fivefold_repetition():
    print("Fivefold repitition")
    sys.exit()
board = chess.Board() 
board.turn = chess.WHITE
while not board.is_game_over():
    check()
    if board.turn:
        move = find_best_move(board, 4)
        print("WHITE")
        board.push(move)
        print("Score: " + str(evaluate(board, True)))
    else:
        move = find_best_move(board, 3)
        print("BLACK")
        board.push(move)
        print("Score: " + str(evaluate(board, False)))
    print(board)
    print(" ")
check()



""" 
For player input:

        user_move = input("Move: ")
        move = chess.Move.from_uci(user_move)
        print("WHITE")
        
"""

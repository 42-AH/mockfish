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
board = chess.Board("1q2k3/2q5/8/8/8/8/8/K7") 
board.turn = chess.WHITE
while not board.is_game_over():
    check()
    if board.turn:
        user_move = input("Move: ")
        move = chess.Move.from_uci(user_move)
        board.push(move)
        print("WHITE")
        print("Score: " + str(evaluate(board, False)))
    else:
        move = find_best_move(board, 3)
        print("BLACK")
        board.push(move)
        print("Score: " + str(evaluate(board, False)))
    print(board)
    print(" ")
check()

import sys
import chess
from eval import evaluate
from minimax import find_best_move

print("MOCKFISH")
print("Copyright (C) 2023 42-AH")
print("All rights reserved")

def check(board):
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
        print("Fivefold repetition")
        sys.exit()

def main():
    board = chess.Board()
    turn = "NONE"

    while True:
        turn = input("WHITE OR BLACK: ").upper()
        if turn in ["WHITE", "BLACK"]:
            print("")
            break
        else:
            print("Invalid input. Please enter 'WHITE' or 'BLACK'.")

    depth = int(input("DEPTH: "))
    print("")

    if turn == "WHITE":
        while not board.is_game_over():
            check(board)
            if board.turn:
                print("WHITE TO MOVE")
                user_move = input("Move: ")
                move = chess.Move.from_uci(user_move)
                if move in board.legal_moves:
                    board.push(move)
                else:
                    print("Invalid move. Please enter a legal move.")
                    continue
                print("Score: " + str(evaluate(board, False)))
            else:
                print("BLACK TO MOVE")
                move = find_best_move(board, depth)
                board.push(move)
                print("Score: " + str(evaluate(board, False)))
            print(board)
            print(" ")
        check(board)
    else:
        while not board.is_game_over():
            check(board)
            if board.turn:
                print("WHITE TO MOVE")
                move = find_best_move(board, depth)
                board.push(move)
                print("Score: " + str(evaluate(board, False)))
            else:
                print("BLACK TO MOVE")
                user_move = input("Move: ")
                move = chess.Move.from_uci(user_move)
                if move in board.legal_moves:
                    board.push(move)
                else:
                    print("Invalid move. Please enter a legal move.")
                    continue
                print("Score: " + str(evaluate(board, False)))
            print(board)
            print(" ")
if __name__ == "__main__":
    main()

import sys
import tkinter as tk
import chess
from chess_ui import ChessUI
import tkinter as tk
from PIL import Image, ImageTk
import os
import chess
from minimax import find_best_move
import sys
import math



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

    while True:
        player_color = input("Choose your color (WHITE/BLACK): ").upper()
        if player_color in ["WHITE", "BLACK"]:
            break
        else:
            print("Invalid input. Please enter 'WHITE' or 'BLACK'.")

    depth = int(input("DEPTH: "))
    print("")

    root = tk.Tk()
    chess_ui = ChessUI(root, depth, player_color)
    root.mainloop()



if __name__ == "__main__":
    main()

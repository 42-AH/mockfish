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




def main():
    board = chess.Board()
    root = tk.Tk()
    chess_ui = ChessUI(root)
    root.mainloop()



if __name__ == "__main__":
    main()
